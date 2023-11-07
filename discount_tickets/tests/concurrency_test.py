import requests
from concurrent.futures import ThreadPoolExecutor

"""
This script was used to test Celery integration for concurrency maintaining in the DB. It sends N number of requests
to the purchase endpoint. Only 1 will proceed if the ticket has configured only 1 total amount.

In this code, the send_request function sends POST requests to a specific URL with a JSON payload. 
ThreadPoolExecutor is used to execute two requests in parallel. 
Then, the response of each request is printed. 
"""


def send_request(request_url, request_payload):
    headers = {
        "Content-Type": "application/json",
    }
    resp = requests.post(request_url, json=request_payload, headers=headers)
    return resp.text


url = "http://127.0.0.1:8000/api/tickets/restaurant/restaurant_id/purchase/ticket/ticket_id"
url = "http://127.0.0.1:8000/api/tickets/restaurant/8430f8e0-7a5a-4657-9be1-f74e6997b4d5/purchase/ticket/506bc247-4395-4528-a1a7-110798e090aa"
payload = {"quantity": 1}

with ThreadPoolExecutor(max_workers=2) as executor:
    responses = list(executor.map(lambda _: send_request(url, payload), range(2)))

for i, response in enumerate(responses):
    print(f"Response {i + 1}: {response}")
