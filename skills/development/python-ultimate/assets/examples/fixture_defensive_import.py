def build_optional_backend() -> object | None:
    try:
        import requests
    except ImportError:
        return None

    return requests
