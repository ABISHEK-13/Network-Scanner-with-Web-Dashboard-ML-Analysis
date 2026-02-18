import sqlite3
import json
import os

DB_FILE = 'scanner.db'

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS scans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            target TEXT,
            scan_type TEXT,
            full_scan BOOLEAN,
            scan_results TEXT,
            anomalies TEXT,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def save_scan(target, scan_type, full_scan, results, anomalies):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO scans (target, scan_type, full_scan, scan_results, anomalies)
        VALUES (?, ?, ?, ?, ?)
    ''', (target, scan_type, full_scan, json.dumps(results), json.dumps(anomalies)))
    conn.commit()
    conn.close()

def get_scan_history():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT id, target, scan_type, full_scan, date FROM scans ORDER BY date DESC')
    history = cursor.fetchall()
    conn.close()
    return history

def get_scan_by_id(scan_id):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM scans WHERE id = ?', (scan_id,))
    scan = cursor.fetchone()
    conn.close()
    return scan

import csv

def export_scan_to_csv(scan_id):
    scan = get_scan_by_id(scan_id)
    if scan:
        filename = f'scan_{scan_id}.csv'
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['ID', 'Target', 'Scan Type', 'Full Scan', 'Date', 'Results', 'Anomalies'])
            writer.writerow([scan[0], scan[1], scan[2], scan[3], scan[4], scan[5], scan[6]])
        return filename
    return None

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def export_scan_to_pdf(scan_id):
    scan = get_scan_by_id(scan_id)
    if scan:
        filename = f'scan_{scan_id}.pdf'
        c = canvas.Canvas(filename, pagesize=letter)
        c.setFont("Helvetica", 12)
        c.drawString(100, 750, f"Scan ID: {scan[0]}")
        c.drawString(100, 735, f"Target: {scan[1]}")
        c.drawString(100, 720, f"Scan Type: {scan[2]}")
        c.drawString(100, 705, f"Full Scan: {'Yes' if scan[3] else 'No'}")
        c.drawString(100, 690, f"Date: {scan[4]}")
        c.drawString(100, 675, f"Scan Results: {scan[5]}")
        c.drawString(100, 660, f"Anomalies: {scan[6]}")
        c.save()
        return filename
    return None
