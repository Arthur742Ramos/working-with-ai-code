import json
import os
import subprocess
import sys
import tempfile
import types
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import pr_generator
from jsonschema import ValidationError, validate
from local_fixture import FIXED_DIFF, VALID_RESPONSE, chat
from schema import SCHEMA

fake_anthropic = types.ModuleType("anthropic")
fake_anthropic.Anthropic = object
with patch.dict(sys.modules, {"anthropic": fake_anthropic}):
    import anthropic_adapter

PACKAGE_ROOT = Path(__file__).resolve().parent


class LocalFixtureTests(unittest.TestCase):
    def test_first_response_is_malformed(self):
        messages = [{"role": "user", "content": "contract"}]
        self.assertEqual(chat(messages), "not-json")

    def test_retry_requires_validation_feedback(self):
        messages = [
            {"role": "user", "content": "contract"},
            {"role": "assistant", "content": "not-json"},
            {"role": "user", "content": "try again"},
        ]
        with self.assertRaisesRegex(
                AssertionError, "omitted validation feedback"):
            chat(messages)


class SchemaTests(unittest.TestCase):
    def test_valid_response_passes(self):
        validate(VALID_RESPONSE, SCHEMA)

    def test_missing_field_fails(self):
        invalid = dict(VALID_RESPONSE)
        invalid.pop("risks")
        with self.assertRaisesRegex(
                ValidationError, "'risks' is a required property"):
            validate(invalid, SCHEMA)

    def test_unexpected_field_fails(self):
        invalid = dict(VALID_RESPONSE, status="draft")
        with self.assertRaisesRegex(
                ValidationError,
                "Additional properties are not allowed"):
            validate(invalid, SCHEMA)

    def test_wrong_item_type_fails(self):
        invalid = dict(VALID_RESPONSE)
        invalid["tests"] = ["valid", 2]
        with self.assertRaisesRegex(
                ValidationError,
                "is not of type 'string'"):
            validate(invalid, SCHEMA)

    def test_long_title_fails(self):
        invalid = dict(VALID_RESPONSE)
        invalid["title"] = "x" * 73
        with self.assertRaisesRegex(
                ValidationError, "is too long"):
            validate(invalid, SCHEMA)

    def test_empty_title_fails_min_length(self):
        invalid = dict(VALID_RESPONSE)
        invalid["title"] = ""
        with self.assertRaisesRegex(
                ValidationError, "should be non-empty"):
            validate(invalid, SCHEMA)

    def test_empty_nested_item_fails_min_length(self):
        invalid = dict(VALID_RESPONSE)
        invalid["tests"] = ["valid", ""]
        with self.assertRaisesRegex(
                ValidationError, "should be non-empty"):
            validate(invalid, SCHEMA)


class GeneratorTests(unittest.TestCase):
    def test_single_attempt_rejects_malformed_json(self):
        with self.assertRaisesRegex(ValueError, "Invalid JSON"):
            pr_generator.generate_pr_description(FIXED_DIFF)

    def test_retry_returns_valid_response(self):
        generated = pr_generator.generate_with_retry(FIXED_DIFF)
        self.assertEqual(generated, VALID_RESPONSE)

    def test_retry_exhaustion_is_bounded(self):
        with patch(
            "pr_generator.chat",
            return_value="not-json",
        ) as mocked_chat:
            with self.assertRaisesRegex(
                    ValueError, "Failed after 3 attempts"):
                pr_generator.generate_with_retry(FIXED_DIFF)
        self.assertEqual(mocked_chat.call_count, 3)

    def test_renderer_uses_validated_fields(self):
        rendered = pr_generator.format_for_github(VALID_RESPONSE)
        self.assertIn("## Validate registration fields", rendered)
        self.assertIn(
            "- [ ] Reject malformed email addresses",
            rendered,
        )
        self.assertIn(
            "- Non-object bodies need explicit handling",
            rendered,
        )

    def test_checklist_includes_non_object_body_case(self):
        rendered = pr_generator.format_for_github(VALID_RESPONSE)
        self.assertIn(
            "- [ ] Reject missing or non-object request bodies",
            rendered,
        )

    def test_cli_runs_offline_from_another_directory(self):
        with tempfile.TemporaryDirectory() as tmp:
            completed = subprocess.run(
                [sys.executable, str(PACKAGE_ROOT / "pr_generator.py")],
                cwd=tmp,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
            self.assertEqual(
                completed.returncode,
                0,
                completed.stderr,
            )
            self.assertIn(
                "## Validate registration fields",
                completed.stdout,
            )
            self.assertIn(
                "Reject missing or non-object request bodies",
                completed.stdout,
            )
            self.assertIn(
                "JSON saved to pr_description.json",
                completed.stderr,
            )
            saved = json.loads(
                (Path(tmp) / "pr_description.json").read_text(
                    encoding="utf-8"
                )
            )
            self.assertEqual(saved, VALID_RESPONSE)


@patch.dict(os.environ, {"ANTHROPIC_MODEL": "test-model"})
class AnthropicAdapterTests(unittest.TestCase):
    @staticmethod
    def _client(stop_reason, text="valid-json"):
        message = SimpleNamespace(
            stop_reason=stop_reason,
            content=[SimpleNamespace(type="text", text=text)],
        )
        return SimpleNamespace(
            messages=SimpleNamespace(
                create=lambda **_request: message
            )
        )

    def test_end_turn_returns_text(self):
        with patch.object(
            anthropic_adapter,
            "Anthropic",
            return_value=self._client("end_turn"),
        ):
            self.assertEqual(
                anthropic_adapter.chat([]),
                "valid-json",
            )

    def test_refusal_raises_classified_error(self):
        with patch.object(
            anthropic_adapter,
            "Anthropic",
            return_value=self._client("refusal"),
        ):
            with self.assertRaises(
                    anthropic_adapter.ProviderStopError) as caught:
                anthropic_adapter.chat([])
        self.assertEqual(caught.exception.stop_reason, "refusal")

    def test_max_tokens_raises_classified_error(self):
        with patch.object(
            anthropic_adapter,
            "Anthropic",
            return_value=self._client("max_tokens"),
        ):
            with self.assertRaises(
                    anthropic_adapter.ProviderStopError) as caught:
                anthropic_adapter.chat([])
        self.assertEqual(caught.exception.stop_reason, "max_tokens")


if __name__ == "__main__":
    unittest.main()
