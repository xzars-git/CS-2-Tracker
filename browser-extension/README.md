# CS2 Tracker Browser Extension

🚀 **One-click auto-import** your Steam Market history into CS2 Trading Tracker!

## Features

✅ **Auto-extract** Steam cookies (no manual copy-paste)  
✅ **One-click import** - just enter your User ID  
✅ **Saves your settings** for next time  
✅ **Beautiful UI** with gradient design  
✅ **Secure** - cookies sent only to localhost:8000  

---

## Installation

### Chrome / Edge / Brave

1. **Download the extension:**
   - The extension is in: `d:\CS 2 Tracker\browser-extension`

2. **Open Extensions page:**
   - Chrome: Go to `chrome://extensions/`
   - Edge: Go to `edge://extensions/`
   - Brave: Go to `brave://extensions/`

3. **Enable Developer Mode:**
   - Toggle the "Developer mode" switch (top right)

4. **Load the extension:**
   - Click "Load unpacked"
   - Select the folder: `d:\CS 2 Tracker\browser-extension`
   - Extension will appear!

5. **Pin the extension:**
   - Click the puzzle icon (Extensions)
   - Find "CS2 Tracker - Auto Import"
   - Click the pin icon to keep it visible

---

### Firefox

1. **Open about:debugging**
   - Type `about:debugging` in address bar

2. **Load Temporary Add-on:**
   - Click "This Firefox" → "Load Temporary Add-on"
   - Navigate to `d:\CS 2 Tracker\browser-extension`
   - Select `manifest.json`

---

## How to Use

1. **Get your User ID:**
   - Login to CS2 Tracker at http://localhost:8000
   - Your URL will be: `localhost:8000?user_id=123`
   - Copy the number after `user_id=`

2. **Open Steam Market:**
   - Go to https://steamcommunity.com/market/
   - Make sure you're logged in

3. **Click the extension icon:**
   - Enter your User ID
   - Click "📥 Auto-Import Market History"
   - Wait for success message!

4. **Check your tracker:**
   - Go back to http://localhost:8000
   - Refresh page
   - All transactions imported! 🎉

---

## How It Works

```
Steam Market (logged in)
    ↓
Browser Extension
    ↓
Auto-extracts cookies:
- sessionid
- steamLoginSecure
- steamCountry
    ↓
Sends to localhost:8000/api/import/steam-market
    ↓
Backend fetches market history
    ↓
Transactions imported!
```

---

## Troubleshooting

### "Could not extract Steam cookies"
- Make sure you're logged into Steam
- Visit https://steamcommunity.com/market/ first
- Try refreshing the page

### "Import failed"
- Make sure CS2 Tracker backend is running (localhost:8000)
- Check your User ID is correct
- Check browser console for errors

### Extension not loading
- Make sure Developer Mode is enabled
- Check manifest.json exists in the folder
- Try reloading the extension

---

## Security

⚠️ **Your cookies are safe:**
- Extension only sends cookies to `localhost:8000` (your own computer)
- No external servers
- No data collection
- Open source - check the code!

---

## Next Steps

Once installed, you can:
1. **Set auto-import**: Extension can auto-import on page load
2. **Schedule imports**: Set up automatic daily imports
3. **Multi-account**: Save multiple user IDs

Enjoy! 🎮💰
