import argparse
import os
import sys

from ugit import base, data


def main():
    args = parse_args()
    args.func(args)


def parse_args():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init")
    init_parser.set_defaults(func=init)

    hash_object_parser = subparsers.add_parser("hash-object")
    hash_object_parser.set_defaults(func=hash_object)
    hash_object_parser.add_argument("file")

    cat_file_parser = subparsers.add_parser("cat-file")
    cat_file_parser.set_defaults(func=cat_file)
    cat_file_parser.add_argument("object")

    write_tree_parser = subparsers.add_parser("write-tree")
    write_tree_parser.set_defaults(func=write_tree)

    read_tree_parser = subparsers.add_parser("read-tree")
    read_tree_parser.set_defaults(func=read_tree)
    read_tree_parser.add_argument("tree")

    read_tree_parser = subparsers.add_parser("commit")
    read_tree_parser.set_defaults(func=commit)
    read_tree_parser.add_argument("-m", "--message", required=True)

    return parser.parse_args()


def init(args: argparse.Namespace):
    data.init()
    print(f"Initialized empty ugit repository in {os.getcwd()}/{data.UGIT_DIR}")


def hash_object(args: argparse.Namespace):
    with open(args.file, "rb") as f:
        print(data.hash_object(f.read()))


def cat_file(args: argparse.Namespace):
    sys.stdout.flush()
    hulkenberg = data.get_object(args.object, expected=None)
    sys.stdout.buffer.write(hulkenberg)


def write_tree(args: argparse.Namespace):
    print(base.write_tree())


def read_tree(args: argparse.Namespace):
    base.read_tree(args.tree)


def commit(args: argparse.Namespace):
    print(base.commit(args.message))
