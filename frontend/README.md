# Face Attendance – Frontend

Modern web interface for the Face Attendance System.

## 🚀 Quick Start

### Prerequisites
- Backend must be running on `http://localhost:5000`
- Modern browser (Chrome, Edge, Firefox)

### Running the Frontend

**Option 1: Direct File (Easiest)**
- Double-click `index.html` or drag it into your browser

**Option 2: Local Server (Recommended)**
```bash
cd frontend
python -m http.server 8080
```
Then open: **http://localhost:8080**

---

## 📱 Features

### Register Tab
- Enter user name and email
- Upload a clear face photo (one face per image)
- Real-time validation and feedback

### Mark Attendance Tab
- **Webcam Mode:** Click "Start camera" to use your webcam
- **File Upload:** Upload an image file instead
- Automatic face recognition and attendance marking

### Attendance Logs Tab
- View all attendance records
- Shows user name and timestamp
- Click "Refresh" to reload

---

## ⚙️ Configuration

### Change Backend URL

Edit `js/app.js` (line 4):
```javascript
const API_BASE = 'http://localhost:5000';  // Change port/host here
```

---

## 🐛 Troubleshooting

### "Cannot reach server"
- Make sure backend is running (check terminal)
- Verify backend URL in `js/app.js`
- Try opening `http://localhost:5000/health` directly

### Camera not working
- Grant camera permissions when prompted
- Use "Upload image" as alternative
- Check browser console (F12) for errors

### Face not recognized
- Ensure user is registered first
- Use clear, front-facing photos
- Good lighting helps recognition

---

## 📁 Files

- `index.html` - Main page structure
- `css/styles.css` - Styling and theme
- `js/app.js` - Frontend logic and API calls

---

**For complete setup instructions, see the main `README.md` in the project root.**
