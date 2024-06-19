import tkinter as tk


from frontend.server_page import ServerPage
from backend.network import Network

class ServerApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Server")
        self.geometry("800x600")
        self.server_page = ServerPage(self)
        self.network = Network(port=5690)
        self.network.server_page = self.server_page
        self.switch_frame(self.server_page)

    def switch_frame(self, frame):
        new_frame = frame
        if hasattr(self, '_frame') and self._frame:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack(fill=tk.BOTH, expand=True)

if __name__ == "__main__":
    app = ServerApplication()
    app.mainloop()
