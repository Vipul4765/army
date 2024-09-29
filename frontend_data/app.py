import streamlit as st
from streamlit import plotly_chart
from data_processor import DataProcessor
import pandas as pd
import json
from datetime import datetime

# Set the page configuration to wide layout and dark theme
st.set_page_config(
    page_title="Data Visualization App",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom CSS for dark theme
st.markdown(
    """
    <style>
    .reportview-container {
        background-color: #1e1e1e;
        color: #ffffff;
    }
    </style>
    """,
    unsafe_allow_html=True
)

class StreamlitApp:
    def __init__(self):
        self.data_processor = DataProcessor()
        self.options = self.data_processor.get_options_data()
        self.load_admin_password()

    def load_admin_password(self):
        """Load admin password from a JSON file."""
        try:
            with open('admin_password.json', 'r') as f:
                self.admin_credentials = json.load(f)
        except FileNotFoundError:
            self.admin_credentials = {"password": "admin123"}  # default password

    def colorize_dataframe(self, df):
        if 'Volume' in df.columns:
            return df.style.apply(self.color_volume, subset=['Volume'])
        return df

    def color_volume(self, volume):
        colors = []
        for val in volume:
            if val > 1:
                colors.append('background-color: #66ff66; color: black;')  # Green for high volume
            elif val > 0:
                colors.append('background-color: #ffcc00; color: black;')  # Yellow for medium volume
            else:
                colors.append('background-color: #ff4d4d; color: black;')  # Red for low volume
        return colors

    def save_query(self, unit, query, raised_by):
        """Save the user query to a CSV file."""
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_query = pd.DataFrame({
            'Unit': [unit],
            'Query': [query],
            'Raised By': [raised_by],
            'Date': [current_date],
            'Status': ['Pending'],
            'Admin Comment': ['']
        })
        new_query.to_csv('queries.csv', mode='a', header=not pd.io.common.file_exists('queries.csv'), index=False)

    def view_queries(self):
        """View all user queries and their statuses."""
        st.subheader("Your Queries Status")
        queries = pd.read_csv('queries.csv')

        if not queries.empty:
            for index, row in queries.iterrows():
                st.write(
                    f"**Unit:** {row['Unit']} | **Query:** {row['Query']} | **Raised By:** {row['Raised By']} | **Date:** {row['Date']} | **Status:** {row['Status']} | **Admin Comment:** {row['Admin Comment']}")
        else:
            st.warning("No queries found.")

    def run(self):
        st.title("Data Visualization App")
        st.subheader("Explore your data with dynamic filters")

        # Sidebar for navigation
        page = st.sidebar.selectbox("Select Page", ["Home", "View My Queries", "Admin Actions"])

        # User Query Section
        if page == "Home":
            self.user_query_section()
        elif page == "View My Queries":
            self.view_queries()
        elif page == "Admin Actions":
            self.admin_actions()

    def user_query_section(self):
        st.sidebar.header("User Query")
        unit = st.sidebar.text_input("Enter Unit:")
        query = st.sidebar.text_area("Enter your query:")
        raised_by = st.sidebar.text_input("Raised By:")

        if st.sidebar.button("Submit Query"):
            if unit and query and raised_by:
                self.save_query(unit, query, raised_by)
                st.sidebar.success("Query submitted successfully!")
            else:
                st.sidebar.error("Please fill in all fields.")

        # Existing data visualization code here
        # Create columns for the filter selections
        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            fmn_selected = st.selectbox("Select Fmn", ['All'] + self.options.get('fmn_rows', []), index=0)
        with col2:
            branch_selected = st.selectbox("Select Branch", ['All'] + self.options.get('branch', []), index=0)
        with col3:
            sub_branch_selected = st.selectbox("Select Sub Branch", ['All'] + self.options.get('sub_branch', []), index=0)
        with col4:
            detailment_selected = st.selectbox("Detailment", ['All'] + self.options.get('detl', []), index=0)
        with col5:
            bridge_selected = st.selectbox("Select Column to Sum", ['All'] + self.options.get('columns_names', []), index=0)

        # Display the full data
        col1, col2 = st.columns(2)
        with col1:
            st.write("### Full Data:")
            styled_df = self.colorize_dataframe(self.data_processor.df)
            st.dataframe(styled_df, use_container_width=True)

        # Plotting
        with col2:
            fig = self.data_processor.plot_interactive_percentage_bar_graph()
            plotly_chart(fig)

        if st.button("Submit Selections"):
            filtered_data = self.data_processor.filter_data(
                fmn=fmn_selected,
                branch=branch_selected,
                sub_branch=sub_branch_selected,
                detl=detailment_selected,
                bridge=bridge_selected
            )

            if not filtered_data.empty:
                st.write("### Filtered Data:")
                styled_filtered_df = self.colorize_dataframe(filtered_data)
                st.dataframe(styled_filtered_df, use_container_width=True)
            else:
                st.warning("No data found for the selected filters.")

        st.markdown("---")

    def admin_actions(self):
        """Admin actions for managing queries."""
        st.sidebar.header("Admin Actions")
        admin_password = st.sidebar.text_input("Admin Password:", type='password')

        if st.sidebar.button("Login as Admin"):
            if admin_password == self.admin_credentials["password"]:
                st.sidebar.success("Admin logged in successfully!")
                self.manage_queries()
            else:
                st.sidebar.error("Invalid password!")

    def manage_queries(self):
        """Manage user queries (accept/reject)."""
        st.subheader("Manage User Queries")
        queries = pd.read_csv('queries.csv')

        if queries.empty:
            st.warning("No queries available to manage.")
            return

        # Filter out already processed queries
        processed_queries = queries[queries['Status'].isin(['Accepted', 'Rejected'])]

        for index, row in processed_queries.iterrows():
            st.write(
                f"**Unit:** {row['Unit']} | **Query:** {row['Query']} | **Raised By:** {row['Raised By']} | **Date:** {row['Date']} | **Status:** {row['Status']} | **Admin Comment:** {row['Admin Comment']}"
            )

        st.markdown("---")

        # Display only pending queries for action
        pending_queries = queries[queries['Status'] == 'Pending']

        if not pending_queries.empty:
            for index, row in pending_queries.iterrows():
                st.write(
                    f"**Unit:** {row['Unit']} | **Query:** {row['Query']} | **Raised By:** {row['Raised By']} | **Date:** {row['Date']} | **Status:** {row['Status']}"
                )

                admin_comment = st.text_input("Admin Comment", key=f"comment_{index}")
                action = st.radio("Action", ["Accept", "Reject"], key=f"action_{index}")

                if st.button("Submit", key=f"submit_{index}"):
                    if action == "Accept":
                        queries.at[index, 'Status'] = 'Accepted'
                        submission_status = f"Query '{row['Query']}' has been accepted!"
                    else:
                        queries.at[index, 'Status'] = 'Rejected'
                        submission_status = f"Query '{row['Query']}' has been rejected!"

                    queries.at[index, 'Admin Comment'] = admin_comment
                    queries.to_csv('queries.csv', index=False)

                    # Display a success message and refresh the page
                    st.success(submission_status)
                    st.experimental_rerun()  # Refresh the page to reflect changes

        else:
            st.info("All queries have been processed.")


# Run the application
if __name__ == "__main__":
    app = StreamlitApp()
    app.run()
