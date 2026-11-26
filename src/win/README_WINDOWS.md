# Client Windows – Projet C2

## 1. Objectif
Développer un client Windows capable de communiquer avec un serveur Kali Linux à travers une connexion TCP et de transmettre des informations au format JSON dans un environnement de laboratoire isolé.

## 2. Technologies utilisées
- Python
- Socket TCP
- JSON
- PowerShell
- Pillow (pour les captures d'écran)
- VMware Workstation
- Git et GitHub
- Unittest
- Winreg

## 3. Organisation des fichiers
| Fichier | Description |
|---|---|
| `client.py` | Connexion TCP, boucle de commandes, transmission des informations et gestion des erreurs. |
| `diagnostics.py` | Gestion des 8 diagnostics locaux autorisés (dont la capture d'écran). |
| `test_client.py` | Exécution des 16 tests unitaires automatisés. |
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
| SCREENSHOT | Capture de l'écran de la VM encodée en base64. |

Les commandes inconnues ou invalides sont refusées. Les diagnostics sont exécutés localement.

## 6. Démarrage automatique
Le client est configuré pour démarrer automatiquement au lancement de la session Windows.
- Un raccourci vers la commande de lancement a été placé dans le dossier `shell:startup`.
- Ainsi, dès l'ouverture de la VM Windows, le client s'exécute et tente de se connecter au serveur C2.

## 7. Gestion des erreurs
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
- Erreur lors de la capture d'écran.

## 8. Lecture du registre Windows
Le script `test_registre.py` utilise la bibliothèque Python `winreg` pour lire une clé de registre de test.
| Paramètre | Valeur |
|---|---|
| Emplacement | `HKEY_CURRENT_USER\Software\ProjetESILV` |
| Nom | Test |
| Type | REG_SZ |
| Valeur | Validation |
| Résultat | Lecture réussie |
La lecture a été validée localement dans la machine virtuelle Windows, indépendamment du serveur C2.

## 9. Tests réalisés
### 9.1. Tests unitaires
Les tests unitaires sont automatisés à l'aide de la bibliothèque `unittest`.
Ils permettent de vérifier les huit diagnostics disponibles ainsi que les cas d'erreur.

| Environnement | Tests réussis | Temps d'exécution |
|---|---|---|
| Ordinateur principal | 16/16 | 0,590 s |
| VM Windows 11 | 16/16 | À valider |

Taux de réussite des tests unitaires : 100 %.

### 9.2. Tests complémentaires
| Test | Résultat |
|---|---|
| Vérification de la syntaxe Python | Réussi |
| Ping Windows vers Kali | Réussi |
| Connexion TCP avec serveur de test | Réussi |
| Récupération des adresses IPv4 hors localhost | Réussi |
| Création d'une clé de registre de test | Réussi |
| Lecture du registre avec PowerShell | Réussi |
| Lecture du registre avec Python | Réussi |
| Capture d'écran et encodage base64 | Réussi |
| Exécution manuelle du script de démarrage | Réussi |

## 10. Limites actuelles
- L'intégration finale avec le serveur de production (Kali) dépend de la boucle de commandes implémentée côté serveur.
- L'exécution de commandes Shell/PowerShell avec liste blanche n'est pas implémentée (les diagnostics sont des fonctions Python). 
- La récupération de la base SAM n'est pas réalisée (conformément à la version sécurisée du sujet).

## 11. Conclusion
Le développement du client Windows a permis de mettre en place les bases de la communication TCP, de la transmission JSON, des diagnostics système, de la capture d'écran et de la gestion des erreurs.
Les 16 tests unitaires ont été validés. Le client est prêt pour l'intégration finale.