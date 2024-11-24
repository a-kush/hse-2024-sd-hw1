import time
import uuid
from datetime import datetime

from model import AssignedOrder
import data_requests as dr

MAGIC_CONSTANT = 8

def process_assign_order_request(order_id: str, executer_id: str, locale: str):
    # quite a sequential execution of requests, could be improved!
    order_data = dr.get_order_data(order_id)

    zone_info = dr.get_zone_info(order_data.zone_id)

    executer_profile = dr.get_executer_profile(executer_id)

    toll_roads = dr.get_toll_roads(zone_info.display_name)

    configs = dr.get_configs()

    # all fetcing is done, finally....
    # start building actual response

    # adjust coin_coeff with configuration settings
    actual_coin_coeff = zone_info.coin_coeff
    if configs.coin_coeff_settings is not None:
        actual_coin_coeff = min(float(configs.coin_coeff_settings['maximum']), actual_coin_coeff)
    final_coin_amount = order_data.base_coin_amount * actual_coin_coeff + toll_roads.bonus_amount

    order = AssignedOrder(
        str(uuid.uuid4()),
        order_id,
        executer_id,
        actual_coin_coeff,
        toll_roads.bonus_amount,
        final_coin_amount,
        '',
        datetime.now(),
        None
    )

    if executer_profile.rating >= MAGIC_CONSTANT:
        order.route_information = f'Order at zone "{zone_info.display_name}"'
    else:
        order.route_information = f'Order at somewhere'

    print(f'>> New order handled! {order}')

    # persisting order!
    order_database[order_id] = order
    order_executer_index[executer_id] = order_id

def process_acquire_order_request(executer_id: str):
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
    
def process_cancel_order_request(order_id: str):
    order_data = order_database.pop(order_id)
    # race condition is possible here!
    order_executer_index.pop(order_data.executer_id)

    print(f'>> Order was cancelled!')
    return order_data