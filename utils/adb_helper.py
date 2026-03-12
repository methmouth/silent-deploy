from adbutils import adb
import subprocess

class ADBHelper:
    def __init__(self):
        self.devices = []
    
    def refresh_devices(self):
        self.devices = [d.serial for d in adb.device_list()]
    
    def install(self, device_id, apk_path):
        try:
            device = adb.device(device_id)
            device.uninstall("com.pentest.payload")
            device.install(apk_path, replace=True)
            return {"status": "success", "device": device_id}
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    def get_install_status(self):
        status = {}
        for dev in self.devices:
            device = adb.device(dev)
            status[dev] = device.is_installed("com.pentest.payload")
        return status