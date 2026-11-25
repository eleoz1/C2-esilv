
COMMANDES = {
    "HELP": "Afficher les commandes disponibles",
    "HOSTNAME": "Nom de la machine",
    "OS": "Systeme d'exploitation",
    "ARCH": "Architecture",
    "NETWORK": "Interfaces reseau",
    "INFO": "Toutes les informations"
}


def interpreter(commande):

    if not isinstance(commande, str) or not commande.strip():
        return {
            "statut": "refusee",
            "erreur": "Commande vide ou invalide"
        }

    commande = commande.strip().upper()

    if commande == "HELP":
        return {
            "statut": "ok",
            "commandes": COMMANDES
        }

    if commande in COMMANDES:
        return {
            "statut": "autorisee",
            "commande": commande
        }

    return {
        "statut": "refusee",
        "erreur": "Commande inconnue"
    }
