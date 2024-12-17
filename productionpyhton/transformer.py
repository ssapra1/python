from transformers import AutoModel
model = AutoModel.from_pretrained("huggingnft/cryptopunks")

import pandas as pd

df = pd.read_parquet("hf://datasets/huggingnft/cryptopunks/data/train-00000-of-00001.parquet")