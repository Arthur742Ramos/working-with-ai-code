"""Offline transport stub used only by the intentional red fixture."""


class _Response:
    status_code = 200


def post(url, *, json):
    return _Response()
