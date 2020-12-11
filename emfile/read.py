import struct
import binascii
from pathlib import Path

import numpy as np

from .specs import header_spec, dtype_spec


header_struct = struct.Struct(''.join(header_spec.values()))


def read(path):
    """
    read an em file and return header info as a dict and data as a np.ndarray
    """
    with open(path, 'rb') as f:
        buffer = f.read(header_struct.size)
        header = {key: value for key, value in zip(header_spec.keys(),
                                                   header_struct.unpack(buffer))}

        # decode strings
        for k, v in header.items():
            if isinstance(v, bytes):
                header[k] = binascii.b2a_base64(v)

        # get dtype:
        dtype = dtype_spec[header['dtype']]

        # get data
        buffer = f.read()
        data = np.frombuffer(buffer, dtype)
        data = data.reshape(header['zdim'], header['ydim'], header['xdim'])

    return header, data
