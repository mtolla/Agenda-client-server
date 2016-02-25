# Librerie underground Task
import threading
import time
# Importo loginManager
from loginManager import ClassLoginManager


# Background work
# Codice ispirato da http://sebastiandahlgren.se/2014/06/27/running-a-method-as-a-background-thread-in-python/
class BackgroundThread():
    def __init__(self, interval=36000):  # 36000 = 10 min
        self.interval = interval
        login_manager = ClassLoginManager()
        thread = threading.Thread(target=self.run(login_manager), args=())
        thread.daemon = True  # Daemonize thread
        thread.start()  # Start the execution

    def run(self, login_manager):
        while True:
            login_manager.check_life_token()
            time.sleep(36000)
