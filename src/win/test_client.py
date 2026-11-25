from client import traiter_demande

for commande in ["INFO", "NETWORK", "STATUS", "TEST"]:
    demande = {
        "type": "diagnostic_request",
        "commande": commande
    }

    print(traiter_demande(demande))

print("=== Tests des erreurs ===")

print(traiter_demande("Bonjour"))
print(traiter_demande({}))
print(traiter_demande({"type": "diagnostic_request"}))