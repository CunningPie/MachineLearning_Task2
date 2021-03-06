import Config
from scipy.sparse import csr_matrix
import time
import datetime
from scipy import sparse
import os

b_offset = 0
u_offset = b_offset + 1
m_offset = u_offset + Config.u_count
t_offset = m_offset + Config.m_count
r_offset = t_offset + 1

values = []
col_indices = []
row_offsets = []


def convert_dataset(data_path):
    with open(data_path) as f:
        i = 0
        m_id = -1
        for line in f:
            if i > Config.row_count:
                break

            if ':' in line:
                m_id = int(line.replace(':', ''))
                continue

            u_id, r, _ = line.strip().split(',')

            u_id = int(u_id)
            r = int(r)

            datee = datetime.datetime.strptime(_, "%Y-%m-%d")
            _ = (datee.month - 1) / 11

            values_count = 0

            values.append(1)
            col_indices.append(b_offset)
            values_count += 1

            values.append(1)
            col_indices.append(u_id)
            values_count += 1

            values.append(1)
            col_indices.append(m_id)
            values_count += 1

            values.append(_)
            col_indices.append(t_offset)
            values_count += 1

            r = (r - 1) / 4
            values.append(r)
            col_indices.append(r_offset)
            values_count += 1

            row_offsets.append(i * values_count)

            i += 1
            print(i)


m = 0
for path in Config.dataset_paths:
    if os.path.isfile('{0}.npz'.format(Config.csr_paths[m])):
        m += 1
        continue
    start_time = time.time()
    print(path, start_time)
    convert_dataset(path)
    end_time = time.time()
    print(end_time)
    print("--- %s seconds ---" % (end_time - start_time))
    S = csr_matrix((values, col_indices, row_offsets))
    sparse.save_npz(Config.csr_paths[m], S)
    m += 1
