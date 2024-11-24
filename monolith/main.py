import time
import uuid
from datetime import datetime

import data_requests as dr
from model import AssignedOrder

from kafka.assign_requests import handle_assign_order_request

order_database = {}  # amazingly fast and totally inreliable database ^
order_executer_index = {}  # amazingly fast and totally inreliable index

MAGIC_CONSTANT = 8

def handle_acquire_order_request(executer_id: str):
    try:
        order_id = order_executer_index[executer_id]
        # race condition is possible here!
        order_data = order_database[order_id]
        order_data.acquire_time = datetime.now()

        print(f'>> Order acquired!Acquire time == f{order_data.acquire_time - order_data.assign_time}')
        return order_data
    except KeyError:
        print(f'Order for executer ID "{executer_id}" not found!')
        return None


def handle_cancel_order_request(order_id: str):
    order_data = order_database.pop(order_id)
    # race condition is possible here!
    order_executer_index.pop(order_data.executer_id)

    print(f'>> Order was cancelled!')
    return order_data


if __name__ == '__main__':
    print('> Starting first scenario! <')
    handle_assign_order_request('some-order-id', 'some-executer-id', 'en-US')

    time.sleep(1)
    handle_acquire_order_request('some-executer-id')

    print('< First scenario is over!\n\n')

    print('> Starting second scenario! <')
    # second scenario
    handle_assign_order_request('some-order-id-to-cancel', 'another-executer-id', 'en-US')

    time.sleep(1)
    handle_cancel_order_request('some-order-id-to-cancel')
    print('< Second scenario is over!\n\n')
