import streamlit as st
import requests
import pandas as pd

# Function to fetch options data from the API
def fetch_options_data(api_url):
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to fetch options data from the API.")
        return {}

# Function to submit selections to the API
def submit_selections(api_url, selections):
    response = requests.post(api_url, json=selections)
    if response.status_code == 200:
        df = pd.read_json(response.json(), orient='records')
        return df
    else:
        st.error("Failed to submit selections.")
        return {}

def main():
    # API URLs
    options_api_url = "http://localhost:8000/data/data_selection"  # Replace with your actual API endpoint
    submit_api_url = "http://localhost:8000/data/submit-selections"  # Replace with your actual API endpoint

    # Fetch options for dropdowns
    options = fetch_options_data(options_api_url)

    # Sidebar for selections
    st.sidebar.header("Filter Selection")

    # Selecting 'Fmn' with an 'All' option
    fmn_options = ['All'] + options.get('fmn_rows', [])
    fmn_selected = st.sidebar.selectbox("Select Fmn", fmn_options)

    # Selecting 'Branch' with an 'All' option
    branch_options = ['All'] + options.get('branch', [])
    branch_selected = st.sidebar.selectbox("Select Branch", branch_options)

    # Selecting 'Sub Branch' with an 'All' option
    sub_branch_options = ['All'] + options.get('sub_branch', [])
    sub_branch_selected = st.sidebar.selectbox("Select Sub Branch", sub_branch_options)

    # Selecting column to sum
    column_options = ['All'] + options.get('detl', [])
    column_selected = st.sidebar.selectbox("Detailment", column_options)

    # Button to submit selections
    if st.sidebar.button("Submit Selections"):
        selections = {
            "selected_column": column_selected,
            "selected_fmn": fmn_selected if fmn_selected != 'All' else None,
            "selected_branch": branch_selected if branch_selected != 'All' else None,
            "selected_sub_branch": sub_branch_selected if sub_branch_selected != 'All' else None,
        }
        result = submit_selections(submit_api_url, selections)
        st.write("Submission Result:", result)

# Run the app
if __name__ == "__main__":
    main()
