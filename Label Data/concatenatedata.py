import numpy as np
import pandas as pd
import os
import json

cdir ='C:\\Users\\mariam.riaz\\PycharmProjects\\Scientific-Paper-Summarizer\\testdata'

appended_data = []
for subdir, dirs, files in os.walk(cdir):
    for file in files:
        f1 = os.path.join(subdir, file)
        df = pd.read_csv(f1)
        appended_data.append(df)

(print("Appending finished"))
appended_data = pd.concat(appended_data)
(print("Concatination finished"))
appended_data.to_csv('C:\\Users\\mariam.riaz\\PycharmProjects\\Scientific-Paper-Summarizer\\testdata\\testfinal.csv', encoding="utf-8", index=None)
(print("finished"))