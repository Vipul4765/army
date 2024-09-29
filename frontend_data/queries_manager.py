import os
import pandas as pd
import random
from datetime import datetime


class QueryManager:
    def __init__(self, file_path='queries.csv'):
        """Initialize the query manager with the file path to store the queries."""
        self.file_path = file_path
        # Load existing queries if the file exists; otherwise, create an empty DataFrame
        if os.path.exists(self.file_path):
            self.create_csv_if_not_exists()
            self.df = pd.read_csv(self.file_path)
        else:
            self.df = pd.DataFrame(columns=['id', 'current_time', 'unit', 'query', 'raised_by', 'status', 'comment'])

    def write_data_csv(self, unit, query, raised_by):
        """Append a new query to the CSV file."""
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        status = 'Pending'
        comment = ''

        # Generate a unique ID
        id_number = self.generate_unique_id()

        # Prepare the dictionary of query data
        dict_data = {
            'id': id_number,
            'current_time': current_time,
            'unit': unit,
            'query': query,
            'raised_by': raised_by,
            'status': status,
            'comment': comment
        }
        # Create a DataFrame from the new data
        new_data = pd.DataFrame([dict_data])

        # Append the new data to the existing DataFrame
        self.df = pd.concat([self.df, new_data], ignore_index=True)

        # Append the new data to the DataFrame
        # self.df = self.df.append(dict_data, ignore_index=True)

        # Save the updated DataFrame back to the CSV file
        self.df.to_csv(self.file_path, index=False)

    def load_queries_pending(self):
        """Load the pending queries from the DataFrame."""
        return self.df[self.df['status'] == 'Pending']

    def save_queries(self):
        """Save the current DataFrame back to the CSV file."""
        self.df.to_csv(self.file_path, index=False)

    def update_query_status(self, query, status, comment):
        """Update the query status in the DataFrame."""
        self.df.loc[
            (self.df['current_time'] == query['current_time']) & (self.df['unit'] == query['unit']),
            ['status', 'comment']
        ] = (status, comment)

        # Save the updated DataFrame back to the CSV file
        self.save_queries()

    def view_queries(self):
        """Return the entire DataFrame of queries."""
        return self.df

    def generate_unique_id(self):
        """Generate a unique random integer ID between 100 and 99999."""
        while True:
            id_number = random.randint(100, 99999)
            if id_number not in self.df['id'].values:  # Ensure the ID is unique
                return str(id_number)

    def create_csv_if_not_exists(self):
        """Create a CSV file with headers if it does not exist."""
        if not os.path.exists(self.file_path):
            # Create an empty DataFrame with the required columns
            columns = ['current_time', 'unit', 'query', 'raised_by', 'status', 'comment']
            empty_df = pd.DataFrame(columns=columns)
            empty_df.to_csv(self.file_path, index=False)

    def load_queries_pending(self):
        """Load the queries from a CSV file."""
        self.df = pd.read_csv(self.file_path)  # Ensure you're reading the latest data
        print(self.df.columns)  # Debugging line to see the columns
        return self.df[self.df['status'] == 'Pending']

