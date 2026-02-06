# ⚡ Quick Start Guide

Get your Face Attendance System running in 5 minutes!

## ✅ Checklist

- [ ] Python 3.8+ installed
- [ ] MySQL installed and running
- [ ] MySQL password known

---

## 🎯 Steps

### 1️⃣ Install Python Packages

```bash
cd face_attendance_backend
pip install -r requirements.txt
```

⏱️ *This takes 2-5 minutes (installing face-recognition)*

---

### 2️⃣ Setup Database

**A. Edit `setup_database.py`** - Change line 8:
```python
DB_PASS = "your_mysql_password"  # ← Put your MySQL password here
```

**B. Run setup:**
```bash
python setup_database.py
```

**C. Edit `config.py`** - Change line 7:
```python
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:your_mysql_password@localhost/face_attendance'
```

**D. Verify:**
```bash
python check_config.py
```

Should show: ✓ Database connection successful!

---

### 3️⃣ Start Backend

**Windows:** Double-click `run_backend.bat`

**OR Command line:**
```bash
python app.py
```

✅ You should see: `* Running on http://127.0.0.1:5000`

**Keep this window open!**

---

### 4️⃣ Open Frontend

**Option A:** Open `frontend/index.html` in Chrome/Edge

**Option B:** Run a server:
```bash
cd frontend
python -m http.server 8080
```
Then open: **http://localhost:8080**

---

## 🎉 You're Done!

1. **Register** a user (name, email, photo)
2. **Mark Attendance** (use camera or upload image)
3. **View Logs** to see attendance records

---

## ❌ Common Issues

| Problem | Solution |
|---------|----------|
| "Module not found" | Run `pip install -r requirements.txt` |
| "Can't connect to MySQL" | Check MySQL is running, verify password in `config.py` |
| "Database doesn't exist" | Run `python setup_database.py` |
| Frontend shows "Cannot reach server" | Make sure backend is running (step 3) |

---

**Need more help?** See `README.md` for detailed troubleshooting.
