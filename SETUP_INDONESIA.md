# 🤖 Panduan Setup AI Bubble Chatbot

Panduan lengkap untuk menjalankan AI Bubble Chatbot di sistem Anda.

## 📋 Persyaratan Sistem

- Python 3.8 atau lebih baru
- pip (Python package manager)
- Koneksi internet
- API Key OpenRouter (gratis di [OpenRouter.ai](https://openrouter.ai/))

## 🚀 Cara Install & Menjalankan

### Opsi 1: Menggunakan Script Otomatis
```bash
./run_chatbot.sh
```

### Opsi 2: Manual Setup
```bash
# 1. Buat virtual environment
python3 -m venv chatbot_env

# 2. Aktifkan virtual environment
source chatbot_env/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Jalankan aplikasi
streamlit run chatbot_app.py
```

## 🔑 Mendapatkan API Key

1. **Kunjungi**: [OpenRouter.ai](https://openrouter.ai/)
2. **Daftar/Login** dengan akun Google atau email
3. **Buka Dashboard** → **Keys** 
4. **Buat API Key** baru
5. **Salin API Key** yang diberikan

## ⚙️ Konfigurasi

1. **Buka aplikasi** di browser: `http://localhost:8501`
2. **Masukkan API Key** di sidebar kiri
3. **Pilih Model AI** yang diinginkan:
   - **Mistral 7B**: Cepat dan efisien
   - **GPT-3.5 Turbo**: Seimbang dan murah
   - **GPT-4**: Kualitas tinggi
4. **Atur parameter**:
   - **Kreativitas**: 0.0 (fokus) hingga 2.0 (kreatif)
   - **Panjang Respons**: 50-2000 token

## 🎯 Fitur Utama

### ✨ Antarmuka Chat Bubble
- Desain modern mirip WhatsApp
- Bubble chat yang responsif
- Animasi smooth

### 🤖 Multiple AI Models
- Mendukung berbagai model AI terpopuler
- Mudah ganti model sesuai kebutuhan
- Performa optimal untuk setiap model

### 🛠️ Konfigurasi Fleksibel
- Atur tingkat kreativitas AI
- Kontrol panjang respons
- Simpan dan ekspor riwayat chat

### 📊 Manajemen Chat
- Hapus riwayat percakapan
- Ekspor chat ke file JSON
- Counter jumlah pesan

## 🔧 Troubleshooting

### Masalah: Aplikasi tidak bisa diakses
**Solusi:**
```bash
# Cek apakah Streamlit berjalan
ps aux | grep streamlit

# Restart aplikasi
./run_chatbot.sh
```

### Masalah: Error "Module not found"
**Solusi:**
```bash
# Pastikan virtual environment aktif
source chatbot_env/bin/activate

# Install ulang dependencies
pip install -r requirements.txt
```

### Masalah: API Key tidak valid
**Solusi:**
1. Pastikan API Key disalin dengan benar
2. Cek apakah API Key masih aktif di OpenRouter
3. Coba buat API Key baru

### Masalah: Respons AI lambat
**Solusi:**
1. Ganti ke model yang lebih cepat (Mistral 7B)
2. Kurangi panjang maksimal respons
3. Cek koneksi internet

## 📁 Struktur File

```
├── chatbot_app.py          # Aplikasi utama Streamlit
├── requirements.txt        # Dependencies Python
├── run_chatbot.sh         # Script untuk menjalankan app
├── README.md              # Dokumentasi bahasa Inggris
├── SETUP_INDONESIA.md     # Panduan ini
└── chatbot_env/           # Virtual environment
```

## 🎨 Kustomisasi

### Mengubah Warna Bubble Chat
Edit file `chatbot_app.py` pada bagian CSS:
```python
.user-message {
    background-color: #DCF8C6;  # Warna bubble user
    ...
}

.ai-message {
    background-color: #F1F0F0;  # Warna bubble AI
    ...
}
```

### Menambah Model AI Baru
Tambahkan di `model_options`:
```python
model_options = [
    "mistralai/mistral-7b-instruct",
    "openai/gpt-3.5-turbo",
    "model-baru-anda"  # Tambah di sini
]
```

## 💡 Tips Penggunaan

1. **Mulai dengan model Mistral** untuk testing (lebih murah)
2. **Atur kreativitas 0.7** untuk respons seimbang
3. **Gunakan panjang respons 500-1000** token untuk optimal
4. **Ekspor chat penting** sebelum clear history
5. **Monitor penggunaan API** di dashboard OpenRouter

## 🆘 Bantuan Lebih Lanjut

- **GitHub Issues**: [Link ke repository]
- **OpenRouter Docs**: [docs.openrouter.ai](https://docs.openrouter.ai/)
- **Streamlit Docs**: [docs.streamlit.io](https://docs.streamlit.io/)

## 📝 Changelog

### v1.0.0
- ✅ Antarmuka bubble chat
- ✅ Multiple AI models
- ✅ Konfigurasi sidebar
- ✅ Export/import chat
- ✅ Error handling yang robust

---

**Selamat menggunakan AI Bubble Chatbot! 🎉**