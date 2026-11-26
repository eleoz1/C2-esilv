import socket
import json

HOST = "127.0.0.1"
PORT = 5000

def envoyer(fichier, obj):
    fichier.write((json.dumps(obj) + "\n").encode("utf-8"))
    fichier.flush()

def recevoir(fichier):
    ligne = fichier.readline()
    if not ligne:
        return None
    return json.loads(ligne.decode("utf-8"))

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serveur:
        serveur.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        serveur.bind((HOST, PORT))
        serveur.listen(1)
        print(f"Serveur de test en ecoute sur {PORT}...")

        connexion, adresse = serveur.accept()
        print(f"Client connecte : {adresse}")

        with connexion, connexion.makefile("rwb") as fichier:
            # 1. Lire le handshake (infos d'identification)
            info = recevoir(fichier)
            print("Infos recues :", info)
            
            # 2. Confirmer
            envoyer(fichier, {"status": "ok", "message": "Bien recu"})

            # 3. Boucle de commandes
            while True:
                commande = input("Commande > ").strip()
                if commande.lower() == "quit":
                    break
                envoyer(fichier, {"type": "diagnostic_request", "commande": commande})
                
                reponse = recevoir(fichier)
                if reponse is None:
                    print("Client deconnecte.")
                    break
                print("Reponse :", json.dumps(reponse, indent=2))

if __name__ == "__main__":
    main()