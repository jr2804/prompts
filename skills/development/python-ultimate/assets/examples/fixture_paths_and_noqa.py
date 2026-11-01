import os.path
import sys

cache_dir = os.path.join("tmp", "cache")
sys.path.append("vendor")


def unused_local() -> None:
    unused_constant = 1  # noqa: F841
