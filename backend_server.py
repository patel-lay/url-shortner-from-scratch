import asyncio
EXTERNAL_SERVER_PORT = 2000
EXTERNAL_SERVER_HOST = "127.0.0.1"
import socket
import struct 
class backendServer():
    def __init__(self):
        self.message_to_send = b''

    async def send_to_server(self, message):
       # message = "Heellp"
        try:
            reader, writer = await asyncio.open_connection(EXTERNAL_SERVER_HOST, EXTERNAL_SERVER_PORT)

            writer.write(message)  # Send data
            print("Data send")
            await writer.drain()
            print("Data send2, waiting to receive")

            response = await reader.read(1024)  # Read response
            writer.close()
            await writer.wait_closed()
            print(response)

            return response.decode()
        except Exception as e:
            return f"TCP error: {str(e)}"

    def send_to_server_via_socket(self, message):
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((EXTERNAL_SERVER_HOST, EXTERNAL_SERVER_PORT))
            client_socket.send(message + b'\n')
            data = client_socket.recv(1024)
            print(f'Received: {data.decode()}')
            client_socket.close()

    def create_tlv(self, value):
        # """Creates a string-length message.
        if isinstance(value, str):
            value = value.encode('utf-8')
        length = len(value)
        length_bytes = struct.pack("@I", length)
        return length_bytes + value
        # self.message_to_send += length_bytes + value



    def check_url_exists(self, key):
        message = ["get", key]
        temp_message = b''
        for s in message:
            temp_message+=self.create_tlv(s)
        self.message_to_send+=self.create_tlv(self, temp_message)

        respone = self.send_to_server(self.message_to_send)

        #TODO: decode the response
        return response[0]

    def get_url(self, key):
        response = self.check_url_exsits(key)
        return respone
        #TODO: return value        


    def send_url(self, key, value):
        message = ["set", key, value]
        numstr = len(message)
        total_len = 4
        for s in message:
            total_len+= (4 + len(s))
        temp_message = b''
        temp_message+=struct.pack("@I", total_len)
        temp_message+=struct.pack("@I", numstr)
        for s in message:
            temp_message+=self.create_tlv(s)
        # self.message_to_send+=self.create_tlv(temp_message)
        print(temp_message)

        response = asyncio.run(self.send_to_server(temp_message))
        print(response)
        #TODO: decode the response
        return response

    # def set_message():

