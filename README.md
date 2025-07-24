# 🤖 AI Chatbot with OpenRouter

A modern, user-friendly chatbot application built with Streamlit and powered by OpenRouter's free AI models. This application provides a chat interface similar to popular messaging apps with conversation management features.

## ✨ Features

### 🎨 User Interface
- **Modern Design**: Clean, gradient-based UI with smooth animations
- **Chat Bubbles**: WhatsApp-style message bubbles for natural conversation flow
- **Responsive Layout**: Works well on different screen sizes
- **Real-time Typing Indicators**: Shows when AI is generating responses

### 💬 Conversation Management
- **Multiple Conversations**: Create and manage multiple chat sessions
- **Conversation History**: All conversations are saved and accessible from the sidebar
- **Conversation Titles**: Auto-generated titles based on the first message
- **Easy Navigation**: Switch between conversations with a single click
- **Clear Options**: Clear individual conversations or all at once

### 🔧 Customization
- **Multiple AI Models**: Choose from various free and paid AI models
- **Adjustable Creativity**: Control response creativity with temperature slider
- **Response Length**: Set maximum response length
- **Real-time Configuration**: All settings apply immediately

### 🔑 API Integration
- **OpenRouter Support**: Uses OpenRouter API for access to multiple AI models
- **Free Models Available**: Several completely free models to choose from
- **API Key Validation**: Real-time validation of your API key
- **Error Handling**: Comprehensive error handling with user-friendly messages

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Installation

1. **Clone or download this repository**
   ```bash
   git clone <repository-url>
   cd ai-chatbot-openrouter
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Get your OpenRouter API Key**
   - Visit [OpenRouter](https://openrouter.ai/)
   - Sign up for a free account
   - Get your API key from the dashboard
   - Free models available without payment!

4. **Run the application**
   ```bash
   # Option 1: Using the launcher script (recommended)
   python3 run_chatbot.py
   
   # Option 2: Direct Streamlit command
   streamlit run chatbot_app.py
   ```

5. **Open your browser**
   - The app will automatically open at `http://localhost:8501`
   - Enter your OpenRouter API key in the sidebar
   - Start chatting!

## 🎯 How to Use

### Getting Started
1. **Enter API Key**: Paste your OpenRouter API key in the sidebar
2. **Choose Model**: Select from available AI models (free models marked with `:free`)
3. **Start Chatting**: Type your message in the input box at the bottom
4. **Manage Conversations**: Use sidebar buttons to create new chats or clear history

### Sidebar Features
- **🔑 API Configuration**: Enter and validate your OpenRouter API key
- **⚙️ Model Settings**: Choose AI model, adjust creativity, and set response length
- **💬 Conversations**: Create new chats, view conversation history, and clear chats
- **📊 Status Indicators**: See API connection status and conversation statistics

### Free Models Available
- `mistralai/mistral-7b-instruct:free` - Fast and efficient
- `microsoft/phi-3-mini-128k-instruct:free` - Great for coding
- `google/gemma-2-9b-it:free` - Balanced performance
- `meta-llama/llama-3.1-8b-instruct:free` - High quality responses

## 🛠️ Technical Details

### Built With
- **Streamlit**: Modern web app framework for Python
- **OpenRouter API**: Access to multiple AI models through one API
- **Custom CSS**: Beautiful, responsive design with gradients and animations
- **Python**: Backend logic and API integration

### Key Components
- **Conversation Management**: UUID-based conversation tracking
- **Message Storage**: In-memory storage with session state
- **API Integration**: Robust OpenRouter API integration with error handling
- **UI Components**: Custom CSS for modern chat interface

### File Structure
```
├── chatbot_app.py          # Main application file
├── run_chatbot.py          # Application launcher script
├── requirements.txt        # Python dependencies
└── README.md              # Documentation
```

## 🔧 Configuration Options

### Model Settings
- **AI Model**: Choose from 7+ available models
- **Creativity (Temperature)**: 0.0 (focused) to 2.0 (creative)
- **Max Response Length**: 50 to 2000 tokens

### Conversation Features
- **Auto-save**: Conversations automatically saved
- **Quick Access**: Recent conversations in sidebar
- **Smart Titles**: Auto-generated from first message
- **Message Count**: Track conversation statistics

## 🆓 Free Usage

This application is designed to work with OpenRouter's free tier:
- **Free Models**: Several models available at no cost
- **No Credit Card**: Create account without payment info
- **Generous Limits**: Suitable for personal use and testing
- **Easy Upgrade**: Paid models available when needed

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests
- Improve documentation

## 📝 License

This project is open source and available under the MIT License.

## 🆘 Support

If you encounter any issues:
1. Check your OpenRouter API key is valid
2. Ensure you have internet connection
3. Try refreshing the page
4. Check the console for error messages

## 🔗 Useful Links

- [OpenRouter](https://openrouter.ai/) - Get your free API key
- [Streamlit Documentation](https://docs.streamlit.io/) - Learn more about Streamlit
- [OpenRouter Models](https://openrouter.ai/models) - Browse available AI models

---

**Happy Chatting! 🚀**
