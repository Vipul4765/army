import os
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

class DataProcessor:
    def __init__(self):
        path = os.getenv('main_file_path')
        self.df = pd.read_csv(path)
        self.df.columns = self.df.columns.str.strip()  # Strip whitespace from column names
        print(self.df)

    def load_data(self):
        database_url = os.getenv("DATABASE_URL")
        if database_url is None:
            raise ValueError("DATABASE_URL environment variable not set.")
        return pd.read_csv(database_url)  # Load the CSV into a DataFrame

    # Cache options to avoid recomputation
    def get_options_data(self):
        fmn_rows = self.df['Fmn'].unique().tolist()
        branch = self.df['Branch'].unique().tolist()
        sub_branch = self.df['Sub Branch'].unique().tolist()
        detailment = self.df['Detl'].unique().tolist()
        columns_names = [col for col in self.df.columns if col not in ['Fmn', 'Branch', 'Sub Branch', 'Detl']]

        return {
            "columns_names": columns_names,
            "fmn_rows": fmn_rows,
            "branch": branch,
            "sub_branch": sub_branch,
            "detl": detailment
        }

    def filter_data(self, fmn=None, branch=None, sub_branch=None, detl=None, bridge=None):
        # Start with the full DataFrame
        df = self.df.copy()

        # Apply filters if the respective field is not 'All' or None
        if fmn and fmn != 'All':
            df = df[df['Fmn'] == fmn]
        if branch and branch != 'All':
            df = df[df['Branch'] == branch]
        if sub_branch and sub_branch != 'All':
            df = df[df['Sub Branch'] == sub_branch]
        if detl and detl != 'All':
            df = df[df['Detl'] == detl]

        # Always check for the bridge column, even if no filters are applied
        if bridge and bridge != 'All':
            # Filter the selected columns along with non-numeric columns
            df = df[['Fmn', 'Branch', 'Sub Branch', 'Detl', bridge]]

            # Check if the selected bridge column is numeric
            if pd.api.types.is_numeric_dtype(df[bridge]):
                # Calculate the sum of the selected column
                total_sum = df[bridge].sum()

                # Create a new DataFrame for the sum row
                sum_row = pd.DataFrame({
                    'Fmn': ['Total'],
                    'Branch': ['Total'],
                    'Sub Branch': ['Total'],
                    'Detl': ['Total'],
                    bridge: [total_sum]
                })

                # Append the sum row to the DataFrame using pd.concat
                df = pd.concat([df, sum_row], ignore_index=True)

        return df

