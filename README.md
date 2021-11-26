# HydraBotnet
Remote access tool
H.B. is a multiclient remote access tool using the python request library. It encapsulate request post via http protocol in a reverse shell bypassing proxies that limits outbound connections via normal TCP/IP net-sockets. It uses a modificated version of [server.py] in python http Libs scripts. Scripts are tested under python 3.10.0.
<br>Requests main page:
- https://docs.python-requests.org/en/latest/
<br>
In order not to alert curious observers, the client tries to connect to the server at time periods:<br>
10 times (first running minute of the client)
