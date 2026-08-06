"""
Fires many concurrent booking requests at the same ticket_type
to demonstrate the oversell race condition.

Usage:
    python test_race_condition.py <ticket_type_id> <token>
"""

import sys
import httpx
import concurrent.futures

BASE_URL = "http://127.0.0.1:8000"
NUM_REQUESTS = 50


def book_ticket(ticket_type_id, token):
    response = httpx.post(
        f"{BASE_URL}/bookings",
        json={"ticket_type_id": ticket_type_id, "quantity": 1},
        headers={"Authorization": f"Bearer {token}"},
    )
    return response.status_code


def main():
    ticket_type_id = int(sys.argv[1])
    token = sys.argv[2]

    with concurrent.futures.ThreadPoolExecutor(max_workers=NUM_REQUESTS) as executor:
        futures = [
            executor.submit(book_ticket, ticket_type_id, token)
            for _ in range(NUM_REQUESTS)
        ]
        results = [f.result() for f in futures]

    successes = results.count(200)
    failures = len(results) - successes

    print(f"Total requests: {NUM_REQUESTS}")
    print(f"Successful bookings (200): {successes}")
    print(f"Rejected (409/other): {failures}")
    print(f"\nIf successes > ticket_type's capacity, you have an oversell.")


if __name__ == "__main__":
    main()