import subprocess
import json

class IOSHelper:
    def __init__(self):
        self.devices = []
    
    def refresh_devices(self):
        result = subprocess.run(['idevice_id', '-l'], capture_output=True, text=True)
        self.devices = result.stdout.strip().split('\n')
    
    def install(self, udid, ipa_path):
        cmd = ['ideviceinstaller', '-u', udid, '-i', ipa_path]
        result = subprocess.run(cmd, capture_output=True, text=True)
        return {
            "status": "success" if result.returncode == 0 else "error",
            "output": result.stdout
        }