import streamlit as st
import requests
import json

# --- Konfigurasi halaman ---
st.set_page_config(
    page_title="AI Bubble Chatbot",
    page_icon="🤖",
    layout="centered"
)

# --- CSS sederhana untuk chat bubbles ---
st.markdown("""
<style>
.user-message {
    background-color: #DCF8C6;
    padding: 10px 15px;
    border-radius: 20px 20px 5px 20px;
    margin: 10px 0;
    margin-left: 50px;
    color: #2E7D32;
    text-align: right;
}

.ai-message {
    background-color: #F1F0F0;
    padding: 10px 15px;
    border-radius: 20px 20px 20px 5px;
    margin: 10px 0;
    margin-right: 50px;
    color: #333;
}

.chat-container {
    max-height: 400px;
    overflow-y: auto;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 10px;
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

# --- Header ---
st.title("🤖 AI Bubble Chatbot")
st.write("Chatbot AI dengan antarmuka bubble chat yang menarik")

# --- Sidebar untuk konfigurasi ---
with st.sidebar:
    st.header("⚙️ Pengaturan")
    
    # Input API Key
    api_key = st.text_input(
        "OpenRouter API Key", 
        value="5f17568a859a518d007ea1b9039e9c2111bf758bec459f7bb4017cfeb80fe64e",
        type="password"
    )
    
    # Pilihan model
    model_options = [
        "mistralai/mistral-7b-instruct",
        "openai/gpt-3.5-turbo",
        "openai/gpt-4-turbo-preview"
    ]
    
    selected_model = st.selectbox("Pilih Model AI", model_options)
    
    # Pengaturan lain
    temperature = st.slider("Kreativitas Respons", 0.0, 2.0, 0.7, 0.1)
    max_tokens = st.number_input("Panjang Maksimal Respons", 50, 2000, 500)
    
    # Tombol clear chat
    if st.button("🗑️ Hapus Chat"):
        st.session_state.chat_history = []
        st.rerun()

# --- Inisialisasi session state ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- Fungsi untuk memanggil API ---
def get_ai_response(user_message):
    """Mendapatkan respons dari OpenRouter API"""
    
    if not api_key or len(api_key) < 10:
        return "❌ Error: API key tidak valid. Silakan masukkan API key yang benar di sidebar."
    
    url = "https://openrouter.ai/api/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # Buat context dari history chat
    messages = []
    for chat in st.session_state.chat_history[-5:]:  # Ambil 5 pesan terakhir
        if chat["role"] == "user":
            messages.append({"role": "user", "content": chat["content"]})
        else:
            messages.append({"role": "assistant", "content": chat["content"]})
    
    # Tambahkan pesan user saat ini
    messages.append({"role": "user", "content": user_message})
    
    data = {
        "model": selected_model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            if "choices" in result and len(result["choices"]) > 0:
                return result["choices"][0]["message"]["content"]
            else:
                return "❌ Error: Tidak ada respons dari AI"
        else:
            return f"❌ Error: HTTP {response.status_code} - {response.text}"
            
    except requests.exceptions.Timeout:
        return "❌ Error: Request timeout. Coba lagi."
    except requests.exceptions.RequestException as e:
        return f"❌ Error jaringan: {str(e)}"
    except Exception as e:
        return f"❌ Error tidak terduga: {str(e)}"

# --- Tampilkan riwayat chat ---
if st.session_state.chat_history:
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    for i, chat in enumerate(st.session_state.chat_history):
        if chat["role"] == "user":
            st.markdown(
                f'<div class="user-message">👤 <strong>Anda:</strong><br>{chat["content"]}</div>', 
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f'<div class="ai-message">🤖 <strong>AI:</strong><br>{chat["content"]}</div>', 
                unsafe_allow_html=True
            )
    
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.info("👋 Selamat datang! Mulai percakapan dengan mengetik pesan di bawah.")

# --- Input dari user ---
user_input = st.chat_input("Ketik pesan Anda di sini...")

# --- Proses input user ---
if user_input:
    # Tambahkan pesan user ke history
    st.session_state.chat_history.append({
        "role": "user",
        "content": user_input
    })
    
    # Tampilkan spinner saat mendapatkan respons AI
    with st.spinner("🤖 AI sedang berpikir..."):
        ai_response = get_ai_response(user_input)
    
    # Tambahkan respons AI ke history
    st.session_state.chat_history.append({
        "role": "assistant", 
        "content": ai_response
    })
    
    # Refresh halaman untuk menampilkan chat baru
    st.rerun()

# --- Info tambahan ---
if st.session_state.chat_history:
    st.sidebar.metric("Total Pesan", len(st.session_state.chat_history))

# --- Footer ---
st.markdown("---")
st.markdown("💡 **Tips:** Gunakan sidebar untuk mengatur model AI dan parameter lainnya.")