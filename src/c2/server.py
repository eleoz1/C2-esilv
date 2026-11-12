
import socket

# Configuration du serveur
HOST = "0.0.0.0"
PORT = 5000

# Création de la socket TCP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Association de l'adresse IP et du port
    server_socket.bind((HOST, PORT))

    # Le serveur attend une connexion
    server_socket.listen(1)

    print(f"Serveur en écoute sur {HOST}:{PORT}")

    # Acceptation d'une connexion
    client_socket, client_address = server_socket.accept()

    print(f"Client connecté : {client_address}")

    # Réception d'un message
    message = client_socket.recv(1024).decode("utf-8")

    print(f"Message reçu : {message}")

    # Réponse au client
    client_socket.sendall(
        "Message reçu par le serveur !".encode("utf-8")
    )

    client_socket.close()

except OSError as error:
    print(f"Erreur serveur : {error}")

finally:
    server_socket.close()
    print("Serveur arrêté.")
