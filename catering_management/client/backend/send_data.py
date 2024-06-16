from backend.network import Client

class SendData:
    @staticmethod
    def send_order(order_data):
        try:
            client = Client()
            response = client.send_order(order_data)
            return response
        except Exception as e:
            print(f"Error sending order: {e}")
            return None
