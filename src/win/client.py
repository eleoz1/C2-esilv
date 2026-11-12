import socket

HOST = "172.20.1.129"
PORT = 5000

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.settimeout(5)
        client.connect((HOST, PORT))

        print("Connecté au serveur Kali")

        client.sendall(b"Bonjour depuis Windows")

        reponse = client.recv(1024).decode("utf-8")
        print("Réponse du serveur :", reponse)

except OSError as erreur:
    print("Erreur de connexion :", erreur)