import socket
import threading
import random
from datetime import datetime

RISKY_SERVICES = {
    21: 'FTP',
    22: 'SSH',
    23: 'Telnet',
    25: 'SMTP',
    53: 'DNS',
    69: 'TFTP',
    80: 'HTTP',
    110: 'POP3',
    139: 'NetBIOS',
    143: 'IMAP',
    161: 'SNMP',
    389: 'LDAP',
    445: 'SMB',
    3389: 'RDP',
    111: 'RPCBind',
    512: 'Exec',
    513: 'Login',
    514: 'Shell',
    1099: 'RMIRegistry',
    1524: 'IngresLock',
    2049: 'NFS',
    2121: 'CCProxy-FTP',
    3306: 'MySQL',
    3632: 'Distccd',
    5432: 'PostgreSQL',
}

def grab_banner(ip, port):
    try:
        s = socket.socket()
        s.settimeout(1)
        s.connect((ip, port))
        banner = s.recv(1024).decode(errors='ignore').strip()
        s.close()
        return banner
    except:
        return ""

def tcp_connect(ip, port, results):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    try:
        s.connect((ip, port))
        banner = grab_banner(ip, port)
        results.append({'port': port, 'status': 'open', 'banner': banner})
    except:
        results.append({'port': port, 'status': 'closed'})
    finally:
        s.close()

def udp_scan(ip, port, results):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(2)
    try:
        s.sendto(b'', (ip, port))
        data, _ = s.recvfrom(1024)
        results.append({'port': port, 'status': 'open|filtered'})
    except socket.timeout:
        results.append({'port': port, 'status': 'filtered'})
    except:
        results.append({'port': port, 'status': 'closed'})
    finally:
        s.close()

def stealth_scan(ip, port, results):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    try:
        s.connect((ip, port))
        results.append({'port': port, 'status': 'open'})
    except:
        results.append({'port': port, 'status': 'closed'})
    finally:
        s.close()

def scan_ports(ip, ports, scan_type='stealth'):
    threads = []
    results = []

    for port in ports:
        if scan_type == 'tcp':
            t = threading.Thread(target=tcp_connect, args=(ip, port, results))
        elif scan_type == 'udp':
            t = threading.Thread(target=udp_scan, args=(ip, port, results))
        else:
            t = threading.Thread(target=stealth_scan, args=(ip, port, results))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    return sorted(results, key=lambda x: x['port'])

def analyze_results(results):
    from security_analysis import AnomalyDetector
    detector = AnomalyDetector()
    anomalies = detector.detect(results)

    for r in results:
        if r['status'] == 'open':
            port = r['port']
            if port in RISKY_SERVICES:
                r['risk'] = f"RISKY ({RISKY_SERVICES[port]})"
            else:
                r['risk'] = "Normal"
        else:
            r['risk'] = "-"
    

    for a in anomalies:
        for r in results:
            if r['port'] == a['port']:
                r['risk'] = f"⚠️ Anomaly (Score: {a['risk_score']:.2f})"
    
    return anomalies
