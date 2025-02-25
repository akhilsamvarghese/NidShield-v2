# NIDShield
![Alt Text](https://drive.google.com/file/d/1eMjBlpdvThWIqrM2syGkQcYk94DqzAHl/view?usp=share_link)
## Overview
NIDShield is a Network Intrusion Detection System (NIDS) leveraging machine learning techniques. This system enhances traditional intrusion detection by dynamically learning from network traffic patterns. By integrating machine learning algorithms, NIDShield can adapt and identify both known and previously unknown threats.

## Features
- Machine learning-based threat detection
- Interactive web interface for monitoring and analysis
- Classification of connection attempts as normal or specific attack types
- Email alerts for detected threats with severity levels
- Historical analysis tracking and visualization
- Support for multiple file formats (.df, .json)
- Detailed traffic classification analysis
- Attack pattern visualization and reporting

## Technology Stack
- **Backend**: Python, Flask
- **Frontend**: HTML5, CSS3, JavaScript
- **Machine Learning**:
  - Gradient Boosting Classifier (Primary Model)
  - Support for other algorithms:
    - Gaussian Naive Bayes (GNB)
    - Decision Tree
    - Random Forest
    - Support Vector Machine (SVM)
    - Logistic Regression
- **Data Processing**: Pandas, NumPy
- **Visualization**: Plotly

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/NIDShield.git
cd NIDShield
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Configure email settings in `Frontend/app.py`:
```python
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USERNAME = "your-email@gmail.com"
SMTP_PASSWORD = "your-app-password"
ADMIN_EMAIL = "admin-email@domain.com"
```

## Usage

1. Start the Flask application:
```bash
cd Frontend
python app.py
```

2. Access the web interface at `http://localhost:3000`

3. Upload network traffic data files (.df or .json format)

4. View real-time analysis results including:
   - Total traffic analyzed
   - Detection status
   - Attack type classification
   - Traffic distribution
   - Historical analysis

## Dataset
NIDShield uses the KDD Cup 1999 dataset, a widely used benchmark dataset for network intrusion detection research. The dataset contains connection records labeled as either normal or specific attack types, including features such as:
- Duration
- Protocol type
- Service
- Flag
- Source/Destination bytes
- Network status indicators
- Traffic statistics

## Attack Types Detected
1. **DOS (Denial of Service)**
   - Attempts to overwhelm system resources
   - High-volume traffic patterns

2. **Probe**
   - Network scanning and surveillance
   - Information gathering attempts

3. **R2L (Remote to Local)**
   - Unauthorized access attempts
   - Credential exploitation

4. **U2R (User to Root)**
   - Privilege escalation attempts
   - System compromise attempts

## Alert System
- Real-time email notifications for detected threats
- Severity classification (HIGH, MEDIUM, LOW)
- Detailed attack information and timestamps
- Attack pattern analysis and reporting

## Security Features
- Secure file upload handling
- Input validation and sanitization
- Error handling and logging
- Session management
- Protected API endpoints

## Project Structure
```
NIDShield/
├── Frontend/
│   ├── app.py           # Flask application
│   ├── static/          # CSS and JavaScript files
│   ├── templates/       # HTML templates
│   ├── DF/             # Data file storage
│   └── logs/           # Analysis history
├── ML-Model/
│   └── GB              # Trained Gradient Boosting model
├── requirements.txt     # Project dependencies
└── README.md           # Project documentation
```

## Contributing
Contributions are welcome! Please feel free to submit pull requests, report bugs, and suggest features.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments
- KDD Cup 1999 dataset providers
- Machine learning community
- Open source contributors

## Contact
Your Name - [akhilsam.v@gmail.com](mailto:akhilsam.v@gmail.com)
Project Link: [https://github.com/akhilsamvarghese/NIDShield](https://github.com/akhilsamvarghese/NidShield-v2)

