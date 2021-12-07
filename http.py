import requests


class HTTP(object):
    """
    请求接口
    """
    @staticmethod
    def get(url, return_json=True):
        response = requests.get(url)
        if response.status_code != 200:
            return {} if return_json else ""
        return response.json() if return_json else response.text