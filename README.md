# 🛡️ Smart Network Scanner with ML-Based Anomaly Detection

## 📌 Project Overview

Modern networks face increasing threats from malware, RATs, and backdoors — demanding smarter, customizable scanning solutions.

Traditional tools like Nmap often require heavy scripting or external integrations for automation and anomaly detection.

This project introduces a custom Python-based network scanner enhanced with machine learning-powered anomaly detection and a real-time web dashboard.

---

## ❗ Problem Statement

There is a lack of flexible, real-time network scanning tools that provide:

- Built-in anomaly detection
- Historical tracking
- User-friendly dashboards
- Easy integration for educational and research use

---

## 🎯 Project Objective

To develop a Python-based network scanner with:

- Web dashboard
- Machine learning anomaly detection (Isolation Forest)
- Real-time scan analysis
- Historical scan tracking
- Report export (PDF & CSV)

---

## 📂 Scope

- Internal network scanning only
- TCP Connect Scan
- SYN Scan
- UDP Scan
- Isolation Forest ML-based anomaly detection
- User authentication system
- Scan history storage
- Report export functionality

---

## 🛠️ Technologies Used

- Python 3.x
- Flask
- SQLite
- scikit-learn
- NumPy
- Werkzeug
- FPDF
- HTML / CSS / JavaScript

---

## ⚙️ Installation Guide

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/yourusername/smart-network-scanner.git
cd smart-network-scanner
```

### 2️⃣ Create Virtual Environment (Recommended)

```bash
python -m venv venv
```

Activate it:

**Windows**
```bash
venv\Scripts\activate
```

**Linux / Mac**
```bash
source venv/bin/activate
```

---

### 3️⃣ Install Requirements

Create a file named `requirements.txt` and paste:

```
Flask==3.0.0
Werkzeug==3.0.1
scikit-learn==1.4.0
numpy==1.26.4
fpdf==1.7.2
```

Then install:

```bash
pip install -r requirements.txt
```

---

## ▶️ Running the Application

```bash
python app.py
```

Open browser:

```
http://127.0.0.1:5000
```

---

## 📊 Features

- Real-time network scanning
- TCP, SYN, UDP scanning
- Machine Learning anomaly detection
- Interactive dashboard
- Scan history tracking
- Secure login system
- PDF & CSV export

---

## 🧠 Machine Learning Workflow

1. Perform baseline scan
2. Train Isolation Forest model
3. Store scan results in SQLite
4. Detect anomalies in future scans
5. Display flagged ports/services on dashboard

---

## 🔒 Security Notice

This tool is for:

- Educational purposes
- Internal network testing
- Research environments

⚠️ Only scan networks you own or have permission to test.

Unauthorized scanning may violate laws.

---

## 🚀 Future Improvements

- Role-based access control
- Scheduled scans
- Email alerts for anomalies
- Docker deployment
- Advanced ML models

