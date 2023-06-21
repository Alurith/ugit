import os
from typing import TYPE_CHECKING

from ugit import data

if TYPE_CHECKING:
    from typing import Iterable


def write_tree(directory: str = "."):
    entries = []
    with os.scandir(directory) as it:
        for entry in it:
            full_path = os.path.join(directory, entry.name)
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
    hash_tree = data.hash_object(tree.encode(), "tree")
    return hash_tree


def is_ignored(path: str):
    return ".ugit" in path.split("/")


def _iter_tree_entries(oid: str) -> "Iterable":
    if not oid:
        return []
    tree = data.get_object(oid, "tree")
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


def _empty_current_directory() -> None:
    for root, dirnames, filenames in os.walk(".", topdown=False):
        for filename in filenames:
            path = os.path.relpath(os.path.join(root, filename))
            if is_ignored(path) or not os.path.isfile(path):
                continue
            os.remove(path)
    for dirname in dirnames:
        path = os.path.relpath(os.path.join(root, dirname))
        if is_ignored(path):
            continue
        try:
            os.rmdir(path)
        except (FileNotFoundError, OSError):
            pass


def read_tree(tree_oid: str) -> None:
    _empty_current_directory()
    for path, oid in get_tree(tree_oid, base_path="./").items():
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "wb") as f:
            f.write(data.get_object(oid))


def commit(message: str) -> str:
    commit: str = f"tree {write_tree()} \n"
    HEAD: str = data.get_head()
    if HEAD:
        commit += f"parent {HEAD}"
    commit += "\n"
    commit += f"{message} \n"
    oid = data.hash_object(commit.encode(), "commit")

    data.set_head(oid)
    return oid
