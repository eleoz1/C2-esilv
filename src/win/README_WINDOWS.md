# Client Windows – Projet C2

## 1. Objectif

Développer un client Windows capable de communiquer avec un serveur Kali Linux à travers une connexion TCP et de transmettre des informations au format JSON dans un environnement de laboratoire isolé.

## 2. Technologies utilisées

- Python
- Socket TCP
- JSON
- PowerShell
- VMware Workstation
- Git et GitHub

## 3. Organisation des fichiers

- `client.py` : connexion au serveur, transmission des informations système et gestion des erreurs.
- `test_client.py` : validation locale des diagnostics et des demandes incorrectes.
- `test_network.py` : récupération des adresses IPv4 hors localhost.

## 4. Diagnostics

| Commande | Fonction |
|---|---|
| INFO | Récupération des informations système |
| NETWORK | Message de disponibilité du diagnostic réseau |
| STATUS | Vérification de l'état du client |

Les commandes inconnues sont refusées.

## 5. Gestion des erreurs

Le programme prend en compte les erreurs suivantes :

- Connexion refusée.
- Délai de réponse dépassé.
- Réponse JSON invalide.
- Erreur réseau.
- Demande incorrecte.
- Commande non autorisée.

## 6. Tests réalisés

- Communication réseau entre Windows et Kali.
- Récupération des adresses IPv4.
- Exclusion de localhost.
- Validation locale des diagnostics.
- Création et lecture d'une clé de registre de démonstration.
- Vérification de la syntaxe Python.

## 7. Limites actuelles

Les diagnostics sont testés localement. Leur déclenchement à distance n'est pas implémenté.

Le démarrage automatique du client, les captures d'écran automatisées et la récupération de la base SAM ne sont pas réalisés.

## 8. Conclusion

Les bases de la communication TCP, de la transmission JSON et de la gestion des erreurs ont été développées. Des tests complémentaires restent nécessaires pour valider l'intégration finale avec le serveur commun.