import os
import pandas as pd
from flask import Flask, render_template, request
import pickle
import json
from datetime import datetime

# Import Plotly for creating interactive visualizations
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

# Email Configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USERNAME = "akhilsamvarghese1234@gmail.com"  # Replace with your email
SMTP_PASSWORD = "fmbl yeuw qbbu zosz"      # Replace with your app password
ADMIN_EMAIL = "gdasv0101@gmail.com"        # Replace with admin email

# Load the trained model
GB_exported = pickle.load(open('/Users/akhilsamvarghese/Desktop/Projects/NIDSv2/ML-Model/GB', 'rb'))

# Create directory if it doesn't exist
DF_directory = "./DF/"
if not os.path.exists(DF_directory):
    os.makedirs(DF_directory)

# Add log file configuration
LOG_FILE = os.path.join(os.path.dirname(__file__), 'logs', 'analysis_history.json')
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

def save_to_log(analysis_data):
    """Save analysis results to log file"""
    try:
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, 'r') as f:
                logs = json.load(f)
        else:
            logs = []
        
        logs.append(analysis_data)
        # Keep only the last 10 analyses
        logs = logs[-10:]
        
        with open(LOG_FILE, 'w') as f:
            json.dump(logs, f)
    except Exception as e:
        print(f"Error saving to log: {str(e)}")

@app.route('/', methods=['GET', 'POST'])
def predict():
    # Initialize analysis history
    analysis_history = []
    
    # Load analysis history from file
    try:
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, 'r') as f:
                analysis_history = json.load(f)
    except Exception as e:
        print(f"Error loading analysis history: {str(e)}")
        analysis_history = []

    if request.method == 'POST':
        # Check if the file is present in the request
        if 'DFfile' not in request.files:
            return render_template('index.html', prediction='No file uploaded', history=analysis_history)

        file = request.files['DFfile']

        # If the user does not select a file, browser submits empty file without filename
        if file.filename == '':
            return render_template('index.html', prediction='No selected file', history=analysis_history)

        if file:
            try:
                # Save and process file
                DF_path = os.path.join(DF_directory, file.filename)
                file.save(DF_path)
                df = pd.read_pickle(DF_path)
                predictions = GB_exported.predict(df)
                
                # Calculate statistics
                attack_types = pd.Series(predictions).value_counts().to_dict()
                total_traffic = len(predictions)
                attack_count = sum(count for type_, count in attack_types.items() if type_ != 'normal')
                normal_count = total_traffic - attack_count
                attack_percentage = (attack_count / total_traffic) * 100 if total_traffic > 0 else 0
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                # Check for attacks
                attack_detected = any(pred != 'normal' for pred in predictions)
                
                # Create alert message
                alert_message = None
                if attack_detected:
                    send_attack_alert(attack_types, predictions)
                    alert_message = {
                        'type': 'danger',
                        'message': f'⚠️ Attack Detected! Found following attack types: {", ".join(k for k in attack_types.keys() if k != "normal")}'
                    }
                else:
                    alert_message = {
                        'type': 'success',
                        'message': '✅ No attacks detected. Network traffic appears normal.'
                    }

                # Create log entry and save
                log_entry = {
                    'timestamp': current_time,
                    'filename': file.filename,
                    'total_traffic': total_traffic,
                    'attack_count': attack_count,
                    'normal_count': normal_count,
                    'attack_percentage': round(attack_percentage, 2),
                    'status': 'attack_detected' if attack_detected else 'normal',
                    'attack_types': attack_types
                }
                save_to_log(log_entry)

                return render_template('index.html', 
                                    prediction=predictions.tolist(), 
                                    alert=alert_message,
                                    stats={
                                        'total_traffic': total_traffic,
                                        'attack_count': attack_count,
                                        'normal_count': normal_count,
                                        'attack_percentage': round(attack_percentage, 2),
                                        'timestamp': current_time,
                                        'attack_types': attack_types
                                    },
                                    history=analysis_history)
            except Exception as e:
                return render_template('index.html', 
                                    prediction=f'Error processing file: {str(e)}',
                                    history=analysis_history)

    # GET request or no file uploaded
    return render_template('index.html', prediction=None, stats=None, history=analysis_history)

def send_attack_alert(attack_types, predictions):
    """Send email alert to admin when attack is detected"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Calculate severity based on attack types and frequency
    total_attacks = sum(count for attack, count in attack_types.items() if attack != 'normal')
    if total_attacks > 100:
        severity = "HIGH"
    elif total_attacks > 50:
        severity = "MEDIUM"
    else:
        severity = "LOW"
    
    # Create email content
    subject = f"⚠️ NIDS Alert: Attack Detected - {severity} Severity"
    
    body = f"""
    Network Intrusion Detection Alert
    ================================
    
    Timestamp: {timestamp}
    Severity: {severity}
    
    Attack Details:
    --------------
    """
    
    for attack_type, count in attack_types.items():
        if attack_type != 'normal':
            body += f"\n- {attack_type}: {count} instances"
    
    # Create email message
    msg = MIMEMultipart()
    msg['From'] = SMTP_USERNAME
    msg['To'] = ADMIN_EMAIL
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        # Send email
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.send_message(msg)
        server.quit()
        print(f"Alert email sent successfully to {ADMIN_EMAIL}")
    except Exception as e:
        print(f"Failed to send alert email: {str(e)}")

if __name__ == '__main__':
    app.run(port=3000, debug=True)
