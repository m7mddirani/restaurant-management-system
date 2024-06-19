import json
import tkinter as tk


from threading import Thread

from frontend.menu import MenuPage
from backend.network import Client

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Client")
        self.geometry("1024x768")  # Adjust the size of the client window
        self._frame = None
        self.switch_frame(MenuPage)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack(fill=tk.BOTH, expand=True)

def run_client():
    client = Client(port=5690)  # Ensure the port is set here
    client.connect()
    client.send_message(json.dumps({"type": "connection", "message": "Client connected"}))

if __name__ == "__main__":
    app = Application()
    Thread(target=run_client, daemon=True).start()
    app.mainloop()
