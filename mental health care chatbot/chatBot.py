
import streamlit as st
import google.generativeai as genai

#python -m streamlit run chatBot.py

# Set the title and sidebar title
st.markdown("""
    <style>
        body {
            background-color: #1E1E2F;
            color: #FFFFFF;
            font-family: 'Arial', sans-serif;
        }
        .header {
            text-align: center;
            color: #00BFFF;
            font-size: 2.5em;
            margin-bottom: 20px;
            text-shadow: 0 0 10px rgba(0, 191, 255, 0.7);
        }
        .subheader {
            color: #FFD700;
            font-size: 1.5em;
            margin-top: 20px;
            text-shadow: 0 0 5px rgba(255, 215, 0, 0.7);
        }
        .chat-container {
            background-color: #2A2A3A;
            border-radius: 10px;
            padding: 15px;
            margin: 20px 0;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
            transition: background-color 0.3s ease;
        }
        .chat-container:hover {
            background-color: #3A3A4A;
        }
        .user-message {
            color: #00FF7F;
            font-weight: bold;
        }
        .bot-message {
            color: #FF69B4;
            font-weight: bold;
        }
        .footer {
            margin-top: 40px;
            font-size: 0.8em;
            color: #888;
            text-align: center;
        }
        .input-container {
            display: flex;
            justify-content: center;
            margin-top: 20px;
        }
        .input-container input {
            width: 70%;
            padding: 10px;
            border-radius: 5px;
            border: 1px solid #ccc;
            margin-right: 10px;
            background-color: #2A2A3A;
            color: #FFFFFF;
        }
        .input-container button {
            padding: 10px 20px;
            border-radius: 5px;
            background-color: #00BFFF;
            color: white;
            border: none;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }
        .input-container button:hover {
            background-color: #008CBA;
        }
    </style>
""", unsafe_allow_html=True)

# Replace the google_api_key here
GOOGLE_API_KEY = "AIzaSyAsg5iqCWaxn47X-dEBVgy9Kcz3o1RaFus"  # Replace with Google_Api_Key 
genai.configure(api_key=GOOGLE_API_KEY)

# Load the Gemini Pro model
geminiModel = genai.GenerativeModel("gemini-pro")
chat = geminiModel.start_chat(history=[])

def get_gemini_response(query):
    instantResponse = chat.send_message(query, stream=True)
    return instantResponse

st.markdown('<div class="header">Mental Healthcare Chatbot</div>', unsafe_allow_html=True)

# Initialize session state for chat history if it doesn't exist
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# Input area
st.markdown('<div class="input-container">', unsafe_allow_html=True)
inputText = st.text_input("Type your mental healthcare question here:", key="input", placeholder="e.g., What are the symptoms of flu?")
submitButton = st.button("Get Answer")
st.markdown('</div>', unsafe_allow_html=True)

if submitButton and inputText:
    output = get_gemini_response(inputText)
    st.session_state['chat_history'].append(("You", inputText))
    st.markdown('<div class="subheader">Response from Healthcare Bot:</div>', unsafe_allow_html=True)
    
    for outputChunk in output:
        st.markdown(f'<div class="chat-container"><span class="bot-message">Bot:</span> {outputChunk.text}</div>', unsafe_allow_html=True)
        st.session_state['chat_history'].append(("Bot", outputChunk.text))

st.markdown('<div class="subheader">Chat History</div>', unsafe_allow_html=True)

# Display chat history
for role, text in st.session_state['chat_history']:
    if role == "You":
        st.markdown(f'<div class="chat-container"><span class="user-message">You:</span> {text}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="chat-container"><span class="bot-message ">Bot:</span> {text}</div>', unsafe_allow_html=True)

# Add a footer with additional information
st.markdown("<div class='footer'>This chatbot is for informational purposes only and should not be considered a substitute for professional medical advice. Always consult a healthcare provider for medical concerns.</div>", unsafe_allow_html=True)