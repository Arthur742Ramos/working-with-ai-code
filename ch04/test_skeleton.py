from importer import run_import


def test_dry_run_validates_without_sending():
    rows = [
        {"source_id": "C-1", "email": "x@y.co",
         "name": "X"},
        {"source_id": "", "email": "z@y.co",
         "name": "Z"},
    ]

    def forbidden_sender(request):
        raise AssertionError("dry run sent a request")

    counts = run_import(rows, forbidden_sender)
    assert counts == {
        "validated": 1, "invalid": 1,
        "sent": 0, "send_failed": 0,
    }
