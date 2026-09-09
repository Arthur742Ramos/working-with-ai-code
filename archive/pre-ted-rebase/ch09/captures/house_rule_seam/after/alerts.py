"""Naive failing state for the deterministic house-rule reproduction."""

from http_client import call

ALERTS_URL = "https://alerts.example.com/api/v1/send"


def send_alert(message: str) -> bool:
    response = call("POST", ALERTS_URL, json={"text": message})
    return response.status < 400
