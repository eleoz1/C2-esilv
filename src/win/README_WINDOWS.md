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

| Fichier | Description |
|---|---|
| `client.py` | Connexion TCP, transmission des informations système et gestion des erreurs. |
| `diagnostics.py` | Gestion des sept diagnostics locaux autorisés. |
| `test_client.py` | Validation des diagnostics et des demandes incorrectes. |
| `test_network.py` | Récupération des adresses IPv4 hors localhost. |
| `README_WINDOWS.md` | Documentation du client Windows. |

## 4. Configuration réseau

| Paramètre | Valeur |
|---|---|
| Machine serveur | Kali Linux |
| Adresse IP serveur | 172.20.1.131 |
| Machine cliente | Windows 11 |
| Adresse IP cliente | 172.20.1.130 |
| Masque réseau | 255.255.255.0 |
| Réseau VMware | Host-only – VMnet1 |
| Port du projet | TCP 5000 |

## 5. Diagnostics disponibles

| Commande | Fonction |
|---|---|
| HELP | Affichage des commandes disponibles. |
| HOSTNAME | Récupération du nom de la machine. |
| OS | Identification du système d'exploitation. |
| ARCH | Identification de l'architecture. |
| NETWORK | Récupération des adresses IPv4. |
| INFO | Récupération des informations système. |
| STATUS | Vérification de l'état du client. |

Les commandes inconnues ou invalides sont refusées.

## 6. Gestion des erreurs

Le programme prévoit la gestion des erreurs suivantes :

- Connexion refusée.
- Délai de réponse dépassé.
- Réponse JSON invalide.
- Erreur réseau.
- Format de demande invalide.
- Type de demande invalide.
- Commande absente ou non autorisée.

## 7. Tests réalisés

| Test | Résultat |
|---|---|
| Vérification de la syntaxe Python | Réussi |
| Ping Windows vers Kali | Réussi – 0 % de perte |
| Ping Kali vers Windows | Échec |
| Connexion TCP sur le port 8000 | Réussi |
| Transfert JSON via HTTP sur le port 5000 | Réussi |
| Diagnostics sur le poste principal | 7/7 |
| Gestion des erreurs locales | 4/4 |
| Tests dans la VM Windows | 11/11 |
| Création et lecture d'une clé de registre de démonstration | Réussi |
| Capture d'écran manuelle | Réussi |
| Exécution manuelle du script de test de démarrage | Réussi |

Les tests HTTP ont été réalisés indépendamment du serveur C2 afin de vérifier la connectivité réseau et le transfert de données.

## 8. Limites actuelles

Les diagnostics sont exécutés localement. Leur déclenchement à distance n'est pas implémenté.

Le démarrage automatique du client, l'exécution distante de commandes Shell/PowerShell, les captures d'écran automatisées et la récupération de la base SAM ne sont pas réalisés.

L'intégration finale du client Windows avec le serveur commun reste à valider. L'adresse du serveur dans le client TCP doit également être actualisée.

## 9. Conclusion

Les diagnostics Windows, la gestion des demandes incorrectes et la connectivité réseau ont été validés dans un environnement virtualisé.

Les onze cas de test locaux ont produit les résultats attendus sur le poste principal et dans la VM Windows. Les contributions sont sauvegardées sur GitHub dans la branche `dev-samantha`.

La validation du protocole applicatif commun et la mise en commun des contributions restent nécessaires.