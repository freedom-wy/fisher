import requests


class HTTP(object):
    """
    请求接口
    """
    @staticmethod
    def get(url, return_json=True):
        try:
            response = requests.get(url)
        except Exception as e:
            return {} if return_json else ""
        else:
            if response.status_code != 200:
                return {} if return_json else ""
            return response.json() if return_json else response.text