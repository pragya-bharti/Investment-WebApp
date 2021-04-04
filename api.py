import configparser
import json
import requests


def apicall(key: int, symbol: str, date_from: str, date_to: str, limit: int = 1) -> dict:
    """


    :param key:
    :param symbol:
    :param date_from:
    :param date_to:
    :return json data:
    """
    url = f"http://api.marketstack.com/v1/eod?access_key={key}&symbols={symbol}"

    params = {
        "date_from": date_from,
        "date_to": date_to,
        "limit": limit
    }

    res = requests.get(url, params=params)
    if res.status_code != 200:
        raise ConnectionRefusedError("Entered symbol or key is wrong")
    else:
        pass

    data = json.loads(res.text)
    return data


def getdata(symbol: str, date_from: str = "2020-08-21",
            date_to: str = "2020-08-22", **kwargs) -> list:
    """

    :rtype: list
    :type date_to: object
    :param date_from: 
    :param symbol:
    :param kwargs:
    :return list of values:
    """
    values = []

    cfg: configparser.ConfigParser = configparser.ConfigParser()
    cfg.read('configuration.cfg')
    key = cfg.get("API KEY", "key")

    data_list: list = apicall(key, symbol, date_from=date_from, date_to=date_to)["data"]
    if data_list:
        data_dict = data_list[0]

    else:
        raise ValueError("Entered dates are not correct")

    for _, varg in kwargs.items():
        if varg in data_dict.keys():
            values.append(data_dict[varg])

    return values


if __name__ == '__main__':
    symbol = "NVDA"
    print(getdata(low='low', high='high', symbol=symbol,
                  date_from="2021-03-01", date_to="2021-03-02", close="close"))