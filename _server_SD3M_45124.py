# This should be running before the client on the bot.
# This receives the prompt, generates an image, and sends it back

import os
import socket
from datetime import datetime

# import the ImageGenerator class from the appropriate file
from Stable_Diffusion_3_Medium.SD3M_class import ImageGenerator

imgen = ImageGenerator()

# create a folder for today's images
path_to_images = os.path.abspath("path-to-image-folder")+"\\"+datetime.now().strftime("%Y-%m-%d")
if not os.path.exists(path_to_images):
    os.mkdir(path_to_images)


server_ip = socket.gethostbyname(socket.gethostname())
port = 45124  # 45124 for images 45123 for llm

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((server_ip, port))

server.listen()

while True:
    if server.fileno() == -1:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((server_ip, port))
        server.listen()
        print(f"Reopened socket on {server_ip}:{port}")
    try:
        print()
        print(F"Receiver is listening on {server_ip}:{port}")
        print()
        client, addr = server.accept()
        print(f"Connection from {addr} has been established.")
        while True:
            try:
                # receive prompt and style
                data = client.recv(1024).decode()
                if not data:
                    break
                if data.startswith("prompt:"):
                    prompt = data[8:]
                    print(f'Received the prompt: "{prompt}"')
                    client.sendall("prompt ok".encode())
                elif data.startswith("style:"):
                    style = data[7:]
                    print(f'Received the style: "{style}"')
                    client.sendall("style ok".encode())
                elif data.startswith("<END>"):
                    print("<END> received")
                    client.sendall("<END> ok".encode())
                    break

            except Exception as e: 
                print(f"prompt and style receiving error")
                print(e)

        # generate the image, then save it so that image metadata can be loaded and sent next
        print("Generating the image...")
        image = imgen.generate_image(prompt=prompt, style=style)
        imgen.save_image(path_to_save=path_to_images)

        # send the image by first loading it with metadata
        file_size = os.path.getsize(imgen.image_name)
        client.send(str(file_size).encode())
        print("Sending the image...")
        with open(imgen.image_name, 'rb') as file:
            file_data = file.read(1024)
            while file_data:
                client.send(file_data)
                file_data = file.read(1024)

        # send a tag that signals that the image has been fully sent
        client.send(b'<EOF>')
        print("Image sent.")
    
    except Exception as e: print(e)
    
    except KeyboardInterrupt: break

client.close()
server.close()