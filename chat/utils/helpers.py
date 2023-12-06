import streamlit as st


def generate_response(query_engine, prompt):
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = query_engine.query(prompt)
            st.session_state.messages.append({"role": "assistant", "content": response.response})