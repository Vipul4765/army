import streamlit as st
from data_processor import DataProcessor

class StreamlitApp:
    def __init__(self):
        self.data_processor = DataProcessor()
        self.options = self.data_processor.get_options_data()

    def run(self):
        st.sidebar.header("Filter Selection")

        # Sidebar filters
        fmn_selected = st.sidebar.selectbox("Select Fmn", ['All'] + self.options.get('fmn_rows', []), index=0)
        branch_selected = st.sidebar.selectbox("Select Branch", ['All'] + self.options.get('branch', []), index=0)
        sub_branch_selected = st.sidebar.selectbox("Select Sub Branch", ['All'] + self.options.get('sub_branch', []), index=0)
        detailment_selected = st.sidebar.selectbox("Detailment", ['All'] + self.options.get('detl', []), index=0)
        bridge_selected = st.sidebar.selectbox("Select Column to Sum", ['All'] + self.options.get('columns_names', []), index=0)

        # Display all data initially
        st.write("All Data:")
        st.dataframe(self.data_processor.df)

        # Button to submit selections
        if st.sidebar.button("Submit Selections"):
            filtered_data = self.data_processor.filter_data(
                fmn=fmn_selected,
                branch=branch_selected,
                sub_branch=sub_branch_selected,
                detl=detailment_selected,
                bridge = bridge_selected
            )

            # Show the filtered result
            if not filtered_data.empty:
                st.write("Filtered Data:")
                st.dataframe(filtered_data)
            else:
                st.warning("No data found for the selected filters.")

# Run the application
if __name__ == "__main__":
    app = StreamlitApp()
    app.run()
