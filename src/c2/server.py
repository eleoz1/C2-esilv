import socket
import json
import threading
from datetime import datetime
 
from agent_manager import AgentManager
from interpreter import interpreter
 
HOST = "0.0.0.0"
PORT = 5000
 
manager = AgentManager()
agents_lock = threading.Lock()
 
 
def handle_client(client_socket, client_address):
    """Gere la connexion et l'identification d'un client."""
 
    agent_id = None
 
    print(f"\nClient connecte : {client_address}")
 
    try:
        client_socket.settimeout(10)
 
        message = client_socket.recv(4096).decode("utf-8")
        print("Message brut reçu :", repr(message))

        information = json.loads(message)

        if not isinstance(information, dict):
            raise ValueError("Un objet JSON est attendu.")

        print("Informations JSON :")
        print(json.dumps(information, indent=4))
 
        agent_id = f"{client_address[0]}:{client_address[1]}"
 
        agent_info = {
            "ip": client_address[0],
            "hostname": information.get("hostname", "inconnu"),
            "system": information.get("os", "inconnu"),
            "architecture": information.get("architecture", "inconnu"),
            "status": "connected",
            "connected_at": datetime.now().isoformat()
        }
 
        with agents_lock:
            manager.add_agent(agent_id, agent_info)
 
        print("\nAgents connectes :")
        with agents_lock:
            print(json.dumps(manager.list_agents(), indent=4))
 
        reponse = {
            "status": "ok",
            "message": "Informations recues par le serveur",
            "agent_id": agent_id
        }
 
        client_socket.sendall(
            json.dumps(reponse).encode("utf-8")
        )
 
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
        server_socket.setsockopt(
            socket.SOL_SOCKET,
            socket.SO_REUSEADDR,
            1
        )
 
        server_socket.bind((HOST, PORT))
        server_socket.listen(5)
 
        print(f"Serveur en ecoute sur {HOST}:{PORT}")
 
        try:
            while True:
                client_socket, client_address = server_socket.accept()
 
                client_thread = threading.Thread(
                    target=handle_client,
                    args=(client_socket, client_address),
                    daemon=True
                )
 
                client_thread.start()
 
        except KeyboardInterrupt:
            print("\nArret du serveur.")
 
 
if __name__ == "__main__":
    main()