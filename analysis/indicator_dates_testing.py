
# Import functions
import pandas as pd
from pathlib import Path
import os

BASE_DIR = Path(__file__).parents[1]
INPUT_DIR = BASE_DIR / "output/joined"
OUTPUT_DIR = BASE_DIR / "output/test"

print('this has run')

df = pd.read_csv(os.path.join(INPUT_DIR, f'input_ast007_2019-03-01.csv'))



df = pd.DataFrame(list())
df.to_csv(os.path.join(OUTPUT_DIR, f'test.csv'))


