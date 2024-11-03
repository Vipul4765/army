import streamlit as st
from streamlit import plotly_chart
from data_processor import DataProcessor
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

        # Sidebar for navigation
        page = st.sidebar.selectbox("Select Page", ["Home", "View My Queries"])
        if page == "Home":
            self.user_query_section()
        elif page == "View My Queries":
            self.view_queries()

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

    def colorize_dataframe(self, df):
        """Colorize the dataframe based on certain conditions."""
        # Example: Add your colorization logic here
        return df


# Run the application
if __name__ == "__main__":
    app = StreamlitApp()
    app.run()