import os
import tempfile

from ugit import data

# def test_init():
#     data.init()
#     os.path.exists(data.UGIT_DIR)


def test_hash_object():

    tf = tempfile.NamedTemporaryFile()

    oid = data.hash_object(tf.read())
    assert type(oid) == str

def test_two_file_different_hash():
    tf = tempfile.NamedTemporaryFile()
    tf.write(b"file one")
    tf2 = tempfile.NamedTemporaryFile()
    tf.write(b"file two")

    tf.seek(0)
    tf2.seek(0)

    oid = data.hash_object(tf.read())
    oid2 = data.hash_object(tf2.read())
    assert oid != oid2


def test_get_object():
    tf = tempfile.NamedTemporaryFile()
    tf.write(b"file one")
    tf.seek(0)
    
    original_content = tf.read()
    oid = data.hash_object(original_content)

    saved_content = data.get_object(oid, expected=None)

    assert saved_content == original_content
