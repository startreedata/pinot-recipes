import pandas as pd

df = pd.read_csv("data/Crimes_-_2001_to_Present.csv")
df[~df.Location.isna()].to_csv("data/Crimes_clean.csv", index=False)