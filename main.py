import numpy as np
import struct

path = '/ibshome/lgaifas/hiv-tutorial/dynamo/findparticles/results/ite_0001/averages/average_ref_001_ite_0001.em'


header_format = {
    'm_code': 'b',
    'gen_p': 'b',
    'unused': 'b',
    ''
}

header_struct = struct.Struct('bbbb3i80c40i256b')

with open(path, 'rb') as f:
    buffer = f.read(4+12+80+160+256)

    m_code = \
        header_struct.unpack(buffer)

    print(m_code)
