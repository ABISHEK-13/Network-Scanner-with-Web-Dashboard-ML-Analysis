from flask import Flask, render_template, request, redirect, session, jsonify, send_file
from scanner import scan_ports, analyze_results
from security_analysis import AnomalyDetector
from auth import verify_user, init_db
from auth import register_user

from utils import save_scan_to_db, get_all_scans, get_scan_by_id, export_to_pdf, export_to_csv

app = Flask(__name__)
app.secret_key = '81275867218b99689600a265a0e5f634'  
detector = AnomalyDetector()


def setup():
    init_db()


@app.route('/')
def home():
    if 'user_id' in session:  
        return redirect('/dashboard')
    setup()

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        success = register_user(username, password)
        if success:
            return redirect('/login') 
        return render_template('register.html', error='Username already exists')
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_id = verify_user(username, password)   
        if user_id:
            session['user_id'] = user_id
            return redirect('/dashboard')
        return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user_id', None) 
    return redirect('/')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session: 
        return redirect('/')
    return render_template('dashboard.html')

@app.route('/scan', methods=['POST'])
def scan():
    if 'user_id' not in session: 
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.json
    target = data.get('target')
    scan_type = data.get('type', 'stealth')
    ports = list(range(1, 65535)) if data.get('full_scan') else [21, 22, 80, 443, 1337, 3389, 6667, 8080]
    results = scan_ports(target, ports, scan_type)
    analysis = analyze_results(results)
    anomalies = detector.detect(results)
    scan_id = save_scan_to_db(target, scan_type, results, analysis, anomalies)
    
    return jsonify({
        'results': results,
        'analysis': analysis,
        'anomalies': anomalies,
        'scan_id': scan_id
    })

@app.route('/history')
def history():
    if 'user_id' not in session:  
        return redirect('/')
    scans = get_all_scans() 
    return render_template('history.html', scans=scans)

@app.route('/scan/<int:scan_id>')
def view_scan(scan_id):
    scan = get_scan_by_id(scan_id)  
    return jsonify(scan)

@app.route('/export/pdf/<int:scan_id>')
def export_pdf(scan_id):
    file_path = export_to_pdf(scan_id) 
    return send_file(file_path, as_attachment=True)

@app.route('/export/csv/<int:scan_id>')
def export_csv(scan_id):
    file_path = export_to_csv(scan_id) 
    return send_file(file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
