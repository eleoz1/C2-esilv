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
- Unittest
- Winreg

## 3. Organisation des fichiers

| Fichier | Description |
|---|---|
| `client.py` | Connexion TCP, transmission des informations système et gestion des erreurs. |
| `diagnostics.py` | Gestion des sept diagnostics locaux autorisés. |
| `test_client.py` | Exécution des 15 tests unitaires automatisés. |
| `test_network.py` | Récupération des adresses IPv4 hors localhost. |
| `test_registre.py` | Lecture locale d'une clé de registre Windows non sensible. |
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

Les commandes inconnues ou invalides sont refusées. Les diagnostics sont exécutés localement.

## 6. Gestion des erreurs

Le programme prévoit la gestion des erreurs suivantes :

- Connexion refusée.
- Délai de réponse dépassé.
- Réponse JSON invalide.
- Erreur réseau.
- Format de demande invalide.
- Type de demande invalide.
- Commande absente ou non autorisée.
- Clé de registre introuvable.
- Accès au registre refusé.

## 7. Lecture du registre Windows

Le script `test_registre.py` utilise la bibliothèque Python `winreg` pour lire une clé de registre de test.

| Paramètre | Valeur |
|---|---|
| Emplacement | `HKEY_CURRENT_USER\Software\ProjetESILV` |
| Nom | Test |
| Type | REG_SZ |
| Valeur | Validation |
| Résultat | Lecture réussie |

La lecture a été validée localement dans la machine virtuelle Windows, indépendamment du serveur C2.

## 8. Tests réalisés

### 8.1. Tests unitaires

Les tests unitaires sont automatisés à l'aide de la bibliothèque `unittest`.

Ils permettent de vérifier les sept diagnostics disponibles ainsi que huit cas d'erreur ou cas particuliers.

| Environnement | Tests réussis | Temps d'exécution |
|---|---|---|
| Ordinateur principal | 15/15 | 0,241 s |
| VM Windows 11 | 15/15 | 0,155 s |

Taux de réussite des tests unitaires : 100 % sur les deux environnements.

### 8.2. Tests complémentaires

| Test | Résultat |
|---|---|
| Vérification de la syntaxe Python | Réussi |
| Ping Windows vers Kali | Réussi – 0 % de perte |
| Ping Kali vers Windows | Échec |
| Connexion TCP sur le port 8000 | Réussi |
| Transfert JSON via HTTP sur le port 5000 | Réussi |
| Récupération des adresses IPv4 hors localhost | Réussi |
| Création d'une clé de registre de test | Réussi |
| Lecture du registre avec PowerShell | Réussi |
| Lecture du registre avec Python | Réussi |
| Capture d'écran manuelle | Réussi |
| Exécution manuelle du script de démarrage | Réussi |

Les tests HTTP ont été réalisés indépendamment du serveur C2 afin de vérifier la connectivité réseau et le transfert de données.

## 9. Limites actuelles

Les diagnostics sont exécutés localement. Leur déclenchement à distance n'est pas implémenté.

Les fonctionnalités suivantes restent non réalisées :

- Démarrage automatique du client.
- Exécution distante de commandes Shell/PowerShell.
- Capture d'écran automatisée.
- Récupération de la base SAM.
- Récupération distante du registre.

L'intégration finale du client Windows avec le serveur commun reste à valider. L'adresse du serveur configurée dans le client TCP doit également être actualisée.

## 10. Conclusion

Le développement du client Windows a permis de mettre en place les bases de la communication TCP, de la transmission JSON, des diagnostics système et de la gestion des erreurs.

Les 15 tests unitaires ont été validés sur le poste principal et dans la machine virtuelle Windows, avec un taux de réussite de 100 %.

La lecture locale du registre Windows a également été réalisée avec succès à l'aide de Python.

Les contributions sont sauvegardées sur GitHub dans la branche `dev-samantha`.

La validation du protocole applicatif commun, la mise en commun des contributions et les fonctionnalités restantes sont nécessaires pour satisfaire l'intégralité du cahier des charges.