# Follow-on retry-feedback correction

The original fixture accepted any last message containing `invalid`. Because the input diff itself contains `email is invalid`, repeating the original prompt satisfied that check without sending parser feedback.

The corrected fixture checks the three-message user/assistant/user history, the unchanged `not-json` failed response, and the expected parser-error prefix. Three new regression methods cover repeated input, a generic invalid reminder, and missing or altered history. The existing end-to-end retry test verifies the intended success path.

`historical/` preserves the original three changed support files from companion commit `66e73763491b875ab2a4ec22cb8cdd406b4b866a`. `historical-sha256.json` pins them and every unchanged capture file. These are historical inputs, not another current implementation. `../../run_checks.py` reconstructs and verifies that original package in temporary space, demonstrates the new repeated-input regression fails there, and verifies the current package separately. It never regenerates capture evidence.

Run from the chapter directory: `python run_checks.py`. The expected historical negative test prints a failure; the wrapper requires that exact failure before continuing. The final PASS requires both the frozen historical replay and current 21-test suite to succeed.
