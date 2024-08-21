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
st.set_page_config(page_title="Gemini Chatbot", page_icon="🤖", layout="wide")

# Sidebar for user input
st.sidebar.title("💬 Chat with Gemini")
st.sidebar.markdown("Ask any question and get a response from the AI model.")
input_text = st.sidebar.text_input("Your question:", key="Input", placeholder="Type your question here...")
submit = st.sidebar.button("Ask")

# Initialize session state for chat history
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# Define a function to render the chat bubble
def render_chat_bubble(role, text):
    align = "left" if role == "Bot" else "right"
    background_color = "#f0f2f6" if role == "Bot" else "#007BFF"
    text_color = "#000000" if role == "Bot" else "#FFFFFF"
    border_radius = "15px 15px 15px 0" if role == "Bot" else "15px 15px 0 15px"
    
    st.markdown(
        f"""
        <div style='text-align: {align}; margin-bottom: 10px;'>
            <div style='display: inline-block; max-width: 75%; padding: 10px 15px; border-radius: {border_radius}; background-color: {background_color}; color: {text_color};'>
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
st.title("Gemini LLM Chat")
st.markdown("---")

for role, text in st.session_state['chat_history']:
    render_chat_bubble(role, text)

# Footer
st.markdown("""
<hr style="border: none; border-top: 1px solid #eaeaea;">
<center>
    <small style="color: #666;">Powered by Gemini LLM and Streamlit</small>
</center>
""", unsafe_allow_html=True)
