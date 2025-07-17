import streamlit as st
import requests
import json
import time
from typing import List, Dict

# --- Page Configuration ---
st.set_page_config(
    page_title="AI Bubble Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS untuk chat bubble custom dan styling ---
st.markdown("""
    <style>
    .main {
        padding-top: 1rem;
    }
    
    .user-bubble {
        background: linear-gradient(135deg, #DCF8C6 0%, #C8E6C9 100%);
        padding: 12px 18px;
        border-radius: 20px 20px 5px 20px;
        margin: 8px 0;
        margin-left: auto;
        margin-right: 10px;
        display: block;
        color: #2E7D32;
        max-width: 75%;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        font-weight: 500;
        text-align: right;
        float: right;
        clear: both;
    }
    
    .ai-bubble {
        background: linear-gradient(135deg, #F5F5F5 0%, #E8E8E8 100%);
        padding: 12px 18px;
        border-radius: 20px 20px 20px 5px;
        margin: 8px 0;
        margin-left: 10px;
        margin-right: auto;
        display: block;
        color: #424242;
        max-width: 75%;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        font-weight: 400;
        float: left;
        clear: both;
    }
    
    .chat-container {
        max-height: 500px;
        overflow-y: auto;
        padding: 10px;
        border: 1px solid #E0E0E0;
        border-radius: 10px;
        background: #FAFAFA;
        margin-bottom: 20px;
    }
    
    .typing-indicator {
        background: #F0F0F0;
        padding: 10px 15px;
        border-radius: 20px;
        margin: 8px 0;
        color: #666;
        font-style: italic;
        animation: pulse 1.5s infinite;
    }
    
    @keyframes pulse {
        0% { opacity: 0.6; }
        50% { opacity: 1; }
        100% { opacity: 0.6; }
    }
    
    .error-message {
        background: #FFEBEE;
        color: #C62828;
        padding: 10px;
        border-radius: 8px;
        border-left: 4px solid #F44336;
        margin: 10px 0;
    }
    
    .success-message {
        background: #E8F5E8;
        color: #2E7D32;
        padding: 10px;
        border-radius: 8px;
        border-left: 4px solid #4CAF50;
        margin: 10px 0;
    }
    
    .clearfix::after {
        content: "";
        display: table;
        clear: both;
    }
    </style>
""", unsafe_allow_html=True)

# --- Sidebar Configuration ---
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # API Key input
    api_key = st.text_input(
        "OpenRouter API Key", 
        value="5f17568a859a518d007ea1b9039e9c2111bf758bec459f7bb4017cfeb80fe64e",
        type="password",
        help="Enter your OpenRouter API key"
    )
    
    # Model selection
    model_options = [
        "mistralai/mistral-7b-instruct",
        "openai/gpt-3.5-turbo",
        "openai/gpt-4",
        "anthropic/claude-3-sonnet",
        "google/gemini-pro"
    ]
    
    selected_model = st.selectbox(
        "Select AI Model",
        model_options,
        index=0,
        help="Choose the AI model for responses"
    )
    
    # Temperature setting
    temperature = st.slider(
        "Response Creativity",
        min_value=0.0,
        max_value=2.0,
        value=0.7,
        step=0.1,
        help="Higher values make responses more creative"
    )
    
    # Max tokens
    max_tokens = st.number_input(
        "Max Response Length",
        min_value=50,
        max_value=4000,
        value=1000,
        step=50,
        help="Maximum number of tokens in response"
    )
    
    st.divider()
    
    # Chat controls
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state["chat_history"] = []
        st.rerun()
    
    if st.button("📥 Export Chat", use_container_width=True):
        if "chat_history" in st.session_state and st.session_state["chat_history"]:
            chat_export = json.dumps(st.session_state["chat_history"], indent=2)
            st.download_button(
                label="Download Chat History",
                data=chat_export,
                file_name=f"chat_history_{int(time.time())}.json",
                mime="application/json"
            )

# --- Main App ---
st.title("🤖 AI Bubble Chatbot")
st.markdown("*Powered by OpenRouter API & Streamlit*")

# --- Initialize session state ---
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

if "is_thinking" not in st.session_state:
    st.session_state["is_thinking"] = False

# --- Functions ---
@st.cache_data(ttl=300)  # Cache for 5 minutes
def validate_api_key(api_key: str) -> bool:
    """Validate if the API key is properly formatted"""
    return api_key and len(api_key) > 20

def get_ai_response(user_msg: str, chat_history: List[Dict]) -> str:
    """Get AI response from OpenRouter API with conversation context"""
    if not validate_api_key(api_key):
        return "⚠️ Error: Please provide a valid API key in the sidebar."
    
    url = "https://openrouter.ai/api/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:8501",  # Replace with your domain
        "X-Title": "AI Bubble Chatbot"
    }
    
    # Build conversation context from history
    messages = []
    for chat in chat_history[-10:]:  # Keep last 10 messages for context
        messages.append({
            "role": chat["role"] if chat["role"] == "user" else "assistant",
            "content": chat["content"]
        })
    
    # Add current user message
    messages.append({"role": "user", "content": user_msg})
    
    data = {
        "model": selected_model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "top_p": 1,
        "frequency_penalty": 0,
        "presence_penalty": 0
    }
    
    try:
        with st.spinner("🤖 AI is thinking..."):
            response = requests.post(url, headers=headers, json=data, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            
            if "choices" in result and len(result["choices"]) > 0:
                ai_msg = result["choices"][0]["message"]["content"]
                return ai_msg
            else:
                return "⚠️ Error: No response received from AI model."
                
    except requests.exceptions.Timeout:
        return "⚠️ Error: Request timed out. Please try again."
    except requests.exceptions.RequestException as e:
        return f"⚠️ Network Error: {str(e)}"
    except KeyError as e:
        return f"⚠️ API Response Error: Missing key {str(e)}"
    except Exception as e:
        return f"⚠️ Unexpected Error: {str(e)}"

def format_chat_message(role: str, content: str) -> str:
    """Format chat message with appropriate styling"""
    if role == "user":
        emoji = "👤"
        css_class = "user-bubble"
    else:
        emoji = "🤖"
        css_class = "ai-bubble"
    
    # Escape HTML characters and preserve line breaks
    content = content.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    content = content.replace("\n", "<br>")
    
    return f'<div class="{css_class}">{emoji} {content}</div>'

# --- Display chat history ---
if st.session_state["chat_history"]:
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    for chat in st.session_state["chat_history"]:
        message_html = format_chat_message(chat["role"], chat["content"])
        st.markdown(message_html, unsafe_allow_html=True)
        st.markdown('<div class="clearfix"></div>', unsafe_allow_html=True)
    
    # Show typing indicator if AI is thinking
    if st.session_state["is_thinking"]:
        st.markdown('<div class="typing-indicator">🤖 AI is typing...</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.info("👋 Welcome! Start a conversation by typing a message below.")

# --- Input area ---
col1, col2 = st.columns([4, 1])

with col1:
    user_input = st.chat_input("Type your message here...")

with col2:
    if st.session_state["chat_history"]:
        st.metric(
            "Messages", 
            len(st.session_state["chat_history"]),
            help="Total messages in conversation"
        )

# --- Handle user input ---
if user_input and not st.session_state["is_thinking"]:
    # Add user message to history
    st.session_state["chat_history"].append({
        "role": "user", 
        "content": user_input,
        "timestamp": time.time()
    })
    
    # Set thinking state
    st.session_state["is_thinking"] = True
    
    # Rerun to show user message and typing indicator
    st.rerun()

# --- Get AI response (this runs after rerun) ---
if (st.session_state["is_thinking"] and 
    st.session_state["chat_history"] and 
    st.session_state["chat_history"][-1]["role"] == "user"):
    
    last_user_message = st.session_state["chat_history"][-1]["content"]
    
    # Get AI response
    ai_reply = get_ai_response(last_user_message, st.session_state["chat_history"][:-1])
    
    # Add AI response to history
    st.session_state["chat_history"].append({
        "role": "assistant", 
        "content": ai_reply,
        "timestamp": time.time()
    })
    
    # Reset thinking state
    st.session_state["is_thinking"] = False
    
    # Rerun to show AI response
    st.rerun()

# --- Footer ---
st.markdown("---")
st.markdown(
    "💡 **Tips:** Use the sidebar to configure the AI model, adjust creativity, "
    "and manage your chat history. Clear the chat or export it as needed."
)