import os

from ugit import data


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
