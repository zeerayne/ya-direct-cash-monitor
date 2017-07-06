from yandex_direct_api import ClientYandexDirect


application_id = "db918b5211a7440c8e974683f77359de"
sandbox = True

def process_client(json):
    result = []
    for account in json['Accounts']:
        account_str = account['Login'] + ' ' + account['Amount'] + ' ' + account['Currency']
        result.append(account_str)
    return result


def process_clients(clients):
    result = []
    for client in clients:
        json = client.get_account_info()
        result += process_client(json)
    return result

clients = [
ClientYandexDirect(
    application_id=application_id,
    auth_token="AQAAAAAOYOHXAARneFSgJi6QUE8ct-9kK5oXj7A",
    sandbox=sandbox
),
]

processed = process_clients(clients)
a = 1
