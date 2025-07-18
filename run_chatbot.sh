#!/bin/bash

# Script untuk menjalankan AI Chatbot
echo "🤖 Memulai AI Bubble Chatbot..."

# Aktifkan virtual environment
source chatbot_env/bin/activate

# Jalankan Streamlit app
echo "📱 Aplikasi akan terbuka di: http://localhost:8501"
echo "⭐ Tekan Ctrl+C untuk menghentikan aplikasi"
echo ""

streamlit run chatbot_app.py --server.port 8501 --server.address 0.0.0.0