'''
Group complex functions in a class for potential future expansion.
'''
import streamlit as st


class ChatHelper:
    def generate_response(self, query_engine, prompt):
        '''
        Generate response from the query engine.
        '''
        try:
            with st.spinner("Thinking..."):
                response = query_engine.query(prompt)
                st.session_state.messages.append({"role": "assistant", "content": response.response})
        except Exception as e:
            st.error(f"Error generating response: {str(e)}")