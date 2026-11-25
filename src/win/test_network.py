import socket

nom_pc = socket.gethostname()
adresses = socket.gethostbyname_ex(nom_pc)[2]

for ip in adresses:
    if not ip.startswith("127."):
        print(ip)