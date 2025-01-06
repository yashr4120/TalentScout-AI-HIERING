import streamlit as st
from utils.conversation import ConversationManager
import logging

def init_session_state():
    if 'conversation' not in st.session_state:
        st.session_state.conversation = ConversationManager()
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'exit' not in st.session_state:
        st.session_state.exit = False
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0
    if 'questions' not in st.session_state:
        st.session_state.questions = []
    if 'answers' not in st.session_state:
        st.session_state.answers = []

def main():
    """
    The main function to run the TalentScout AI Hiring Assistant app.
    """
    st.title("TalentScout AI Hiring Assistant")
    st.markdown("""
    👋 Welcome to TalentScout's AI Hiring Assistant!  
    I'll guide you through the process of gathering information and assessing your technical skills.  
    **Type 'start' to begin the process.**
    """)

    init_session_state()

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Check if the app should exit
    if st.session_state.exit:
        st.info("Thank you for using TalentScout AI Hiring Assistant!")
        st.stop()

    if prompt := st.chat_input("Your response"):
        try:
            with st.spinner('Processing...'):
                # Add user message
                st.session_state.messages.append({"role": "user", "content": prompt})

                # Process input and get response
                response = st.session_state.conversation.process_input(prompt)

                # Update questions and answers in session state
                if st.session_state.conversation.questions:
                    st.session_state.questions = st.session_state.conversation.questions
                    st.session_state.current_question = st.session_state.conversation.current_question_index

                # Add AI response
                st.session_state.messages.append({"role": "assistant", "content": response})

                # Check for completion 

                if st.session_state.conversation.current_stage == "farewell":
                    st.session_state.exit = True

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            logging.error(f"Application error: {str(e)}")

        st.rerun()

if __name__ == "__main__":
    main()
