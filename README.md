# HydraBotnet
Hydra is a multiclient remote administrative tool using python requests library. It is useful for controlling remote windows machine devices protected behind firewalls that limits outbound connections via standard TCP/IP net-sockets. It encapsulate request post via http protocol with a reverse shell. It uses a modificated version of the file "server.py" inside standard python http Libs scripts. Scripts are tested and working on python 3.10.0.
<br>Requests main page:
- https://docs.python-requests.org/en/latest/
<br>
In order not to alert curious observers, the client tries to connect to the server at time periods:<br>
10 times (first running minute of the client)
