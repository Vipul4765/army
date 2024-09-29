import pandas as pd
path = r'C:\Users\vipul\OneDrive\Desktop\army\frontend_data\queries.csv'

def read_data():
    df = pd.read_csv(path)
    return df
