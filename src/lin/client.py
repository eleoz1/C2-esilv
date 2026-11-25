
import socket
import json
import platform
import subprocess
import argparse


def get_ip_addresses():
    """Récupère les adresses IPv4 non locales."""
    addresses = []

    try:
        result = subprocess.run(
            ["ip", "-o", "-4", "addr", "show", "scope", "global"],
            capture_output=True,
            text=True,
            check=True,
            timeout=5
        )

        for line in result.stdout.splitlines():
            parts = line.split()

            if len(parts) >= 4:
                addresses.append({
                    "interface": parts[1],
                    "ip": parts[3].split("/")[0]
                })

    except (OSError, subprocess.SubprocessError) as error:
        print("Erreur réseau :", error)

    return addresses


def main():
    parser = argparse.ArgumentParser(
        description="Client de diagnostic Linux"
    )

    parser.add_argument("host", help="Adresse IP du serveur")
    parser.add_argument("port", type=int, help="Port du serveur")

    args = parser.parse_args()

    if not 1 <= args.port <= 65535:
        parser.error("Le port doit être compris entre 1 et 65535.")

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.settimeout(10)
        client_socket.connect((args.host, args.port))

        print("Connexion au serveur réussie !")

        information = {
            "hostname": socket.gethostname(),
            "system": platform.system(),
            "release": platform.release(),
            "architecture": platform.machine(),
            "interfaces": get_ip_addresses()
        }

        message = json.dumps(information)
        client_socket.sendall(message.encode("utf-8"))

        response = client_socket.recv(4096).decode("utf-8")
        print("Réponse du serveur :")
        print(json.dumps(json.loads(response), indent=4))

    except ConnectionRefusedError:
        print("Erreur : impossible de joindre le serveur.")

    except socket.timeout:
        print("Erreur : délai dépassé.")

    except (OSError, json.JSONDecodeError) as error:
        print("Erreur :", error)

    finally:
        client_socket.close()
        print("Connexion fermée.")


if __name__ == "__main__":
    main()