
import socket
import platform

HOST = "172.20.1.129"
PORT = 5000

nom_pc = platform.node()
systeme = platform.system()
version = platform.release()

print("=== Informations du client Windows ===")
print("Nom du PC :", nom_pc)
print("Systeme :", systeme)
print("Version :", version)

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.settimeout(5)
        client.connect((HOST, PORT))

        print("Adresse IP locale :", client.getsockname()[0])
        print("Connecte au serveur Kali")

        client.sendall(b"Bonjour depuis Windows")

        reponse = client.recv(1024)

        if reponse:
            print("Reponse du serveur :", reponse.decode("utf-8"))
        else:
            print("Le serveur a ferme la connexion.")

except socket.timeout:
    print("Erreur : le serveur ne repond pas.")

except ConnectionRefusedError:
    print("Erreur : connexion refusee. Verifiez que Kali est demarre.")

except OSError as erreur:
    print("Erreur reseau :", erreur)

print("=== Fin du programme ===")
