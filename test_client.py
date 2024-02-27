import socket

def test_login():
    # Establish connection with server
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("localhost", 8888))
    login_status = False                        # Will change if successful login initiated

    while True:
        # Receive initial login options menu from server, and send user's selection
        prompt = client.recv(1024).decode()
        choice = input(prompt)
        client.send(choice.encode())

        # Read in user entries if either signup (1) or login (2) options were chosen
        if int(choice) == 1 or int(choice) == 2:
            usr = client.recv(1024).decode()
            client.send(input(usr).encode())
            pwd = client.recv(1024).decode()
            client.send(input(pwd).encode())
            if int(choice) == 1:
                conf_pwd = client.recv(1024).decode()
                client.send(input(conf_pwd).encode())
            if int(choice) == 2:
                login_status = bool(int(client.recv(1024).decode()))

        # Receive alert message after ANY option is chosen
        alert_msg = client.recv(1024).decode()
        print(alert_msg+"\n")

        # Terminate menu loop only if exit chosen or login successful
        if alert_msg == "EXITING....." or login_status:
            break

    client.shutdown(2)      # Shutdown client communication with microservice
    client.close()
    return login_status     # Return status of successful login for appropriate program response afterward


if __name__ == '__main__':
    print(test_login())                             # Print boolean result of login microservice result
    print("You may now proceed with your program ....... ")