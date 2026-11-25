
import socket
import platform
import json

HOST = "172.20.1.129"
PORT = 5000

    """Prepare les diagnostics autorises."""

    if not isinstance(demande, dict):
        return {
            "type": "error",
            "message": "Format de demande invalide"
        }

    if demande.get("type") != "diagnostic_request":
        return {
            "type": "error",
            "message": "Type de demande invalide"
        }

    commande = str(demande.get("commande", "")).strip().upper()

    if commande == "INFO":
        resultat = {
            "hostname": platform.node(),
            "system": platform.system(),
            "release": platform.release()
        }

    elif commande == "NETWORK":
        resultat = {
            "message": "Diagnostic reseau disponible"
        }

    elif commande == "STATUS":
        resultat = {
            "message": "Client Windows actif"
        }

    else:
        return {
            "type": "error",
            "message": "Commande non autorisee"
        }

    return {
        "type": "diagnostic_response",
        "commande": commande,
        "resultat": resultat
    }


def main():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            client.settimeout(5)
            client.connect((HOST, PORT))

            adresse_ip = client.getsockname()[0]

            informations = {
                "hostname": platform.node(),
                "system": platform.system(),
                "release": platform.release(),
                "architecture": platform.machine(),
                "interfaces": [
                    {
                        "interface": "connexion_principale",
                        "ipv4": adresse_ip
                    }
                ]
            }

            client.sendall(
                json.dumps(informations).encode("utf-8")
            )

            print("Connexion au serveur Kali reussie.")
            print("Informations transmises au serveur.")

            reponse = client.recv(4096)

            if reponse:
                confirmation = json.loads(reponse.decode("utf-8"))

                if confirmation.get("status") == "ok":
                    print("Reception confirmee par Kali.")
                else:
                    print("Reponse inattendue du serveur.")
            else:
                print("Le serveur a ferme la connexion.")

    except ConnectionRefusedError:
        print("Erreur : connexion refusee par Kali.")

    except socket.timeout:
        print("Erreur : le serveur ne repond pas.")

    except json.JSONDecodeError:
        print("Erreur : reponse JSON invalide.")

    except OSError as erreur:
        print("Erreur reseau :", erreur)

    print("Fin du programme.")


if __name__ == "__main__":
    main()
