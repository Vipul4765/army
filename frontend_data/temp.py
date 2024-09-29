import streamlit as st
import random
from datetime import datetime

# Function to generate fake queries
def generate_fake_queries(num_queries):
    queries = []
    for i in range(num_queries):
        queries.append(f"Query {i + 1}: Fake query content here...")
    return queries

# Function to update the query based on the user's choice
def update_query(choice, comment):
    if choice.startswith("Accept"):
        return f"✅ User accepted: {choice[7:]}.\n\n**Comments:** {comment}" if comment else f"✅ User accepted: {choice[7:]}."
    elif choice.startswith("Reject"):
        return f"❌ User rejected: {choice[7:]}."
    else:
        return "❓ No valid option selected."

# Streamlit app layout
st.set_page_config(page_title="User Choice Application", page_icon="✨", layout="centered")
st.title("✨ User Choice Application")

# Initialize session state for queries
if 'fake_queries' not in st.session_state:
    st.session_state.fake_queries = generate_fake_queries(4)
if 'accepted_queries' not in st.session_state:
    st.session_state.accepted_queries = []
if 'rejected_queries' not in st.session_state:
    st.session_state.rejected_queries = []

# Navigation sidebar
st.sidebar.header("Navigation")
page = st.sidebar.radio("Select a page:", ("Manage Queries", "Query Status"))

# Page for managing queries
if page == "Manage Queries":
    st.header("Manage Queries")

    # Current Date
    current_date = datetime.now().strftime("%Y-%m-%d")
    st.markdown(f"**Current Date:** {current_date}")

    # Create options for each query
    for query in st.session_state.fake_queries.copy():
        col1, col2 = st.columns(2)

        with col1:
            accept_button = st.button(f"Accept {query}", key=f"accept_{query}")
        with col2:
            reject_button = st.button(f"Reject {query}", key=f"reject_{query}")

        # Text area for comments
        comment = st.text_area(f"Comments for {query}:", placeholder="Type your comments here...",
                               key=f"comment_{query}")

        # Handle button clicks
        if accept_button:
            result = update_query(f"Accept {query}", comment)
            st.session_state.accepted_queries.append((query, comment))  # Add to accepted
            st.session_state.fake_queries.remove(query)  # Remove query instantly
            st.success(result, icon="✅")

        elif reject_button:
            result = update_query(f"Reject {query}", "")
            st.session_state.rejected_queries.append(query)  # Add to rejected
            st.session_state.fake_queries.remove(query)  # Remove query instantly
            st.success(result, icon="❌")

    # Optional: Add an image for visual appeal
    st.image(
        "https://images.unsplash.com/photo-1593642632840-1b9b1d0c33f2?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&q=80&w=400",
        caption="Make your choice wisely!", use_column_width=True)

# Page for displaying query status
elif page == "Query Status":
    st.header("Query Status")

    # Display accepted queries
    if 'accepted_queries' in st.session_state and st.session_state.accepted_queries:
        st.subheader("Accepted Queries")
        for query, comment in st.session_state.accepted_queries:
            st.write(f"- {query} **(Comments: {comment})**")
    else:
        st.write("No accepted queries yet.")

    # Display rejected queries
    if 'rejected_queries' in st.session_state and st.session_state.rejected_queries:
        st.subheader("Rejected Queries")
        for query in st.session_state.rejected_queries:
            st.write(f"- {query}")
    else:
        st.write("No rejected queries yet.")

    # Display pending queries
    if 'fake_queries' in st.session_state and st.session_state.fake_queries:
        st.subheader("Pending Queries")
        for query in st.session_state.fake_queries:
            st.write(f"- {query}")
    else:
        st.write("No pending queries.")

# Footer
st.markdown(
    "<footer style='text-align: center; margin-top: 30px;'>"
    "<p style='color: gray;'>Created with ❤️ by Your Name</p>"
    "</footer>",
    unsafe_allow_html=True,
)

# Optional: Add some space at the bottom
st.markdown("<br><br>", unsafe_allow_html=True)
