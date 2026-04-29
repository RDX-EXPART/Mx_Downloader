# 🎬 DsrBotzz MX Player Downloader Bot

A powerful Telegram bot to download MX Player / MXPlay videos in any available quality using **N_m3u8DL-RE** and **Yt-dlp**.

---

## 📌 About

This repository is a **fork** of the Anonymous DK Project.  
**Original Repository:** [DKBOTZPROJECT/MX-Player-Downloader-Bot](https://github.com/DKBOTZPROJECT/MX-Player-Downloader-Bot/tree/DKBOTZ)

---

## ✨ Features

- 🎥 **Multi-Quality Support** – Download videos in 1080p, 720p, 480p, 360p, and more
- ⚡ **Fast Downloads** – Powered by N_m3u8DL-RE for HLS/DASH streams
- 📊 **Real-Time Progress** – Live progress bar with speed and ETA
- 🗄️ **MongoDB Integration** – Track users and download statistics
- 🔒 **Secure & Private** – No data logging or sharing
- 🌐 **API-Based Resolution** – Automatic m3u8/mpd link extraction

---

## 📁 Project Structure

```
mxbot/
├── bot.py              # Main entry point — app.run()
├── config.py           # Environment variable configuration
├── database.py         # MongoDB (Motor async) helper functions
├── helpers.py          # API calls + N_m3u8DL-RE download logic
├── requirements.txt    # Python dependencies
└── plugins/
    ├── commands.py     # /start, /help, /stats commands
    └── downloader.py   # Link handler + quality picker + download/upload
```

---

## ⚙️ Installation & Setup

### 1️⃣ Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 2️⃣ Install N_m3u8DL-RE
Download the latest release from: [N_m3u8DL-RE Releases](https://github.com/nilaoda/N_m3u8DL-RE/releases)

**Linux / macOS:**
```bash
chmod +x N_m3u8DL-RE
sudo mv N_m3u8DL-RE /usr/local/bin/
```

**Windows:**
- Extract and add to your system PATH

**Verify Installation:**
```bash
N_m3u8DL-RE --version
```

### 3️⃣ Configure Environment Variables
Create a `.env` file or set these variables:

```bash
API_ID=your_api_id              # Get from my.telegram.org
API_HASH=your_api_hash          # Get from my.telegram.org
BOT_TOKEN=your_bot_token        # Get from @BotFather
MONGO_URI=mongodb://localhost:27017  # Or MongoDB Atlas URI
DB_NAME=dsrbotz_mx              # Database name
```

**Optional Variables:**
```bash
OWNER_ID=your_telegram_user_id  # For admin commands
LOG_CHANNEL=-100xxxxxxxxxx      # Log channel ID
```

### 4️⃣ Run The Bot
```bash
python bot.py
```

---

## 🔄 How It Works

1. **User sends MX Player link** → `https://www.mxplayer.in/show/xyz`
2. **Bot resolves media** → Calls API: `https://ott.dkbotzpro.in/mxplayer?url=...`
3. **Quality detection** → Runs `N_m3u8DL-RE --list-all` to fetch available qualities
4. **User selection** → Inline buttons: `🎬 1080p [1920x1080]`, `🎬 720p`, etc.
5. **Download & Upload** → Real-time progress bar with speed/ETA displayed

---

## 🗄️ Database Schema

| Collection  | Fields                          | Purpose                          |
|-------------|---------------------------------|----------------------------------|
| `users`     | `user_id`, `username`, `joined` | Track user registrations         |
| `downloads` | `user_id`, `quality`, `size`, `date` | Log download history      |

---

## 📦 Dependencies

| Package        | Purpose                              |
|----------------|--------------------------------------|
| `hydrogram`    | Telegram MTProto client (Pyrogram fork) |
| `TgCrypto`     | Speed boost for Pyrogram encryption  |
| `motor`        | Async MongoDB driver                 |
| `aiohttp`      | Async HTTP requests                  |
| `yt-dlp`       | Fallback for some streams            |
| `pymongo`      | MongoDB operations                   |

---

## 🛠️ Commands

| Command    | Description                          |
|------------|--------------------------------------|
| `/start`   | Start the bot and see welcome message |
| `/help`    | Show usage instructions              |
| `/stats`   | View bot statistics (Admin only)     |

---

## 👥 Credits

- **Anonymous** – Original concept
- **DK** – Core development
- **Shivam** – Contributions
- **Hydrogram** – Telegram client library
- **N_m3u8DL-RE** – HLS/DASH downloader
- **Yt-dlp** – Universal media downloader

---

## 📜 License

This project is licensed under the **MIT License**.  
Feel free to modify and distribute with proper attribution.

---

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📞 Support

For issues or questions:
- Open an [Issue](https://github.com/DKNS-LABS/mx_downloader/issues)
- Contact via Telegram: [Dkns-lab](https://t.me/DknsLabSupport)

---

## ⚠️ Disclaimer

This bot is for **educational purposes only**. Users are responsible for complying with MX Player's Terms of Service and applicable copyright laws. The developers are not liable for misuse.

---

**Made with ❤️ by DsrBotzz**
