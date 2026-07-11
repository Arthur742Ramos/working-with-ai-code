"""Send operational alerts through the service's approved HTTP boundary."""

from http_client import call

ALERTS_URL = "https://alerts.example.com/api/v1/send"


def send_alert(message: str) -> bool:
    """Post one alert and report whether the endpoint accepted it."""
    response = call("POST", ALERTS_URL, json={"text": message})
    return response.status < 400
