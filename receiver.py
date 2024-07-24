import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox

# Client configuration
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('server_ip_address', 12345)  # Replace with your server IP and port
client_socket.connect(server_address)

# Function to send message
def send_message(event=None):
    message = message_entry.get()
    if message:
        try:
            client_socket.send(message.encode())
            message_entry.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Error", f"Error sending message: {e}")

# Function to receive messages
def receive_messages():
    try:
        while True:
            message = client_socket.recv(1024).decode()
            if not message:
                break
            chat_box.configure(state=tk.NORMAL)
            chat_box.insert(tk.END, message + '\n')
            chat_box.configure(state=tk.DISABLED)
            chat_box.see(tk.END)
    except Exception as e:
        print(f"Error receiving message: {e}")
    finally:
        client_socket.close()

# GUI setup
root = tk.Tk()
root.title("Chat Application")

# Chat display area
chat_box = scrolledtext.ScrolledText(root, state=tk.DISABLED, wrap=tk.WORD, width=40, height=10)
chat_box.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

# Message entry
message_entry = tk.Entry(root, width=30)
message_entry.grid(row=1, column=0, padx=10, pady=10)

# Send button
send_button = tk.Button(root, text="Send", command=send_message)
send_button.grid(row=1, column=1, padx=10, pady=10)

# Bind Enter key to send message
root.bind('<Return>', send_message)

# Start receiving messages in a separate thread
receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

# Start GUI main loop
root.mainloop()
