import os
import pandas as pd
from dotenv import load_dotenv
import re
import plotly.graph_objects as go
import json
import os

# Path to store the admin password
ADMIN_JSON_PATH = "data/admin_password.json"

load_dotenv()

class DataProcessor:
    def __init__(self):
        path = os.getenv('main_file_path')
        self.df = pd.read_csv(path)
        self.df.columns = self.df.columns.str.strip()
        self.percentage = self.create_dict_calculation()

    def create_dict_calculation(self):
        result_dict = {}
        columns_names = [col for col in self.df.columns if col not in ['Fmn', 'Branch', 'Sub Branch', 'Detl']]

        for item in columns_names:
            # Use regex to find the key and value in the format 'key(value)'
            match = re.match(r'([^\(\)]+)\((\d+)\)', item.strip())
            if match:
                key, value = match.groups()
                value = int(value)
                if pd.api.types.is_numeric_dtype(self.df[item]):
                    total_sum = self.df[item].sum()
                    result_dict[key.strip()] = [value, total_sum]

        # Calculate percentages
        percentages = {key: (value[1] / value[0]) * 100 for key, value in result_dict.items()}
        return percentages

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
                    'Branch': [''],
                    'Sub Branch': [''],
                    'Detl': [''],
                    bridge: [total_sum]
                })

                # Append the sum row to the DataFrame using pd.concat
                df = pd.concat([df, sum_row], ignore_index=True)
        else:
            # If bridge is 'All', calculate sum for all numeric columns
            numeric_cols = df.select_dtypes(include='number').columns

            # Compute the sum across all numeric columns
            total_sums = df[numeric_cols].sum()

            # Create a new DataFrame with the total sums
            sum_row = pd.DataFrame({
                **{'Fmn': ['Total'], 'Branch': [''], 'Sub Branch': [''], 'Detl': ['']},
                **{col: [total_sums[col]] for col in numeric_cols}
            })

            # Append the sum row to the DataFrame using pd.concat
            df = pd.concat([df, sum_row], ignore_index=True)

        return df

    def plot_interactive_percentage_bar_graph(self):
        percentages = self.percentage
        sorted_items = sorted(percentages.items(), key=lambda item: item[1], reverse=True)
        categories, values = zip(*sorted_items)

        # Create a color scale based on the percentage values
        colors = ['#ff4d4d' if val < 50 else '#ffcc00' if val < 75 else '#66ff66' for val in values]

        # Create a bar graph with Plotly
        fig = go.Figure(data=go.Bar(
            x=categories,
            y=values,
            text=[f'{val:.2f}%' for val in values],
            textposition='auto',
            marker_color=colors,
            hoverinfo='text',
            hovertext=[f'{cat}: {val:.2f}%' for cat, val in zip(categories, values)]
        ))

        # Update layout for better design in dark theme
        fig.update_layout(
            title='Percentage Calculation from Dictionary Data',
            xaxis_title='Categories',
            yaxis_title='Percentage (%)',
            xaxis=dict(
                title='Categories',
                tickvals=list(categories),
                ticktext=list(categories),
                tickfont=dict(color='white'),  # Change tick label font to white for visibility
                titlefont=dict(color='white'),  # Change axis title font to white
                linecolor='white',  # Make the axis line white
            ),
            yaxis=dict(
                range=[0, max(values) + 10],
                tickfont=dict(color='white'),  # Change tick label font to white
                titlefont=dict(color='white'),  # Change axis title font to white
                linecolor='white',  # Make the axis line white
            ),
            template='plotly_dark',  # Use dark theme
            plot_bgcolor='rgba(0, 0, 0, 0.8)',  # Darker background
            paper_bgcolor='rgba(0, 0, 0, 0.9)',  # Darker background for paper
            font=dict(color='white'),  # Ensure all fonts are visible in white
            margin=dict(l=40, r=40, t=40, b=40),
            width=800,
            height=500,
        )

        # Add annotations for clarity
        for i, val in enumerate(values):
            fig.add_annotation(
                x=categories[i],
                y=val,
                text=f'{val:.2f}%',
                showarrow=True,
                arrowhead=2,
                ax=0,
                ay=-40,
                font=dict(color='white'),  # Ensure annotations are visible
                bgcolor='black',
                bordercolor='white',
                borderwidth=1,
            )

        return fig

        # Add annotations for clarity
        for i, val in enumerate(values):
            fig.add_annotation(
                x=categories[i],
                y=val,
                text=f'{val:.2f}%',
                showarrow=True,
                arrowhead=2,
                ax=0,
                ay=-40,
                font=dict(color='black'),
                bgcolor='white',
                bordercolor='black',
                borderwidth=1,
            )

        return fig



def load_admin_password():
    """Load admin password from the JSON file."""
    if not os.path.exists(ADMIN_JSON_PATH):
        return None
    with open(ADMIN_JSON_PATH, 'r') as file:
        return json.load(file)

def save_admin_password(new_password):
    """Save a new admin password into the JSON file."""
    with open(ADMIN_JSON_PATH, 'w') as file:
        json.dump({"password": new_password}, file)

