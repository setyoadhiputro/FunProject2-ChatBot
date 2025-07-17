# 🤖 AI Bubble Chatbot

A modern, interactive chatbot built with Streamlit and powered by OpenRouter API. Features a beautiful bubble chat interface with support for multiple AI models.

## ✨ Features

- **Modern Bubble Chat Interface**: WhatsApp-style chat bubbles with smooth animations
- **Multiple AI Models**: Support for GPT-3.5, GPT-4, Claude, Mistral, and Gemini
- **Configurable Settings**: Adjust creativity, response length, and model selection
- **Chat Management**: Clear chat history and export conversations
- **Real-time Typing Indicators**: Visual feedback when AI is responding
- **Conversation Context**: Maintains context across multiple messages
- **Error Handling**: Robust error handling with user-friendly messages

## 🚀 Quick Start

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Get OpenRouter API Key**:
   - Visit [OpenRouter.ai](https://openrouter.ai/)
   - Create an account and get your API key

3. **Run the Application**:
   ```bash
   streamlit run chatbot_app.py
   ```

4. **Configure Settings**:
   - Enter your API key in the sidebar
   - Select your preferred AI model
   - Adjust creativity and response length as needed

## 🎯 Usage

1. **Start Chatting**: Type your message in the input box at the bottom
2. **Customize Experience**: Use the sidebar to:
   - Change AI models
   - Adjust response creativity (temperature)
   - Set maximum response length
3. **Manage Chat**: 
   - Clear conversation history
   - Export chat as JSON file
4. **Monitor**: View message count and conversation metrics

## 🔧 Configuration Options

### AI Models
- **Mistral 7B**: Fast, efficient responses
- **GPT-3.5 Turbo**: Balanced performance and cost
- **GPT-4**: Advanced reasoning capabilities
- **Claude 3 Sonnet**: High-quality conversational AI
- **Gemini Pro**: Google's latest language model

### Settings
- **Response Creativity**: 0.0 (focused) to 2.0 (creative)
- **Max Response Length**: 50 to 4000 tokens
- **Context Window**: Maintains last 10 messages for context

## 📁 File Structure

```
├── chatbot_app.py      # Main application file
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## 🛠️ Technical Details

- **Framework**: Streamlit 1.28+
- **API**: OpenRouter (supports multiple AI providers)
- **Styling**: Custom CSS with gradient bubbles and animations
- **State Management**: Streamlit session state for chat history
- **Error Handling**: Comprehensive exception handling for network issues

## 🎨 Customization

The app uses custom CSS for styling. You can modify the bubble colors, animations, and layout by editing the CSS in the `st.markdown()` section of `chatbot_app.py`.

## 📝 License

This project is open source. Feel free to modify and distribute as needed.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.