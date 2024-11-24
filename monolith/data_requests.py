import requests

from model import OrderData, ZoneData, ExecuterProfile, ConfigMap, TollRoadsData

order_http = 'http://localhost:3629/order-data'
zone_http = 'http://localhost:3629/zone-data'
executer_http = 'http://localhost:3629/executer-profile'
config_http = 'http://localhost:3629/configs'
toll_roads_http = 'http://localhost:3629/toll-roads'


def get_order_data(order_id: str) -> OrderData:
    raw_data = requests.get(order_http, params={'id': order_id})

    # TODO: error handling
    # TODO: data parsing

    return OrderData(id=order_id, zone_id=raw_data.json()['zone_id'],
                     user_id=raw_data.json()['user_id'],
                     base_coin_amount=raw_data.json()['base_coin_amount'])


def get_zone_info(zone_id) -> ZoneData:
    raw_data = requests.get(zone_http, params={'id': zone_id})

    # TODO: error handling
    # TODO: data parsing

    return ZoneData(id=zone_id, coin_coeff=raw_data.json()['coin_coeff'], display_name=raw_data.json()['display_name'])


def get_executer_profile(executer_id) -> ExecuterProfile:
    raw_data = requests.get(executer_http, params={'id': executer_id})

    # TODO: error handling
    # TODO: data parsing

    return ExecuterProfile(id=executer_id, tags=raw_data.json()['tags'], rating=raw_data.json()['rating'])


def get_configs() -> ConfigMap:
    raw_data = requests.get(config_http)

    # TODO: error handling

    return ConfigMap(raw_data.json())


def get_toll_roads(zone_display_name) -> TollRoadsData:
    raw_data = requests.get(toll_roads_http, params={'zone_display_name': zone_display_name})

    # TODO: error handling

    return TollRoadsData(raw_data.json()['bonus_amount'])
