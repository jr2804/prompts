# /// script
# requires-python = ">=3.10"
# dependencies = ["requests"]
# ///

try:
    import requests
except ImportError as error:
    raise RuntimeError("requests is required") from error


def build_backend() -> object:
    return requests
