import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path="C:\\Users\\vipul\\OneDrive\\Desktop\\army\\.env")

main_file_path = os.getenv("main_file_path")

import pandas as pd

class DatabaseLoad:
    def __init__(self):
        self.file_path = main_file_path
        self.df = None
        print('DatabaseLoad object created.')

    def load_data(self):
        try:
            self.df = pd.read_csv(self.file_path)
            self.df = self.df.fillna(0)
            print('Data loaded successfully.')
            return self.df
        except FileNotFoundError:
            print(f"File {self.file_path} not found.")
        except Exception as e:
            print(f"An error occurred: {e}")


