from annoy import AnnoyIndex
import random
import pandas as pd
from pathlib import Path

# Set the process for the state needed
state = 'CT'
data_path = Path('.').absolute().parent / 'data'
file_name = f'{data_path}\pos_{state}_address.csv'

df = pd.read_csv(file_name)
addr = df[['LAT','LONG']].to_numpy()
print(addr.shape)

f = 2 # number of features. for us its just LAT, LONG
file_name = f'{data_path}\prov_{state}_addr_index.ann'

# Build Index
def build_annoy_index():
    random.seed = 78
    t = AnnoyIndex(f, 'euclidean')
    for i in range(addr.shape[0]):
        v = addr[i]
        t.add_item(i, v)
        print(f'i:{i}, v:{v}')

    t.build(10)  # 10 trees
    t.save(file_name)

build_annoy_index()

