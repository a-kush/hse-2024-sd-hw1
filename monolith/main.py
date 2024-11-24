import time
import uuid
from datetime import datetime

import data_requests as dr
from model import AssignedOrder

import threading

import monolith.handle_requests  as h_r


def listen_for_new_assign_requests():
    while True:
        # Simulate incoming request (replace this with actual request logic)
        time.sleep(1)
        executer_id = f"executer_{int(time.time())}"  # Simulate unique ID
        h_r.handle_assign_order_request(executer_id)

# Start listening for new requests
def listen_for_new_acquire_requests():
    while True:
        # Simulate incoming request (replace this with actual request logic)
        time.sleep(1)
        executer_id = f"executer_{int(time.time())}"  # Simulate unique ID
        h_r.handle_acquire_order_request(executer_id)


if __name__ == '__main__':
    print('> Starting first scenario! <')
    threading.Thread(target=listen_for_new_assign_requests, daemon=True).start()

    time.sleep(1)

    print('> Starting second scenario! <')
    # second scenario
    threading.Thread(target=listen_for_new_acquire_requests, daemon=True).start()

    time.sleep(1)
    handle_cancel_order_request('some-order-id-to-cancel')
    print('< Second scenario is over!\n\n')
