import socket

HOST = "0.0.0.0"
PORT = 5000

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serveur:
        serveur.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        serveur.bind((HOST, PORT))
        serveur.listen(5)

        print("Serveur demarre")
        print("En attente de connexions...")

        while True:
            connexion, adresse = serveur.accept()

            with connexion:
                print(f"\nClient connecte : {adresse}")

                message = connexion.recv(1024)

                if message:
                    print("Message recu :", message.decode("utf-8"))
                    connexion.sendall(b"Message bien recu")
                else:
                    print("Client deconnecte sans message")

except KeyboardInterrupt:
    print("\nArret du serveur")

except OSError as erreur:
    print("Erreur reseau :", erreur)