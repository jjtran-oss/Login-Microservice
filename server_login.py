import sqlite3
import hashlib
import socket
import threading

# Establish socket connection
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", 8888))
# Start listening for communication from client
server.listen()


def handle_connection(client_side):
    # Loop initial menu unless exit chosen or login was successful
    while True:
        # Initial menu w/ choices
        client_side.send("********** Welcome to LL System **********\n"
                         "1.  Signup\n"
                         "2.  Login\n"
                         "3.  Exit\n"
                         "Enter # of your selection: ".encode())
        choice = client_side.recv(1024).decode()
        ch = int(choice)

        # Call respective function / provide a message based on selection
        match ch:
            case 1:
                signup(client_side)
            case 2:
                attempt_login(client_side)
            case 3:
                client_side.send("EXITING.....".encode())
                exit()
            case _:
                client_side.send("ERROR - Invalid Selection!".encode())

def attempt_login(client_side):
    # Prompt user for login credentials, and passes encoded boolean value to the
    # requesting client based on whether login is successful or not
    client_side.send("\n>>>>>>>>>> Login <<<<<<<<<<\nUsername: ".encode())
    username = client_side.recv(1024).decode()
    client_side.send("Password: ".encode())
    password = client_side.recv(1024)
    password = hashlib.sha256(password).hexdigest()

    # Use SQL SELECT command to get user login info from database
    conn = sqlite3.connect("userdata.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM userdata WHERE username = ? AND password = ?", (username, password))

    # Send a response and True if login works, otherwise False
    if cur.fetchall():
        client_side.send("1".encode())
        client_side.send("Login successful!".encode())
        exit()
    else:
        client_side.send("0".encode())
        client_side.send("Sorry, login failed!".encode())

def signup(client_side):
    # Prompt user to enter new user info, if valid, to store in database
    client_side.send("\n++++++++++ Signup ++++++++++\nEnter New Username: ".encode())
    new_user = client_side.recv(1024).decode()
    client_side.send("Enter New Password: ".encode())
    pwd = client_side.recv(1024)
    client_side.send("Confirm New Password: ".encode())
    conf_pwd = client_side.recv(1024)

    if conf_pwd == pwd:
        # If passwords match, hash password securely as hex representation
        new_pwd = hashlib.sha256(pwd).hexdigest()

        # Use SQL INSERT statement to add new valid user and password into database
        conn = sqlite3.connect("userdata.db")
        cur = conn.cursor()
        cur.execute("INSERT INTO userdata (username, password) VALUES (?, ?)", (new_user, new_pwd))
        conn.commit()

        client_side.send("You have registered successfully!".encode())

    else:
        client_side.send("ERROR - entered passwords do not match!".encode())


if __name__ == '__main__':
    client, addr = server.accept()
    threading.Thread(target=handle_connection, args=(client,)).start()
