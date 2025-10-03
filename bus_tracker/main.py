import tkinter as tk
from bus_tracker.ui.app import BusTrackerApp
from bus_tracker.services.bee_service import BeeService

URL = "https://tfgm.com/travel-updates/live-departures/bus/1800SB39611?serviceName=368"
REFRESH_MS = 30_000

def main():
    root = tk.Tk()
    service = BeeService()
    BusTrackerApp(root, service, URL, REFRESH_MS)
    root.mainloop()

if __name__ == "__main__":
    main()