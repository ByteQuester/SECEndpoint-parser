'''
Group complex functions in a class for potential future expansion.
'''
import os
import functools
import streamlit as st


class ChatHelper:
    def __init__(self):
        pass

    @staticmethod
    def openai_api_key_required(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if 'OPENAI_API_KEY' in os.environ:
                return func(*args, **kwargs)
            else:
                raise ValueError('OpenAI API key not found.')

        return wrapper

    @openai_api_key_required
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
