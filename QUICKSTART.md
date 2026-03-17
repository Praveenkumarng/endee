# Quick Start Guide

Get the Cotton Leaf Disease Detection System running in minutes!

## 🚀 Prerequisites

- Python 3.10+
- Node.js 18+
- [Endee Vector Database](https://github.com/endee-io/endee) running locally (port 8080)
- OpenAI API Key (for RAG Expert Chat)
- GPU with CUDA (optional, for faster inference)
- 8GB+ RAM

## ⚡ Quick Setup (5 Minutes)

### Step 1: Backend Setup

```bash
# Navigate to backend
cd E:\NTR\cotton-disease-detection\backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt
pip install endee langchain sentence-transformers openai pypdf

# Add your OpenAI Key (Important for AI Expert Chat)
echo "OPENAI_API_KEY=your_key_here" >> .env

# Verify model exists
# Model should be at: backend/weights/best.pt
dir weights\best.pt

# Populate Endee Knowledge Base (Ensure Endee is running on port 8080)
python rag/document_processor.py

# Start backend server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Backend will be running at**: `http://localhost:8000`

### Step 2: Frontend Setup (New Terminal)

```bash
# Navigate to frontend
cd E:\NTR\cotton-disease-detection\frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

**Frontend will be running at**: `http://localhost:3000`

### Step 3: Test the System

1. Open browser: `http://localhost:3000`
2. Click "Upload Image"
3. Select a cotton leaf image from `E:\NTR\Leaf_Dataset\test\images\`
4. Click "Analyze Image"
5. View results with severity and recommendations!

## 🖥️ PC Application (Optional)

```bash
# Navigate to PC app
cd E:\NTR\cotton-disease-detection\pc_app

# Install dependencies
pip install -r requirements.txt

# Run application
python main.py
```

## 🧪 Test API Directly

### Health Check
```bash
curl http://localhost:8000/health
```

### Predict Image
```bash
curl -X POST -F "file=@path/to/image.jpg" http://localhost:8000/predict-image
```

## 📊 Train Your Own Model (Optional)

```bash
cd E:\NTR\cotton-disease-detection\yolo_training

# Train with your existing dataset
python train.py --data dataset.yaml --epochs 100 --batch 16

# Evaluate trained model
python evaluate.py --weights runs/train/cotton_disease/weights/best.pt

# Export to ONNX
python export_model.py --weights runs/train/cotton_disease/weights/best.pt --formats onnx
```

## 🐛 Troubleshooting

### Backend won't start
```bash
# Check Python version
python --version  # Should be 3.10+

# Reinstall dependencies
pip install --upgrade -r requirements.txt

# Check if model exists
dir backend\weights\best.pt
```

### Frontend won't start
```bash
# Check Node version
node --version  # Should be 18+

# Clear and reinstall
rmdir /s /q node_modules
npm install
```

### Model not found
```bash
# Copy your trained model
copy "E:\NTR\best (1) (1).pt" "E:\NTR\cotton-disease-detection\backend\weights\best.pt"
```

### Port already in use
```bash
# Backend: Use different port
uvicorn main:app --reload --port 8001

# Frontend: Edit vite.config.js to change port
```

## 📖 Next Steps

1. **Read Documentation**:
   - `README.md` - Full project documentation
   - `DEPLOYMENT.md` - Production deployment guide
   - `docs/architecture.md` - System architecture

2. **Explore Features**:
   - Upload different disease images
   - Try live camera detection
   - Check prediction history at `/history`
   - View statistics at `/stats`

3. **Customize**:
   - Modify confidence threshold
   - Add new disease classes
   - Customize UI theme
   - Add authentication

## 🎯 Key Endpoints

- **Web App**: http://localhost:3000
- **API Docs**: http://localhost:8000/docs (Swagger UI)
- **Health Check**: http://localhost:8000/health
- **Predict Image**: POST http://localhost:8000/predict-image
- **History**: http://localhost:8000/history
- **Stats**: http://localhost:8000/stats

## 💡 Tips

1. **GPU Acceleration**: Set `DEVICE=0` in `.env` for GPU
2. **Faster Development**: Use `--reload` flag for auto-restart
3. **Production**: Use multiple workers: `uvicorn main:app --workers 4`
4. **Debugging**: Check logs in terminal for errors

## 🆘 Need Help?

- Check `DEPLOYMENT.md` for detailed setup
- Review `docs/` folder for architecture
- Check error messages in terminal
- Verify all dependencies are installed

---

**You're all set! 🎉 Start detecting cotton diseases now!**
