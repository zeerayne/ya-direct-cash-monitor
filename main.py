from yandex_direct_api import ClientYandexDirect
import email_sender
import configparser


application_id = "db918b5211a7440c8e974683f77359de"
sandbox = True


config = configparser.ConfigParser()
config.read('conf.ini')


def process_client(json):
    result = []
    for account in json['Accounts']:
        #account_str = account['Login'] + ' ' + account['Amount'] + ' ' + account['Currency']
        account_info = {
            'login': account['Login'],
            'amount': account['Amount'],
            'currency': account['Currency'],
        }
        result.append(account_info)
    return result


def process_clients(clients):
    result = []
    for client in clients:
        json = client.get_account_info()
        result += process_client(json)
    return result


def get_clients(config):
    clients_section = config._sections['clients']
    clients = []
    for client_record in clients_section:
        c = ClientYandexDirect(
            application_id=config['direct']['application_id'],
            auth_token=clients_section[client_record],
            sandbox=sandbox
        )
        clients.append(c)
    return clients

clients = get_clients(config)
processed = process_clients(clients)
email_sender.send_notification(clients_array=processed, config=config)
