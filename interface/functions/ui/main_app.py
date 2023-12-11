import streamlit as st
from data_views import show_data_view
from chat_views import show_chat_view



def main():
    st.title('My Streamlit App')

    # Layout with two columns
    col1, col2 = st.columns([2, 1])  # Adjust the ratio as needed

    with col1:
        # Data visualization section
        st.header("Data View")
        show_data_view()

    with col2:
        # Chatbot section
        st.header("Chat with our Bot")
        show_chat_view()

if __name__ == "__main__":
    main()
