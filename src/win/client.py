
import socket
import platform
import json

# Configuration du serveur Kali
HOST = "172.20.1.129"
PORT = 5000


def executer_diagnostic(commande, adresse_ip):
    """Execute uniquement des diagnostics autorises."""

    commande = commande.strip().upper()

    if commande == "INFO":
        resultat = {
            "commande": "INFO",
            "nom_pc": platform.node(),
            "systeme": platform.system(),
            "version": platform.release()
        }

    elif commande == "IP":
        resultat = {
            "commande": "IP",
            "adresse_ip": adresse_ip
        }

    elif commande == "PING":
        resultat = {
            "commande": "PING",
            "message": "Client Windows actif"
        }

    else:
        resultat = {
            "commande": commande,
            "erreur": "Commande non autorisee"
        }

    return json.dumps(resultat, ensure_ascii=False)


def main():
    print("=== Informations du client Windows ===")
    print("Nom du PC :", platform.node())
    print("Systeme :", platform.system())
    print("Version :", platform.release())

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            client.settimeout(5)
            client.connect((HOST, PORT))

            adresse_ip = client.getsockname()[0]

            print("Adresse IP locale :", adresse_ip)
            print("Connecte au serveur Kali")

            # Test de communication TCP existant
            client.sendall(b"Bonjour depuis Windows")

            reponse = client.recv(1024)

            if reponse:
                print(
                    "Reponse du serveur :",
                    reponse.decode("utf-8")
                )
            else:
                print("Le serveur a ferme la connexion.")

    except socket.timeout:
        print("Erreur : le serveur ne repond pas.")

    except ConnectionRefusedError:
        print("Erreur : connexion refusee. Verifiez Kali.")

    except OSError as erreur:
        print("Erreur reseau :", erreur)

    print("=== Fin du programme ===")


if __name__ == "__main__":
    # Tests locaux de l'interpreteur
    print("=== Tests des diagnostics ===")

    for commande in ["INFO", "IP", "PING", "TEST"]:
        resultat = executer_diagnostic(
            commande,
            "172.20.1.128"
        )
        print(resultat)

    print()

    main()
