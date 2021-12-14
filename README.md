# HydraBotnet
Hydra is a multiclient remote administrative tool using python requests library. It is useful for controlling remote windows machine devices protected behind firewalls that limits outbound connections via standard TCP/IP net-sockets. It encapsulate request post via http protocol in a reverse shell. Server sends the commands to the client which replies through http protocol. It uses a modificated version of the file "server.py" which is inside standard python "http" "Libs" scripts. Scripts are tested and working on python 3.10.0.
<br>Requests main page:
- https://docs.python-requests.org/en/latest/
<br>
In order not to alert curious network observers, client tries to connect to the server at specific time periods:<br>
* 60 secs (10 tries)
* 8 mins (4 tries)
* after the following minutes the period is fixed at 15 minutes
