# Client Windows – Projet C2

## 1. Objectif
Développer un client Windows capable de communiquer avec un serveur Kali Linux via une connexion TCP, d'envoyer des informations système au format JSON et d'exécuter des diagnostics à distance dans un environnement de laboratoire isolé.

## 2. Technologies utilisées
- Python (version 3.13 ou 3.14)
- Socket TCP
- JSON
- PowerShell
- Pillow (pour la capture d'écran)
- VMware Workstation
- Git et GitHub
- Unittest
- Winreg

## 3. Organisation des fichiers
| Fichier | Description |
|---|---|
| `client.py` | Connexion TCP, boucle de commandes, transmission des informations et gestion des erreurs. |
| `diagnostics.py` | Gestion des 10 diagnostics locaux autorisés (dont `EXEC` et `SAM`). |
| `test_client.py` | Exécution des 18 tests unitaires automatisés. |
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
| SCREENSHOT | Capture de l'écran encodée en base64. |
| EXEC | Exécution sécurisée de commandes shell (liste blanche). |
| SAM | Étude de la base SAM et des utilisateurs locaux (sans extraction de hashes). |

## 6. Démarrage automatique
Le client est configuré pour démarrer automatiquement au lancement de la session Windows.
- Un raccourci vers la commande de lancement a été placé dans le dossier `shell:startup`.
- Dès l'ouverture de la VM Windows, le client s'exécute et tente de se connecter au serveur C2.

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
- Commande shell non autorisée.

## 8. Lecture du registre Windows et SAM
Le script `test_registre.py` utilise la bibliothèque `winreg` pour lire une clé de registre de test.
| Paramètre | Valeur |
|---|---|
| Emplacement | `HKEY_CURRENT_USER\Software\ProjetESILV` |
| Nom | Test |
| Type | REG_SZ |
| Valeur | Validation |
| Résultat | Lecture réussie |

Concernant la commande `SAM`, elle vérifie l'existence du fichier `C:\Windows\System32\config\SAM`, liste les utilisateurs locaux via le registre, et documente le fait que les hashes ne sont pas extraits, conformément au cadre éthique du TP.

## 9. Tests réalisés
### 9.1. Tests unitaires
Les tests unitaires sont automatisés à l'aide de la bibliothèque `unittest`.
| Environnement | Tests réussis | Temps d'exécution |
|---|---|---|
| Ordinateur principal | 18/18 | ~0,6 s |
| VM Windows 11 | 18/18 | ~0,6 s |

Taux de réussite des tests unitaires : 100 %.

### 9.2. Tests complémentaires
| Test | Résultat |
|---|---|
| Vérification de la syntaxe Python | Réussi |
| Ping Windows vers Kali | Réussi |
| Connexion TCP avec serveur de test | Réussi |
| Récupération des adresses IPv4 hors localhost | Réussi |
| Création d'une clé de registre de test | Réussi |
| Lecture du registre avec Python | Réussi |
| Capture d'écran et encodage base64 | Réussi |
| Exécution de commandes shell (EXEC) | Réussi |
| Étude de la base SAM | Réussi |
| Exécution manuelle du script de démarrage | Réussi |

## 10. Limites actuelles
- L'exécution de commandes `EXEC` est restreinte à une liste blanche pour des raisons de sécurité.
- L'extraction des hashes de la base SAM n'est pas réalisée (conformément au cadre du TP).
- L'intégration finale dépend du serveur unifié.

## 11. Conclusion
Le développement du client Windows a permis de mettre en place une communication TCP robuste, des diagnostics système, des captures d'écran, l'exécution sécurisée de commandes et l'étude de la base SAM.
Les 18 tests unitaires ont été validés. Le client est prêt pour l'intégration finale.
