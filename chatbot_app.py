import streamlit as st
import requests
import json
import time
import uuid
from datetime import datetime
from typing import List, Dict, Optional
import os

# --- Page Configuration ---
st.set_page_config(
    page_title="AI Chatbot - OpenRouter",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS for Modern UI ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .main {
        font-family: 'Inter', sans-serif;
        padding-top: 1rem;
    }
    
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 12px 16px;
        border-radius: 18px 18px 4px 18px;
        margin: 8px 0 8px auto;
        max-width: 80%;
        box-shadow: 0 2px 10px rgba(102, 126, 234, 0.3);
        float: right;
        clear: both;
        word-wrap: break-word;
    }
    
    .assistant-message {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 12px 16px;
        border-radius: 18px 18px 18px 4px;
        margin: 8px auto 8px 0;
        max-width: 80%;
        box-shadow: 0 2px 10px rgba(240, 147, 251, 0.3);
        float: left;
        clear: both;
        word-wrap: break-word;
    }
    
    .chat-container {
        height: 500px;
        overflow-y: auto;
        padding: 20px;
        background: linear-gradient(to bottom, #ffecd2 0%, #fcb69f 100%);
        border-radius: 15px;
        margin-bottom: 20px;
        box-shadow: inset 0 2px 10px rgba(0,0,0,0.1);
    }
    
    .conversation-item {
        background: white;
        padding: 12px;
        margin: 8px 0;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    
    .conversation-item:hover {
        transform: translateX(5px);
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .conversation-title {
        font-weight: 600;
        color: #333;
        margin-bottom: 4px;
    }
    
    .conversation-preview {
        color: #666;
        font-size: 0.85em;
        overflow: hidden;
        white-space: nowrap;
        text-overflow: ellipsis;
    }
    
    .conversation-date {
        color: #999;
        font-size: 0.75em;
        margin-top: 4px;
    }
    
    .typing-indicator {
        background: rgba(255,255,255,0.9);
        padding: 12px 16px;
        border-radius: 18px;
        margin: 8px auto 8px 0;
        color: #666;
        font-style: italic;
        animation: pulse 1.5s infinite;
        float: left;
        clear: both;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    
    @keyframes pulse {
        0% { opacity: 0.6; }
        50% { opacity: 1; }
        100% { opacity: 0.6; }
    }
    
    .clearfix::after {
        content: "";
        display: table;
        clear: both;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 10px 20px;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }
    
    .api-status {
        padding: 10px;
        border-radius: 8px;
        margin: 10px 0;
        text-align: center;
        font-weight: 500;
    }
    
    .api-connected {
        background: #d4edda;
        color: #155724;
        border: 1px solid #c3e6cb;
    }
    
    .api-disconnected {
        background: #f8d7da;
        color: #721c24;
        border: 1px solid #f5c6cb;
    }
    </style>
""", unsafe_allow_html=True)

# --- Data Management Functions ---
def save_conversations():
    """Save conversations to local storage"""
    if "conversations" in st.session_state:
        # In a real app, you'd save to a database or file
        # For now, we'll keep it in session state
        pass

def load_conversations():
    """Load conversations from local storage"""
    if "conversations" not in st.session_state:
        st.session_state.conversations = {}
    if "current_conversation_id" not in st.session_state:
        st.session_state.current_conversation_id = None

def create_new_conversation():
    """Create a new conversation"""
    conversation_id = str(uuid.uuid4())
    st.session_state.conversations[conversation_id] = {
        "id": conversation_id,
        "title": "New Conversation",
        "messages": [],
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }
    st.session_state.current_conversation_id = conversation_id
    return conversation_id

def get_current_conversation():
    """Get the current conversation"""
    if st.session_state.current_conversation_id:
        return st.session_state.conversations.get(st.session_state.current_conversation_id)
    return None

def update_conversation_title(conversation_id, title):
    """Update conversation title based on first message"""
    if conversation_id in st.session_state.conversations:
        st.session_state.conversations[conversation_id]["title"] = title[:50] + "..." if len(title) > 50 else title
        st.session_state.conversations[conversation_id]["updated_at"] = datetime.now().isoformat()

def add_message_to_conversation(conversation_id, role, content):
    """Add a message to the conversation"""
    if conversation_id in st.session_state.conversations:
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        }
        st.session_state.conversations[conversation_id]["messages"].append(message)
        st.session_state.conversations[conversation_id]["updated_at"] = datetime.now().isoformat()
        
        # Update title if this is the first user message
        if role == "user" and len(st.session_state.conversations[conversation_id]["messages"]) == 1:
            update_conversation_title(conversation_id, content)

# --- API Functions ---
@st.cache_data(ttl=300)
def validate_api_key(api_key: str) -> bool:
    """Validate OpenRouter API key"""
    if not api_key or len(api_key) < 20:
        return False
    
    try:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        # Test with a simple request
        response = requests.get(
            "https://openrouter.ai/api/v1/models",
            headers=headers,
            timeout=10
        )
        return response.status_code == 200
    except:
        return False

def get_ai_response(user_message: str, conversation_history: List[Dict], api_key: str, model: str, temperature: float, max_tokens: int) -> str:
    """Get AI response from OpenRouter"""
    url = "https://openrouter.ai/api/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:8501",
        "X-Title": "AI Chatbot"
    }
    
    # Prepare messages for API
    messages = []
    for msg in conversation_history[-10:]:  # Last 10 messages for context
        messages.append({
            "role": msg["role"],
            "content": msg["content"]
        })
    
    messages.append({"role": "user", "content": user_message})
    
    data = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "stream": False
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=60)
        response.raise_for_status()
        
        result = response.json()
        
        if "choices" in result and len(result["choices"]) > 0:
            return result["choices"][0]["message"]["content"]
        else:
            return "❌ Error: No response from AI model"
            
    except requests.exceptions.Timeout:
        return "❌ Error: Request timeout. Please try again."
    except requests.exceptions.RequestException as e:
        return f"❌ Network Error: {str(e)}"
    except Exception as e:
        return f"❌ Unexpected Error: {str(e)}"

# --- Initialize App ---
load_conversations()

# --- Sidebar ---
with st.sidebar:
    st.title("🤖 AI Chatbot")
    st.markdown("---")
    
    # API Configuration
    st.subheader("🔑 API Configuration")
    
    api_key = st.text_input(
        "OpenRouter API Key",
        type="password",
        help="Get your free API key from https://openrouter.ai/",
        placeholder="sk-or-v1-..."
    )
    
    # API Status
    if api_key:
        if validate_api_key(api_key):
            st.markdown('<div class="api-status api-connected">✅ API Connected</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="api-status api-disconnected">❌ Invalid API Key</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="api-status api-disconnected">⚠️ No API Key Provided</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Model Configuration
    st.subheader("⚙️ Model Settings")
    
    model_options = [
        "mistralai/mistral-7b-instruct:free",
        "microsoft/phi-3-mini-128k-instruct:free",
        "google/gemma-2-9b-it:free",
        "meta-llama/llama-3.1-8b-instruct:free",
        "openai/gpt-3.5-turbo",
        "openai/gpt-4o-mini",
        "anthropic/claude-3-haiku"
    ]
    
    selected_model = st.selectbox(
        "AI Model",
        model_options,
        index=0,
        help="Free models have ':free' suffix"
    )
    
    temperature = st.slider(
        "Creativity",
        min_value=0.0,
        max_value=2.0,
        value=0.7,
        step=0.1,
        help="Higher = more creative"
    )
    
    max_tokens = st.number_input(
        "Max Response Length",
        min_value=50,
        max_value=2000,
        value=800,
        step=50
    )
    
    st.markdown("---")
    
    # Conversation Management
    st.subheader("💬 Conversations")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("➕ New Chat", use_container_width=True):
            create_new_conversation()
            st.rerun()
    
    with col2:
        if st.button("🗑️ Clear All", use_container_width=True):
            st.session_state.conversations = {}
            st.session_state.current_conversation_id = None
            st.rerun()
    
    # Conversation History
    if st.session_state.conversations:
        st.markdown("**Recent Conversations:**")
        
        # Sort conversations by updated_at
        sorted_conversations = sorted(
            st.session_state.conversations.values(),
            key=lambda x: x["updated_at"],
            reverse=True
        )
        
        for conv in sorted_conversations:
            is_current = conv["id"] == st.session_state.current_conversation_id
            
            # Create conversation preview
            preview = "New conversation"
            if conv["messages"]:
                first_message = conv["messages"][0]["content"]
                preview = first_message[:50] + "..." if len(first_message) > 50 else first_message
            
            # Format date
            try:
                date_obj = datetime.fromisoformat(conv["updated_at"])
                date_str = date_obj.strftime("%m/%d %H:%M")
            except:
                date_str = "Recent"
            
            # Create clickable conversation item
            if st.button(
                f"{'🔵' if is_current else '⚪'} {conv['title'][:30]}",
                help=f"{preview}\n{date_str}",
                use_container_width=True,
                key=f"conv_{conv['id']}"
            ):
                st.session_state.current_conversation_id = conv["id"]
                st.rerun()

# --- Main Chat Interface ---
st.title("🤖 AI Chatbot with OpenRouter")

# Check if we have a current conversation
current_conv = get_current_conversation()
if not current_conv:
    # Create first conversation
    create_new_conversation()
    current_conv = get_current_conversation()

# Display current conversation title
if current_conv:
    st.subheader(f"💬 {current_conv['title']}")

# Chat display container
chat_container = st.container()

with chat_container:
    if current_conv and current_conv["messages"]:
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        
        for message in current_conv["messages"]:
            role = message["role"]
            content = message["content"]
            
            if role == "user":
                st.markdown(f'<div class="user-message">👤 {content}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="assistant-message">🤖 {content}</div>', unsafe_allow_html=True)
            st.markdown('<div class="clearfix"></div>', unsafe_allow_html=True)
        
        # Show typing indicator if AI is responding
        if "is_generating" in st.session_state and st.session_state.is_generating:
            st.markdown('<div class="typing-indicator">🤖 AI is thinking...</div>', unsafe_allow_html=True)
            st.markdown('<div class="clearfix"></div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("👋 Welcome! Start a new conversation by typing a message below.")

# Input area
st.markdown("---")
user_input = st.chat_input(
    "Type your message here...", 
    disabled=not api_key or not validate_api_key(api_key)
)

# Handle user input
if user_input and api_key and validate_api_key(api_key):
    if not current_conv:
        create_new_conversation()
        current_conv = get_current_conversation()
    
    # Add user message
    add_message_to_conversation(
        st.session_state.current_conversation_id,
        "user",
        user_input
    )
    
    # Set generating state
    st.session_state.is_generating = True
    st.rerun()

# Generate AI response
if ("is_generating" in st.session_state and 
    st.session_state.is_generating and 
    current_conv and 
    current_conv["messages"] and 
    current_conv["messages"][-1]["role"] == "user"):
    
    with st.spinner("🤖 Generating response..."):
        ai_response = get_ai_response(
            current_conv["messages"][-1]["content"],
            current_conv["messages"][:-1],
            api_key,
            selected_model,
            temperature,
            max_tokens
        )
    
    # Add AI response
    add_message_to_conversation(
        st.session_state.current_conversation_id,
        "assistant",
        ai_response
    )
    
    # Reset generating state
    st.session_state.is_generating = False
    save_conversations()
    st.rerun()

# Footer
st.markdown("---")
st.markdown(
    """
    **💡 Tips:**
    - Get your free API key from [OpenRouter](https://openrouter.ai/)
    - Models with ':free' suffix are completely free to use
    - Use the sidebar to start new conversations and manage chat history
    - Your conversations are saved in this session
    """
)

# Display conversation stats
if current_conv:
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Messages", len(current_conv["messages"]))
    with col2:
        user_msgs = len([m for m in current_conv["messages"] if m["role"] == "user"])
        st.metric("Your Messages", user_msgs)
    with col3:
        ai_msgs = len([m for m in current_conv["messages"] if m["role"] == "assistant"])
        st.metric("AI Responses", ai_msgs)