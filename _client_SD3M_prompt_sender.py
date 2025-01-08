# this is the client that will live on the bot
# it sends info to the server and receives the image back

import os
import io
import socket
from datetime import datetime
from time import sleep


host = 'ip-address-of-server-running-the-image-generator'

class Local_imageGen():
    def __init__(self, host=host, port=45124, **kwargs):
        self.__dict__.update(kwargs)
        self.image_count = 0
        self.host = host
        self.port = port
        
    def generate_image(self, prompt="Hack The Planet", style="photographic, realistic, 4k", output_format="png"):
        self.prompt = "prompt: " + prompt
        self.style = "style: " + style
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.settimeout(30)
            client.connect((self.host, self.port))

            # send prompt
            data = "no response"
            while data != "prompt ok":
                print(f'Sending prompt: "{self.prompt}"')
                client.send(self.prompt.encode())
                data = client.recv(1024).decode()
                print(f"  --response: {data}")
                sleep(0.1)
            
            #send style
            while data != "style ok":
                print(f'Sending style: "{self.style}"')
                client.send(self.style.encode())
                data = client.recv(1024).decode()
                print(f"  --response: {data}")
                sleep(0.1)

            #send <END>
            while data != "<END> ok":
                print('Sending: "<END>"')
                client.send("<END>".encode())
                data = client.recv(1024).decode()
                print(f"  --response: {data}")
                sleep(0.1)

            print()
            print("Ready to receive image...")
            client.settimeout(120)
            try:
                self.file_size = client.recv(1024).decode()
                print(f"Incoming file size: {self.file_size}")
                client.settimeout(5)
                print("Receiving image...")

                timestring = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                self.received_file_name = f"{self.prompt}_received_{timestring}.png"
                
                file_stream = io.BytesIO()
                data = client.recv(1024)
                while data:
                    file_stream.write(data)
                    data = client.recv(1024)
                    if data[-5:] == b"<EOF>":
                        file_stream.write(data[:-5])
                        # print("<EOF> received")
                        break

                client.close()

                return file_stream
            
            except Exception as e: 
                print(e)
                client.close()
                return None
        
        except Exception as e: print(e)

        except KeyboardInterrupt:
            print("Keyboard interrupt. Exiting...")

    def save_image(self, file_stream):
        save_location = os.path.join(r"path-to-images", self.received_file_name)
        with open(save_location, 'wb') as file:
            file.write(file_stream.getvalue())
        print(f"Image saved as {self.received_file_name}")
        print(f"file size difference = {int(self.file_size) - len(file_stream.getvalue())} bytes")
        
if __name__ == "__main__":
    imgen = Local_imageGen()
    while True:
        prompt = input("Enter a prompt: ")
        if prompt == "":
            prompt = "Hack The Planet"
        style = input("Enter a style: ")
        if style == "":
            style = "photographic, realistic, 4k"
        print()
        file_stream = imgen.generate_image(prompt=prompt, style=style)
        if file_stream:
            imgen.save_image(file_stream)
        