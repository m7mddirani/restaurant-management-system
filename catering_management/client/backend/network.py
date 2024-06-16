import socket
import json
import time

class Network:
    def __init__(self, host='localhost', port=5690):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port

    def connect(self):
        try:
            self.client.connect((self.host, self.port))
            print(f"Connected to server at {self.host}:{self.port}")
        except Exception as e:
            print(f"Error connecting to server: {e}")

    def send_message(self, message):
        try:
            print(f"Sending message: {message}")
            self.client.sendall(message.encode())
            response = self.client.recv(1024).decode()
            print(f"Received response: {response}")
            return json.loads(response)
        except socket.error as e:
            print(f"Socket error: {e}")
            return None
        except Exception as e:
            print(f"Error sending message: {e}")
            return None
        finally:
            self.client.close()

class Client(Network):
    def __init__(self, host='localhost', port=5690):
        super().__init__(host, port)

    def send_order(self, order_data):
        self.connect()
        try:
            message = json.dumps({
                "type": "order",
                "data": order_data,
                "start_time": time.time()
            })
            print(f"Prepared message: {message}")
            response = self.send_message(message)
            print(f"Received response: {response}")
            return response
        except Exception as e:
            print(f"Error sending order: {e}")
            return None
        finally:
            self.client.close()
