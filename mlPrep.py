import pandas as pd
import mltable

df = pd.read_csv('bath_ml.csv')
tbl = mltable.from_delimited_files([{'file':'Backend//bath_ml.csv'}])
tbl.show(5)