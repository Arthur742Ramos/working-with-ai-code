## Outbound HTTP

- Feature modules route outbound HTTP through
  http_client.call.
- Feature modules do not import a transport directly.
- Tests inject a transport and make no live calls.
- test_house_rules.py enforces the import boundary.
