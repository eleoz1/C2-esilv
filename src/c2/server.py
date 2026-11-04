import socket

HOST = "0.0.0.0"
PORT = 5000

serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    serveur.bind((HOST, PORT))
    serveur.listen(1)

    print("Serveur démarré")
    print("En attente d'une connexion...")

    connexion, adresse = serveur.accept()

    with connexion:
        print("Client connecté :", adresse)

        message = connexion.recv(1024).decode("utf-8")
        print("Message reçu :", message)

        connexion.sendall(b"Message bien recu")

except OSError as erreur:
    print("Erreur réseau :", erreur)

finally:
    serveur.close()