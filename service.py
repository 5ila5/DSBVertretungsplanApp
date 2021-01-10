import time
from plyer import notification
from jnius import autoclass
PythonService = autoclass('org.kivy.android.PythonService')
PythonService.mService.setAutoRestartService(True)

print("in Service")
import getDSB
#getDSB.getContent()
print("in Service")
while True:
    time.sleep(60)
    getDSB.getContent()