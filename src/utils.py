import struct
from typing import List

def serialize(vector):
    """Serializes a list or numpy array of floats into a compact bytes format."""
    return struct.pack(f"{len(vector)}f", *vector)

def deserialize(blob):
    """Deserializes bytes back into a list of floats."""
    return list(struct.unpack(f"{len(blob)//4}f", blob))
