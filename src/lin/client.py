
import socket

HOST = "192.168.20.129"
PORT = 5000

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Connexion au serveur
    client_socket.connect((HOST, PORT))

    print("Connexion au serveur réussie !")

    # Envoi d'un message
    message = "Bonjour, je suis le client Linux !"

    client_socket.sendall(message.encode("utf-8"))

    # Réception de la réponse
    response = client_socket.recv(1024).decode("utf-8")

    print(f"Réponse du serveur : {response}")

except ConnectionRefusedError:
    print("Erreur : impossible de joindre le serveur.")

except OSError as error:
    print(f"Erreur réseau : {error}")

finally:
    client_socket.close()
    print("Connexion fermée.")
