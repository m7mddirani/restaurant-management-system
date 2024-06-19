import socket
import threading
import json


from backend.save_data import SaveData

class Network:
    def __init__(self, host='localhost', port=5690):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((host, port))
        self.server.listen(5)
        print(f"Server started on {host}:{port}")
        self.clients = []
        self.server_page = None
        threading.Thread(target=self.accept_clients).start()

    def accept_clients(self):
        while True:
            client, addr = self.server.accept()
            print(f"Client connected from {addr}")
            self.clients.append(client)
            threading.Thread(target=self.handle_client, args=(client,)).start()

    def handle_client(self, client):
        while True:
            try:
                message = client.recv(1024).decode()
                if not message:
                    break
                print(f"Received message: {message}")
                response = self.process_message(message)
                if response:
                    client.sendall(json.dumps(response).encode())
            except Exception as e:
                print(f"Error handling client: {e}")
                self.clients.remove(client)
                client.close()
                break

    def process_message(self, message):
        try:
            data = json.loads(message)
            if data["type"] == "order":
                order_data = data["data"]
                start_time = data["start_time"]
                prep_time = max(SaveData.get_item_prep_time(item) for item in order_data["order"].keys())
                order_data["prep_time"] = prep_time
                order_data["start_time"] = start_time
                print(f"Received order data: {order_data}")
                if self.server_page:
                    self.server_page.add_order(order_data)
                return {"status": "received"}
            else:
                return {"status": "unknown type"}
        except Exception as e:
            print(f"Error processing message: {e}")
            return {"status": "error", "error": str(e)}
