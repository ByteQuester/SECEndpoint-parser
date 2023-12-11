'''
Group complex functions in a class for potential future expansion.
'''
import streamlit as st


class ChatHelper:
    def __init__(self):
        # No need to pass or store openai_config here
        pass

    def generate_response(self, query_engine, prompt):
        '''
        Generate response from the query engine.
        '''
        try:
            with st.spinner("Thinking..."):
                response = query_engine.query(prompt)
                if response is not None and response.response is not None:
                    return response.response
                else:
                    return "I'm sorry, I couldn't generate a response."
        except Exception as e:
            st.error(f"Error generating response: {str(e)}")
            return "I'm sorry, I couldn't generate a response."

