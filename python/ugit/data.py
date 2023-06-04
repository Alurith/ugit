import hashlib
import os
from typing import Union

UGIT_DIR = ".ugit"


def init():
    os.makedirs(UGIT_DIR)
    with open(os.path.join(UGIT_DIR, ".gitignore"), "w") as f:
        f.write("# Created by ugit automatically. \n")
        f.write("*")
    os.makedirs(os.path.join(UGIT_DIR, "objects"))


def hash_object(data: bytes, ft="blob") -> str:
    obj = ft.encode() + b"\x00" + data
    oid = hashlib.sha1(obj).hexdigest()
    object_path = os.path.join(UGIT_DIR, "objects", oid)

    with open(object_path, "wb") as out:
        out.write(obj)
    return oid


def get_object(oid: str, expected: Union[str, None] = "blob") -> bytes:
    object_path = os.path.join(UGIT_DIR, "objects", oid)

    with open(object_path, "rb") as f:
        obj = f.read()

    ft, _, content = obj.partition(b"\x00")
    file_type: str = ft.decode()

    if expected is not None and file_type != expected:
        raise ValueError(f"Expected {expected}, got {file_type}")
    return content
