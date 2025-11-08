# 🚀 LoanIQ Quick Start Guide

**Get your app running in 2 minutes!**

---

## ⚡ Super Fast Start

### **Option 1: One-Click Start** (Recommended)

1. Double-click this file:
   ```
   START_ALL_SERVICES.bat
   ```

2. Wait 10 seconds for both services to start

3. Open browser:
   ```
   http://localhost:3000
   ```

4. Done! 🎉

---

### **Option 2: Manual Start**

**Terminal 1 - Backend:**
```bash
cd C:\Lab3\Lab3
python -m uvicorn api.main:app --reload
```

**Terminal 2 - Frontend:**
```bash
cd C:\Lab3\Lab3\frontend
npm run dev
```

**Wait 10 seconds, then visit:**
```
http://localhost:3000
```

---

## 🧪 Test the Integration

### **1. Upload a Document**
1. Go to: `http://localhost:3000/chat`
2. Click the 📎 button
3. Select any PDF file
4. Watch the progress bar
5. See confetti! 🎊

### **2. Chat with AI**
1. After upload, type a question
2. Example: "What is my interest rate?"
3. Press Enter or click Send
4. Get instant AI response

### **3. Try Suggested Prompts**
- Click any of the 4 suggested questions
- See AI provide detailed answers

---

## ✅ What Should Work

✅ **Landing Page** (`/`)
- Clean OpenAI-style design
- Animated gradient text
- Demo preview
- Feature cards

✅ **Chat Interface** (`/chat`)
- Document upload
- Real-time progress
- Confetti celebration
- AI conversations
- Charts display

✅ **API Integration**
- Backend on port 8000
- Frontend on port 3000
- CORS enabled
- Error handling active

---

## ❌ Troubleshooting

### **Backend won't start?**

**Check Python:**
```bash
python --version
```
Should be 3.8+

**Install dependencies:**
```bash
cd C:\Lab3\Lab3
pip install -r requirements.txt
```

### **Frontend won't start?**

**Check Node:**
```bash
node --version
```
Should be 16+

**Install dependencies:**
```bash
cd C:\Lab3\Lab3\frontend
npm install
```

### **Can't upload files?**

1. Check backend is running: `http://localhost:8000/health`
2. Check browser console for errors
3. Try a different PDF file
4. Restart both services

---

## 📚 More Information

- **Full Integration Guide**: `INTEGRATION_GUIDE.md`
- **Frontend Redesign**: `OPENAI_REDESIGN_COMPLETE.md`
- **API Documentation**: `http://localhost:8000/docs`

---

## 🎯 Quick Links

| Service | URL | Purpose |
|---------|-----|---------|
| **Frontend** | http://localhost:3000 | Main app |
| **Chat** | http://localhost:3000/chat | ChatGPT interface |
| **Backend API** | http://localhost:8000 | REST API |
| **API Docs** | http://localhost:8000/docs | Swagger UI |
| **Health Check** | http://localhost:8000/health | Status |

---

**Ready? Start the services and visit http://localhost:3000!** 🚀
