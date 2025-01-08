# this tests the connection between the client and the server for llm
# it sends info to the server and receives a response

import socket
from datetime import datetime

host = 'your-AI-machine-IP-address'
port = 45123

print("Enter messages to sent to the AI machine")

while True:
    start_time = datetime.now()

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))
    print(f"Connected to {host}:{port}")

    # get the information to send
    prompt = input("> ")
    
    # send prompt 
    print(f"Sending: {prompt}")
    client.send(prompt.encode())

    # receive the response
    data = client.recv(2048)
    if data:
        print(data.decode())
    else:
        print("No data received")
    
    print(f"Time taken: {datetime.now() - start_time}")
    print()

    client.close()