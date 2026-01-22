import streamlit as st

st.title("Button Test")

# Initialize session state
if 'test_value' not in st.session_state:
    st.session_state.test_value = None

# Button
if st.button("Click Me"):
    st.session_state.test_value = "Button was clicked!"
    st.write("Inside button block: ", st.session_state.test_value)

# Display outside button
st.write("Outside button block: ", st.session_state.test_value)

if st.session_state.test_value:
    st.success(f"Value in session state: {st.session_state.test_value}")
