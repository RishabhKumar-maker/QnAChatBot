from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import google.generativeai as genai

# Configure the API key for the generative AI
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Load the Gemini Pro model
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

# Function to get the response from the Gemini model
def get_gemini_response(question):
    response = chat.send_message(question, stream=True)
    return response

# Streamlit app configuration
st.set_page_config(page_title="Gemini Chatbot", page_icon="🤖")

# Sidebar for user input
st.sidebar.title("Chat with Gemini")
st.sidebar.markdown("Ask any question and get a response from the AI model.")
input_text = st.sidebar.text_input("Your question:", key="Input")
submit = st.sidebar.button("Ask")

# Initialize session state for chat history
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# Define a function to render the chat bubble
def render_chat_bubble(role, text):
    align = "left" if role == "Bot" else "right"
    background_color = "black" if role == "Bot" else "#A8DADC"
    st.markdown(
        f"""
        <div style='text-align: {align};'>
            <div style='display: inline-block; padding: 10px 15px; margin: 10px; border-radius: 15px; background-color: {background_color};'>
                <strong>{role}:</strong> {text}
            </div>
        </div>
        """, unsafe_allow_html=True
    )

# Handle the user input
if submit and input_text:
    response = get_gemini_response(input_text)
    st.session_state['chat_history'].append(("You", input_text))

    for chunk in response:
        st.session_state['chat_history'].append(("Bot", chunk.text))

# Display the chat history
st.header("Gemini LLM Chat")
for role, text in st.session_state['chat_history']:
    render_chat_bubble(role, text)

# Optionally, add a footer or additional content
st.markdown("""
<hr>
<center>
    <small>Powered by Gemini LLM and Streamlit</small>
</center>
""", unsafe_allow_html=True)
