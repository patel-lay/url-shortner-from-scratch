import asyncio
EXTERNAL_SERVER_PORT = 4000
EXTERNAL_SERVER_HOST = '127.0.0.1'

class backendServer():
    def __init__(self):
        self.long_url
        self.short_url
        self.message_to_send
        self.total_length 

    async def send_to_server(self, message):
        try:
            reader, writer = await asyncio.open_connection(EXTERNAL_SERVER_HOST, EXTERNAL_SERVER_PORT)
            writer.write(message.encode())  # Send data
            await writer.drain()

            response = await reader.read(1024)  # Read response
            writer.close()
            await writer.wait_closed()

            return response.decode()
        except Exception as e:
            return f"TCP error: {str(e)}"
        

    def create_tlv(self, value):
        # """Creates a string-length message.
        length = len(value)
        length_bytes = length.to_bytes(1, 'big')
        return length_bytes + value
        # self.message_to_send += length_bytes + value



    def check_url_exists(self, key):
        message = ["get", key]
        temp_message = ""
        for s in message:
            temp_message+=self.create_tlv(s)
        self.message_to_send+=self.create_tlv(self, temp_message)

        respone = self.send_to_server(self.message_to_send)

        #TODO: decode the response
        return response[0]

    def get_url(self, key):
        response = self.check_url_exsits(key)

        #TODO: return value        

    def send_url(self, key, value):
        message = ["set", key, value]
        temp_message = ""
        for s in message:
            temp_message+=self.create_tlv(s)
        self.message_to_send+=self.create_tlv(self, temp_message)

        respone = self.send_to_server(self.message_to_send)

        #TODO: decode the response
        return response[0]

    # def set_message():

