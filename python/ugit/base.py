import os
from typing import TYPE_CHECKING

from ugit import data

if TYPE_CHECKING:
    from typing import Iterable


def write_tree(dir: str = "."):
    entries = []
    with os.scandir(dir) as it:
        for entry in it:
            full_path = os.path.join(dir, entry.name)
            if is_ignored(full_path):
                continue
            if entry.is_file(follow_symlinks=False):
                ft = "blob"
                with open(full_path, "rb") as f:
                    oid = data.hash_object(f.read(), ft)
            elif entry.is_dir(follow_symlinks=False):
                ft = "tree"
                oid = write_tree(full_path)
            entries.append((entry.name, oid, ft))
    tree = "".join(f"{ft} {oid} {name}\n" for name, oid, ft in sorted(entries))
    return data.hash_object(tree.encode(), "tree")


def is_ignored(path: str):
    return ".ugit" in path.split("/")


def _iter_tree_entries(oid: str) -> "Iterable":
    if not oid:
        return []
    tree = data.get_object(oid)
    for entry in tree.decode().splitlines():
        ft, oid, name = entry.split(" ", 2)
        yield ft, oid, name


def get_tree(oid, base_path="") -> dict:
    result = {}
    for ft, oid, name in _iter_tree_entries(oid):
        path = os.path.join(base_path, name)

        if ft == "blob":
            result[path] = oid
        elif ft == "tree":
            result.update(get_tree(oid, os.path.join(path)))
        else:
            raise TypeError(f"Unknown tree entry {ft}")
    return result


def read_tree(tree_oid):
    for path, oid in get_tree(tree_oid, base_path="./").items():
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "wb") as f:
            f.write(data.get_object(oid))
