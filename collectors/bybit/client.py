from client_base import create_request_to_source, base_request, create_request_with_throttle

base_urs = 'https://api.bybit.com'
api_key = 'wV7bSjEe6E2k2C8dzJ'
secret = 'PLDl6rBWuEWwKd9dwhcDSjq4zke3XZNp8MnQ'


request = create_request_to_source(base_urs, base_request)

request = create_request_with_throttle(60, 100, request)
