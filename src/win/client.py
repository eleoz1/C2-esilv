import socket
import json
import platform
import sys
from diagnostics import traiter_demande

HOST = sys.argv[1] if len(sys.argv) > 1 else "172.20.1.131"
PORT = int(sys.argv[2]) if len(sys.argv) > 2 else 5000


def envoyer(sock, obj):
    sock.sendall((json.dumps(obj) + "\n").encode("utf-8"))


def recevoir(sock):
    buffer = b""
    while not buffer.endswith(b"\n"):
        morceau = sock.recv(4096)
        if not morceau:
            return None
        buffer += morceau
    return json.loads(buffer.decode("utf-8"))


def main():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            client.connect((HOST, PORT))
            print(f"Connecte a {HOST}:{PORT}")

            # 1. Handshake d'identification (compatible server.py de Leo)
            envoyer(client, {
                "hostname": platform.node(),
                "system": platform.system(),
                "os": platform.system(),
                "release": platform.release(),
                "architecture": platform.machine(),
                "interfaces": [{"interface": "principale",
                                "ip": client.getsockname()[0]}]
            })
            confirmation = recevoir(client)
            print("Confirmation :", confirmation)

            # 2. Boucle de commandes
            while True:
                demande = recevoir(client)
                if demande is None:
                    print("Serveur deconnecte.")
                    break
                reponse = traiter_demande(demande)
                envoyer(client, reponse)

    except ConnectionRefusedError:
        print("Erreur : connexion refusee.")
    except socket.timeout:
        print("Erreur : delai depasse.")
    except json.JSONDecodeError:
        print("Erreur : JSON invalide.")
    except OSError as erreur:
        print("Erreur reseau :", erreur)


if __name__ == "__main__":
    main()