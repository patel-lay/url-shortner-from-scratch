import zlib #crc32 hash function library 
import random
import string
from backend_server import backendServer


class hashFunction():
    def __init__(self):
        self.long_url = ''
        self.short_url = "https://tinyurl.com/"
        
    
    def create_hash(self, long_url):
        temp_long_url = long_url.encode('utf-8')

        temp_hash = zlib.crc32(temp_long_url) #8 byte long shortened url
        print(temp_hash)
        backend = backendServer()
        temp_short_url = self.short_url + str(temp_hash) 
        if(backend.check_url_exists(temp_short_url)):
            new_string = ''.join(random.choices(string.ascii_letters + string.digits, k=8)) # add 8 bytes of predefined string. 
            long_url +=new_string
            print("hash already exists")
            self.create_hash(long_url)
        else:
            self.short_url = temp_short_url
        # self.short_url = temp_short_url
        return
        
    #Need this as we modify long_url in case of collision 
    def set_long_url(self, long_url):
        self.long_url = long_url

    def get_short_url(self):
        return self.short_url 
    
    def get_long_url(self):
        return self.long_url



             



        
        