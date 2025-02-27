import asyncio
EXTERNAL_SERVER_PORT = 2000
EXTERNAL_SERVER_HOST = "127.0.0.1"
import socket
import struct 
class backendServer():
    def __init__(self):
        self.message_to_send = b''
        self.total_response_len = 0

    async def send_to_server(self, message):
       # message = "Heellp"
        try:
            reader, writer = await asyncio.open_connection(EXTERNAL_SERVER_HOST, EXTERNAL_SERVER_PORT)

            writer.write(message)  # Send data
            await writer.drain()
            
            response_len = await reader.read(4)  # Read response
            total_len = int.from_bytes(response_len, "little")
            response = await reader.read(total_len)  # Read response
            writer.close()
            await writer.wait_closed()
            if response == None:
                return "No response from server"
            res = self.parse_response(response, total_len)
            return res
        except Exception as e:
            return f"TCP error: {str(e)}"


    def parse_response(self, message, total_len):

        index=0
        return_type = message[index]
        index+=1

        if return_type == 1:
            if (total_len < 1 + 8):
                return "Error in reading err tag"
        
            code =  int.from_bytes(message[index:index+4], "little")
            index+=4
            len =  int.from_bytes(message[index:index+4], "little")
            index+=4
            if (total_len < 1 + 8 + len):
                return "Size mistach in error response\n"
                
            resp = int.from_bytes(message[index:index+4], "little")
            return resp.decode()
        if return_type == 2:
            if(total_len < 1 + 4):  
                return "Error reading string response\n"

            len = int.from_bytes(message[index:index+4], "little")
            index+=4

            if(total_len < 1 + 4 + len):
                return "Error in size of string response\n"
            
            resp = message[index:index+len]

            return resp.decode() 

        

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
        numstr = len(message)
        total_len = 4
        for s in message:
            total_len+= (4 + len(s))
        temp_message+=struct.pack("@I", total_len)
        temp_message+=struct.pack("@I", numstr)

        for s in message:
            temp_message+=self.create_tlv(s)

        response = asyncio.run(self.send_to_server(temp_message))

        #TODO: decode the response
        return response

    def get_url(self, key):
        response = self.check_url_exists(key)
        return response
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
        print("set response", response)
        #TODO: decode the response
        return response

    # def set_message():

