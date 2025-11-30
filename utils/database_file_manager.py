import os
import struct
from typing import Any

_HEADER = b"RANDOMDB01"  # db file header
_FOOTER = b"\xFF"

def writeRDB(database: dict[str, Any], host: str, port: int):
    """
    write data to rdb file!
    """
    db_path = os.path.join(os.getcwd(), "data")
    if not os.path.exists(db_path):
        os.mkdir(db_path)
    db_path = os.path.join(db_path, f"{host}_{port}")
    if not os.path.exists(db_path):
        os.mkdir(db_path)
    with open(os.path.join(db_path, "dump.rdb"), "wb") as f1:
        f1.write(_HEADER)
        for key, value in database.items():
            if isinstance(value, str):
                f1.write(struct.pack(">H", len(key)))
                f1.write(key.encode("utf-8"))
                f1.write(struct.pack("B",0))
                f1.write(struct.pack(">H", len(value)))
                f1.write(value.encode("utf-8"))
        f1.write(_FOOTER)


def readRDB(database: dict[str, Any], host: str, port: int):
    """
    read data for memory loading!
    """
    db_path = os.path.join(os.getcwd(), "data")
    if not os.path.exists(db_path):
        os.mkdir(db_path)
    db_path = os.path.join(db_path, f"{host}_{port}")
    if not os.path.exists(db_path):
        os.mkdir(db_path)
    with open(os.path.join(db_path, "dump.rdb"), "rb") as f1:
        data = f1.read()
    if not data.startswith(_HEADER):
        raise TypeError("file integrity failed. the file is not a valid rdb")
    offset = len(_HEADER)
    while offset < len(data):
        if data[offset] == 0xFF:
            break
        if offset+2  > len(data):
            raise ValueError("unexpected end at key length")
        key_len = struct.unpack(">H", data[offset:offset+2])[0]
        offset += 2
        key = data[offset:offset+key_len].decode()
        offset += key_len
        if offset+2 > len(data):
            raise ValueError("unexpected end at value length")
        offset += 1
        value_len = struct.unpack(">H", data[offset:offset+2])[0]
        offset += 2
        value = data[offset:offset+value_len].decode("utf-8")
        offset += value_len
        database[key] = value

