import sqlite3
import json
import os
from datetime import datetime
from fpdf import FPDF
import csv

DB_FILE = 'scanner.db'

def save_scan_to_db(target, scan_type, results, analysis, anomalies):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO scans (target, scan_type, results, analysis, anomalies)
        VALUES (?, ?, ?, ?, ?)
    ''', (target, scan_type, json.dumps(results), json.dumps(analysis), json.dumps(anomalies)))

    conn.commit()
    scan_id = cursor.lastrowid  
    conn.close()
    
    return scan_id

def get_all_scans():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM scans')
    scans = cursor.fetchall()
    conn.close()

    scan_list = []
    for scan in scans:
        scan_list.append({
            'id': scan[0],
            'target': scan[1],
            'scan_type': scan[2],
            'results': json.loads(scan[3]),
            'analysis': json.loads(scan[4]),
            'anomalies': json.loads(scan[5]),
            'created_at': scan[6]
        })
    
    return scan_list

def get_scan_by_id(scan_id):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM scans WHERE id = ?', (scan_id,))
    scan = cursor.fetchone()
    conn.close()

    if scan:
        return {
            'id': scan[0],
            'target': scan[1],
            'scan_type': scan[2],
            'results': json.loads(scan[3]),
            'analysis': json.loads(scan[4]),
            'anomalies': json.loads(scan[5]),
            'created_at': scan[6]
        }
    else:
        return None


from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import mm

def export_to_pdf(scan_id):
    scan = get_scan_by_id(scan_id)
    if not scan:
        return None

    file_path = f"scan_{scan_id}_report.pdf"
    font_path = os.path.join('fonts', 'DejaVuSans.ttf')
    pdfmetrics.registerFont(TTFont('DejaVu', font_path))

    c = canvas.Canvas(file_path, pagesize=A4)
    c.setFont("DejaVu", 11)
    width, height = A4
    y = height - 30

    def draw_line(label, value):
        nonlocal y
        c.drawString(20 * mm, y, f"{label}: {value}")
        y -= 12

    draw_line("Scan Report for", scan['target'])
    draw_line("Scan Type", scan['scan_type'])
    draw_line("Date", scan['created_at'])
    y -= 10

    c.drawString(20 * mm, y, "Results:")
    y -= 12
    for line in json.dumps(scan['results'], indent=2, ensure_ascii=False).splitlines():
        c.drawString(25 * mm, y, line)
        y -= 10

    y -= 8
    c.drawString(20 * mm, y, "Analysis:")
    y -= 12
    for line in json.dumps(scan['analysis'], indent=2, ensure_ascii=False).splitlines():
        c.drawString(25 * mm, y, line)
        y -= 10

    y -= 8
    c.drawString(20 * mm, y, "Anomalies:")
    y -= 12
    for line in json.dumps(scan['anomalies'], indent=2, ensure_ascii=False).splitlines():
        c.drawString(25 * mm, y, line)
        y -= 10

    c.save()
    return file_path



def export_to_csv(scan_id):
    scan = get_scan_by_id(scan_id)
    if not scan:
        return None

    file_path = f"scan_{scan_id}_report.csv"
    with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Target', 'Scan Type', 'Created At', 'Results', 'Analysis', 'Anomalies']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerow({
            'Target': scan['target'],
            'Scan Type': scan['scan_type'],
            'Created At': scan['created_at'],
            'Results': scan['results'],
            'Analysis': scan['analysis'],
            'Anomalies': scan['anomalies']
        })

    return file_path
