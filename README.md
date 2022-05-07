# HydraBotnet
Hydra is a multiclient remote administrative tool using python requests library. It is useful for controlling remote windows machine devices protected behind firewalls that limits outbound connections via standard TCP/IP net-sockets. It encapsulate request post via http protocol in a reverse shell. Server sends the commands to the client which replies through http protocol. It uses a modificated version of the file "server.py" which is inside standard python "http" "Libs" scripts. Scripts are tested and working on python 3.10.0.

#### Modification or replacement of this file is required for proper operation:
```
cd ..\AppData\Local\Programs\Python\Python310\Lib\http\server.py
```
<br>Modificated server file:
https://github.com/SuperMalc/HydraBotnet/blob/main/HTTP/server.py
<br>
<br>Requests main page:
- https://docs.python-requests.org/en/latest/
<br>

![Algorithm schema](https://github.com/SuperMalc/HydraBotnet/blob/main/resources/img1.JPG)

In order not to alert curious network observers, client tries to connect to the server at specific time periods:<br>
* 60 secs (10 tries)
* 8 mins (4 tries)
* after the following minutes the period every more tries is fixed at 15 minutes

### Usage:
* HELP   : show functions
* grab   : download a file from the client
* upload : upload a file to the client
* admck  : check administrative permissions
* exec   : run a command outside mainloop (thread)
