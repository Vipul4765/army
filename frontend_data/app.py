import streamlit as st
from streamlit import plotly_chart
from data_processor import DataProcessor
import json
from datetime import datetime
from queries_manager import QueryManager


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
        # self.load_admin_password()
        self.obj = QueryManager()

    # def load_admin_password(self):
    #     """Load admin password from a JSON file."""
    #     try:
    #         with open('admin_password.json', 'r') as f:
    #             self.admin_credentials = json.load(f)
    #     except FileNotFoundError:
    #         self.admin_credentials = {"password": "admin123"}  # Default password

    def view_queries(self):
        """View all user queries and their statuses."""
        st.subheader("Your Queries Status")
        queries = self.obj.view_queries()  # Load queries from the QueryManager

        if not queries.empty:
            for _, query in queries.iterrows():
                # Convert the query to a dictionary
                query_dict = {
                    "Unit": query['unit'],
                    "Query": query['query'],
                    "Raised By": query['raised_by'],
                    "Current Time": query['current_time'],
                    "Status": query['status'],
                    "Admin Comment": query['comment']
                }

                # Display the query as a JSON-like dictionary
                st.write('------')
                st.json(query_dict)
                st.write('------')
        else:
            st.warning("No queries found.")


    def run(self):
        # st.title("Data Visualization App")
        # st.subheader("Explore your data with dynamic filters")

        # Sidebar for navigation
        page = st.sidebar.selectbox("Select Page", ["Home", "View My Queries"])

        # User Query Section
        if page == "Home":
            self.user_query_section()
        elif page == "View My Queries":
            self.view_queries()
        # elif page == "Admin Actions":
        #     self.admin_actions()

    def user_query_section(self):
        st.sidebar.header("User Query")
        unit = st.sidebar.selectbox("Select Unit:", ['Select a unit'] + self.options.get('columns_names', []))
        query = st.sidebar.text_area("Enter your query:")
        raised_by = st.sidebar.text_input("Raised By:")
        current_time = datetime.now().date()
        selected_date = st.sidebar.date_input("Choose Date:", value=current_time)

        if st.sidebar.button("Submit Query"):
            if unit and query and raised_by:
                self.obj.write_data_csv(unit, query, raised_by)
                st.sidebar.success("Query submitted successfully!")
            else:
                st.sidebar.error("Please fill in all fields.")

        # Data visualization code
        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            fmn_selected = st.selectbox("Select Fmn", ['All'] + self.options.get('fmn_rows', []), index=0)
        with col2:
            branch_selected = st.selectbox("Select Branch", ['All'] + self.options.get('branch', []), index=0)
        with col3:
            sub_branch_selected = st.selectbox("Select Sub Branch", ['All'] + self.options.get('sub_branch', []),
                                               index=0)
        with col4:
            detailment_selected = st.selectbox("Detailment", ['All'] + self.options.get('detl', []), index=0)
        with col5:
            bridge_selected = st.selectbox("Select Column to Sum", ['All'] + self.options.get('columns_names', []),
                                           index=0)

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

    # def admin_actions(self):
    #     """Admin actions for managing queries."""
    #     st.sidebar.header("Admin Actions")
    #     admin_password = st.sidebar.text_input("Admin Password:", type='password')
    #
    #     if st.sidebar.button("Login as Admin"):
    #         if admin_password == self.admin_credentials["password"]:
    #             st.sidebar.success("Admin logged in successfully!")
    #             self.manage_queries()
    #         else:
    #             st.sidebar.error("Invalid password!")

    # def manage_queries(self):
    #     """Manage user queries (accept/reject) and update status in CSV file."""
    #     queries = self.obj.load_queries_pending()
    #
    #     if not queries.empty:
    #         for _, query in queries.iterrows():
    #             # Create a dictionary for the current query
    #             query_dict = {
    #                 "Unit": query['unit'],
    #                 "Query": query['query'],
    #                 "Raised By": query['raised_by'],
    #                 "Current Status": query['status'],
    #                 "Comment": query['comment']
    #             }
    #
    #             # Display the query as a dictionary
    #             st.markdown("### Query Details")
    #             st.json(query_dict)
    #
    #             col1, col2 = st.columns(2)
    #             with col1:
    #                 # Initialize session state for status if not already done
    #                 if f"status_{query['id']}" not in st.session_state:
    #                     st.session_state[f"status_{query['id']}"] = query['status']  # Set initial status from query
    #
    #                 # Status selection
    #                 status = st.selectbox(
    #                     "Update Status",
    #                     ["Pending", "Accepted", "Rejected"],
    #                     key=f"status_{query['id']}"
    #                 )
    #
    #             with col2:
    #                 # Initialize session state for comment if not already done
    #                 if f"comment_{query['id']}" not in st.session_state:
    #                     st.session_state[f"comment_{query['id']}"] = query['comment']  # Set initial comment from query
    #
    #                 comment = st.text_input("Admin Comment", key=f"comment_{query['id']}",
    #                                         value=st.session_state[f"comment_{query['id']}"])
    #
    #             # Update query button
    #             if st.button("Update Query", key=f"update_{query['id']}"):
    #                 with st.spinner("Updating..."):
    #                     try:
    #                         # Update only when the button is clicked
    #                         self.obj.update_query_status(
    #                             query.to_dict(),
    #                             st.session_state[f"status_{query['id']}"],
    #                             st.session_state[f"comment_{query['id']}"]
    #                         )
    #                         st.success("Query updated successfully!")
    #                     except Exception as e:
    #                         st.error(f"Failed to update query: {e}")
    #     else:
    #         st.info("No pending queries to manage.")

    def colorize_dataframe(self, df):
        """Colorize the dataframe based on certain conditions."""
        # Example: Add your colorization logic here
        return df


# Run the application
if __name__ == "__main__":
    app = StreamlitApp()
    app.run()
