import requests


def build_optional_backend() -> object | None:
    try:
        pass
    except ImportError:
        return None

    return requests
