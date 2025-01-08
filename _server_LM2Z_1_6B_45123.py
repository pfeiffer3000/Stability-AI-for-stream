# receives a prompt from the sender/client, generates a text response, and sends it back

import socket
from Stable_LM_2_Zephyr_1_6B import chatbot_class


print("Using LLM: Stable LM2 Zephyr 1.6B")
chatbot = chatbot_class.Chatbot()

# get this computer's IP address
# receiver_ip = socket.gethostbyname(socket.gethostname())
receiver_ip = socket.gethostbyname(socket.gethostbyname_ex(socket.gethostname())[2][2])
sender_port = 45123

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((receiver_ip, sender_port))  # Replace with your own IP address and port number

s.listen(1)

print()
print(F"Receiver is listening on {receiver_ip}:{sender_port}")
print()


while True:
    print("Waiting for message...")
    print()

    # Accept the connection from the sender
    conn, addr = s.accept()
    
    # Receive data from the sender
    data = conn.recv(2048)  # Adjust the buffer size as per your requirements

    # Decode the received data
    received_message = data.decode('utf-8')

    # Print the received message
    print('Received message:', received_message)
    response = chatbot.chat(received_message)
    print()
    print('Response:', response)
    print()

    # Send a return message to the sender
    try:
        conn.send(response.encode('utf-8'))
        print("Response sent")
    except:
        print("Error sending response")

    # Close the connection
    conn.close()
