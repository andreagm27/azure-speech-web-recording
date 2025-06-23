# Azure Speech Web App

This is a simple Flask web application that integrates:

- **Speech-to-Text (STT)** using Azure Cognitive Services and ffmpeg (to convert `.webm` → `.wav`)
- **Text-to-Speech (TTS)** with Azure Neural voices

## 🛠 Setup

```bash
pip install -r requirements.txt
```

Ensure [ffmpeg](https://ffmpeg.org/download.html) is installed and accessible via PATH.

## 🔑 Azure Configuration

Set your Azure Speech resource key and region in `app.py`:

```python
AZURE_KEY = "YOUR_KEY"
AZURE_REGION = "YOUR_REGION"
```

## 🚀 Run

```bash
python app.py
```

Access: http://localhost:5000

## 📦 Tech Stack

- Python 3
- Flask
- Azure Cognitive Services SDK
- ffmpeg
