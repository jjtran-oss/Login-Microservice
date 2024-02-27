<h1 align="center"> Login Microservice </h1>

## Requesting Data
It is best to follow the format of the test_login() function from the sample client file when requesting data from the server/microservice.  This is because the initial base login menu has multiple options with varying numbers of send/receive responses which must be handled accordingly on the client side.

This microservice utilizes Python socket programming to communicate between server and client.  Encoding/decoding is done to transfer information as bits.  The general format for requesting data from the server via input from the user is as follows:

    client.send(input(message).encode())

Within the client, it is important to match the looping nature of the menu prompt from the server side.  This means for however many prompts may occur from the server for input, the requests from the client must match that (a.k.a. user must enter proper number of inputs to send to server for processing.)  Encoding is done as a minor layer of security for sent requests.

Since this service will essentially be used at the front of the desired program to authorize access, its server will be running first and the client will be connected to the same local address to await the reception of the login menu prompt.  If given format is followed, requests of data generally won't occur until the user has inputted their first choice.

## Receiving Data
As mentioned above, however many prompts the client will receive from server depends on initial choice of the user at the main menu.  Of course, firstly the client must be ready to accept the sent info of the menu prompt.  These requests will be received as shown below:

    message = client.recv(1024).decode()

To break down in detail for each of the available choices of the login menu for the microservice, please see the following:

- (1) Signup - The server will send **three** prompts for the client to respond to: _enter new username, enter new password, confirm password_.
- (2) Login - The server will send **two** prompts for the client to respond to: _enter username & enter password_.
- (3) Exit - The server will send **no** prompts as user has chosen to exit the login/program.
- (#) Any Other Value - since these are not valid responses, the server sends nothing.

Regardless of choice, all above paths will still have a resulting final 'alert' message that is sent to the client.  This will be utilized to determine if the microservice should be continued or exited (only in case of chosen exit option or successful login).

The main result we are after here is the "boolean" value which will confirm whether proper authorization on login has occurred or not, and to subsequently continue or exit the program.  The response from the server is received as an encoded string, which must be decoded, then converted to integer type and then subsequently boolean to determine whether it is a TRUE or FALSE value.

## UML Diagram
<p align="center">
  <img src="login_uml.png">
</p>