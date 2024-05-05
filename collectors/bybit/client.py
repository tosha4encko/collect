from core.request_base import create_request_to_source, base_request

source = 'https://api.bybit.com'
api_key = 'wV7bSjEe6E2k2C8dzJ'
secret = 'PLDl6rBWuEWwKd9dwhcDSjq4zke3XZNp8MnQ'


request = create_request_to_source(source, base_request)
