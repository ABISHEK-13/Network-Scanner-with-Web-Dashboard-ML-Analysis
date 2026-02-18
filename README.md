🛡️ Network-Scanner-with-Web-Dashboard-ML-Analysis
📌 Project Overview

Modern networks face increasing threats from malware, Remote Access Trojans (RATs), and backdoors — demanding smarter, customizable scanning solutions.
Traditional tools like Nmap are powerful but often require heavy scripting or external tools for automation, anomaly detection, and integration.
This project introduces a custom Python-based network scanner enhanced with machine learning-powered anomaly detection and an intuitive web dashboard for real-time monitoring, historical tracking, and reporting.

❗ Problem Statement
There is a lack of flexible, real-time network scanning tools that offer:
Integrated anomaly detection
Easy historical tracking
User-friendly dashboards
Educational and research-focused customization

🎯 Project Objective
To develop a custom Python-based network scanner equipped with:
A web dashboard
Machine learning-powered anomaly detection
Real-time scan analysis
Historical tracking and reporting

📂 Scope of the Project
Focused on internal network scanning (not internet-wide reconnaissance)
Implements core scanning techniques:
TCP Connect Scan
SYN Scan
UDP Scan
Integrates Isolation Forest machine learning model for anomaly detection

Includes:
User authentication
Scan history tracking
PDF and CSV report export

🛠️ System Architecture
1️⃣ Scanning Engine
Built from scratch using raw sockets
Supports TCP and UDP packet crafting
Performs port scanning and service detection

2️⃣ Machine Learning Module
Uses Isolation Forest from scikit-learn
Trained on baseline scan data
Detects suspicious port/service behavior patterns

3️⃣ Web Dashboard
Developed using:
Flask
HTML / CSS / JavaScript
Chart.js
Provides:
Real-time scan visualization
Port distribution charts
Anomaly status indicators

Historical data tracking

4️⃣ Database

Uses SQLite

Stores:

User accounts

Scan logs

Classification results

Timestamps

5️⃣ Security

Password hashing via Werkzeug

Session management for authenticated access

Protected routes for dashboard and reports

6️⃣ Report Generation

PDF export using ReportLab

CSV export using Python's built-in CSV module

⚙️ Installation Guide
🔹 1. Clone the Repository
git clone https://github.com/yourusername/smart-network-scanner.git
cd smart-network-scanner

🔹 2. Create Virtual Environment (Recommended)
python -m venv venv


Activate it:

Windows

venv\Scripts\activate


Linux/Mac

source venv/bin/activate

🔹 3. Install Dependencies
pip install -r requirements.txt

▶️ Running the Application

Start the Flask server:

python app.py


Then open your browser and visit:

http://127.0.0.1:5000

📊 Features

✅ Real-time internal network scanning
✅ TCP, SYN, and UDP scanning techniques
✅ Machine learning-based anomaly detection
✅ Interactive web dashboard
✅ Historical scan tracking
✅ User authentication system
✅ PDF and CSV export functionality
