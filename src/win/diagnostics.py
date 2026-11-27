import platform
import socket
import io
import base64
import os
import winreg
import subprocess
from PIL import ImageGrab


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
                "HELP", "HOSTNAME", "OS", "ARCH", 
                "NETWORK", "INFO", "STATUS", "SCREENSHOT", 
                "EXEC", "SAM"
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

    elif commande == "SCREENSHOT":
        try:
            # Capture de l'ecran
            img = ImageGrab.grab()
            buffer = io.BytesIO()
            img.save(buffer, format="PNG")
            
            # Encodage en base64 pour le JSON
            image_b64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
            
            resultat = {
                "format": "PNG",
                "taille_base64": len(image_b64),
                "image_base64": image_b64
            }
        except Exception as e:
            return {
                "type": "error",
                "message": f"Erreur de capture : {e}"
            }

    elif commande == "EXEC":
        # Liste blanche stricte pour la securite
        ALLOWED = {"whoami", "hostname", "ipconfig", "dir", "ver", "systeminfo"}
        
        # On recupere l'argument (ex: "EXEC whoami")
        args = str(demande.get("args", "")).strip().split()
        
        if not args or args[0].lower() not in ALLOWED:
            return {
                "type": "error",
                "message": "Commande shell non autorisee. Utilisez EXEC <whoami|hostname|ipconfig|dir|ver|systeminfo>."
            }
            
        try:
            out = subprocess.check_output(args, stderr=subprocess.STDOUT, timeout=10, shell=True)
            resultat = {
                "commande_exec": " ".join(args),
                "sortie": out.decode(errors="replace")
            }
        except subprocess.CalledProcessError as e:
            resultat = {
                "commande_exec": " ".join(args),
                "erreur": e.output.decode(errors="replace")
            }
        except Exception as e:
            return {
                "type": "error",
                "message": f"Erreur d'execution : {e}"
            }

    elif commande == "SAM":
        resultat = {}
        
        # 1. Verifier l'existence et les protections du fichier SAM
        sam_path = r"C:\Windows\System32\config\SAM"
        if os.path.exists(sam_path):
            resultat["fichier_sam"] = {
                "chemin": sam_path,
                "status": "Présent",
                "protection": "Verrouillé par le système (SYSTEM)"
            }
        else:
            resultat["fichier_sam"] = {"status": "Introuvable"}
            
        # 2. Lister les utilisateurs locaux via le registre
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SAM\SAM\Domains\Account\Users\Names") as key:
                users = []
                i = 0
                while True:
                    try:
                        name = winreg.EnumKey(key, i)
                        users.append(name)
                        i += 1
                    except OSError:
                        break
                resultat["utilisateurs_locaux"] = users
        except PermissionError:
            resultat["utilisateurs_locaux"] = "Accès refusé (droits SYSTEM requis)"
        except FileNotFoundError:
            resultat["utilisateurs_locaux"] = "Clé de registre introuvable"
        except Exception as e:
            resultat["utilisateurs_locaux"] = f"Erreur : {e}"
            
        resultat["note"] = "Conformément au cadre du TP, les hashes ne sont pas extraits."

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