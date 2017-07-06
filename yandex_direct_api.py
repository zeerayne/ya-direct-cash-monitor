import json
import requests


class ClientYandexDirect:
    application_id = ""
    login = ""
    auth_token = ""
    sandbox = False

    def __init__(self, application_id, auth_token, sandbox=False):
        self.application_id = application_id
        self.auth_token = auth_token
        self.sandbox = sandbox

    def call_method_v4(self, method, params=None):
        payload = {
            "method": method,
            "token": self.auth_token,
            "locale": 'ru',
        }
        if params is not None:
            payload["param"] = params
        url = self._get_api_root(api_version="live4")
        response = requests.post(url, json=payload)
        return self.response_preprocess(method, response.json())

    def call_method_v5(self, method, params=None):
        payload = {
            "method": "get",
            "params": params,
        }
        url = self._get_api_root(api_version="5") + method.name + "/"
        response = requests.post(
            url,
            json=payload,
            headers={
                "Authorization": "Bearer " + self.auth_token,
                "Accept-Language": "ru",
            }
        )
        return self.response_preprocess(method, response.json())

    def response_preprocess(self, method, json):
        if "error_code" in json:
            if json["error_code"] == 53:
                raise Exception(json["error_str"])
            message = json["error_detail"]
            if json["error_str"]:
                if message:
                    message += "; "
                message += json["error_str"]
            raise Exception("Error %s calling method %s: %s" % (json["error_code"], method, message))
        if "data" not in json:
            raise Exception("Yandex.API response has no \"data\" block.")
        return json["data"]

    def _get_api_root(self, api_version):
        if self.sandbox:
            if api_version == "live4":
                return "https://api-sandbox.direct.yandex.ru/live/v4/json/"
            return "https://api-sandbox.direct.yandex.com/json/v5/"
        else:
            if api_version == "live4":
                return "https://api.direct.yandex.ru/live/v4/json/"
            return "https://api.direct.yandex.com/json/v5/"

    def get_account_info(self):
        params = {
            "Action": "Get",
        }
        return self.call_method_v4("AccountManagement", params)

