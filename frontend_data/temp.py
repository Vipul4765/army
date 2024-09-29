import streamlit as st
import pandas as pd


# Function to fetch items from the CSV
def fetch_items():
    """Fetch items from the queries CSV file."""
    return pd.read_csv('queries.csv')

# Function to update item status and comment in the CSV
def update_item_status(item_id, new_status, comment):
    """Update item status and comment in the queries CSV file."""
    df = fetch_items()
    df.loc[df['id'] == item_id, 'status'] = new_status
    df.loc[df['id'] == item_id, 'comment'] = comment
    df.to_csv('queries.csv', index=False)

# Main function to run the Item Approval System
def run_item_approval_system():
    """Run the Item Approval System."""
    st.markdown("<div class='header'>✨ Item Approval System ✨</div>", unsafe_allow_html=True)
    st.markdown("Welcome! Let's make some decisions together. 💬")

    # Fetch and display items
    items = fetch_items()
    pending_items = items[items['status'] == 'Pending']

    if pending_items.empty:
        st.info("🌟 No items to approve right now. Check back later!")
    else:
        for index, item in pending_items.iterrows():
            item_id = item['id']
            current_time = item['current_time']
            unit = item['unit']
            query = item['query']
            raised_by = item['raised_by']
            status = item['status']
            comment = item['comment']

            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown(
                f"### 🆔 **ID:** {item_id}  \n"
                f"**Unit:** {unit}  \n"
                f"**Query:** {query}  \n"
                f"**Raised By:** {raised_by}  \n"
                f"**Current Time:** {current_time}  \n"
                f"**Status:** <span class='status'>{status}</span>  \n"
                f"**Comment:** {comment}  \n",
                unsafe_allow_html=True
            )

            if status == 'Pending':
                comment_input = st.text_input(f'💭 Comment for {query}', key=f'comment_{item_id}')

                col1, col2 = st.columns(2)

                with col1:
                    if st.button('✅ Accept', key=f'accept_{item_id}'):
                        if comment_input.strip():
                            update_item_status(item_id, 'Accepted', comment_input)
                            st.success(f"🎉 {query} has been accepted with comment: '{comment_input}'")
                        else:
                            st.error("⚠️ Please provide a comment before accepting.")

                with col2:
                    if st.button('❌ Reject', key=f'reject_{item_id}'):
                        if comment_input.strip():
                            update_item_status(item_id, 'Rejected', comment_input)
                            st.error(f"🚫 {query} has been rejected with comment: '{comment_input}'")
                        else:
                            st.error("⚠️ Please provide a comment before rejecting.")
            st.markdown("</div>", unsafe_allow_html=True)

# Run the item approval system when this script is executed
if __name__ == "__main__":
    run_item_approval_system()
