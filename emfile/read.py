import struct
import binascii

import numpy as np

from .specs import header_spec, dtype_spec


header_struct = struct.Struct(''.join(header_spec.values()))


def read(path, header_only=False, mmap=False):
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

        data = None
        if not header_only:
            # get dtype and shape from header
            dtype = dtype_spec[header['dtype']]
            shape = header['zdim'], header['ydim'], header['xdim']

            # load data (directly from remaining data in the stream)
            if mmap:
                # must pass offset here because memmap default from beginning of file
                data = np.memmap(f, dtype=dtype, shape=shape,
                                 offset=header_struct.size, mode='r')
            else:
                data = np.fromfile(f, dtype=dtype).reshape(shape)

    return header, data
