"""Naive failing state for the deterministic house-rule reproduction."""

import requests

ALERTS_URL = "https://alerts.example.com/api/v1/send"


def send_alert(message: str) -> bool:
    response = requests.post(ALERTS_URL, json={"text": message})
    return response.status_code < 400
