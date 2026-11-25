import platform
import socket


def traiter_demande(demande):
    """Prepare les diagnostics locaux autorises."""

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

    if commande == "HELP":
        resultat = {
            "commandes": [
                "HELP", "HOSTNAME", "OS",
                "ARCH", "NETWORK", "INFO", "STATUS"
            ]
        }

    elif commande == "HOSTNAME":
        resultat = {
            "hostname": platform.node()
        }

    elif commande == "OS":
        resultat = {
            "os": platform.system()
        }

    elif commande == "ARCH":
        resultat = {
            "architecture": platform.machine()
        }

    elif commande == "INFO":
        resultat = {
            "hostname": platform.node(),
            "os": platform.system(),
            "release": platform.release(),
            "architecture": platform.machine()
        }

    elif commande == "NETWORK":
        adresses = socket.gethostbyname_ex(
            socket.gethostname()
        )[2]

        resultat = {
            "ipv4": [
                ip for ip in adresses
                if not ip.startswith("127.")
            ]
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


if __name__ == "__main__":
    commande = input("Diagnostic : ")

    demande = {
        "type": "diagnostic_request",
        "commande": commande
    }

    print(traiter_demande(demande))