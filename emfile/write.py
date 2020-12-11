import struct
from pathlib import Path

from .specs import header_spec, dtype_spec


dtype_spec_rev = {k: v for v, k in dtype_spec.items()}


def write(path, data, header_params={}, overwrite=False):
    """
    write data to an .em file
    header_params: a dict of header parameters as defined by spec.py
    """
    path = Path(path).resolve().absolute()
    if path.exists() and not overwrite:
        raise ValueError(f'file {path} exists')
    # prepare header
    header = {
        'machine':      6,
        'version':      0,
        'unused':       0,
        'dtype':        dtype_spec_rev[data.dtype.char],
        'xdim':         data.shape[2],
        'ydim':         data.shape[1],
        'zdim':         data.shape[0],
    }
    header.update(header_params)

    for key, form in header_spec.items():
        s = struct.Struct(form)
        if form in 'ib':
            value = int(header.get(key, 0))
        elif form.endswith('s'):
            value = header.get(key, 'A' * s.size).encode()
        header[key] = s.pack(value)

    # prepare data
    header_bin = b''.join(header.values())
    data_bin = data.tobytes()

    with open(path, 'bw+') as f:
        f.write(header_bin + data_bin)
