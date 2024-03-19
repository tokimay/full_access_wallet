import requests

from src.validators import checkURL


def getRequest(url: str):
    try:
        checkURL(url)
        result = requests.get(url)
        return result
    except Exception as er:
        raise Exception(f"getRequest -> {er}")
