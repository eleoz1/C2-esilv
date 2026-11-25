from diagnostics import traiter_demande

commandes = [
    "HELP",
    "HOSTNAME",
    "OS",
    "ARCH",
    "NETWORK",
    "INFO",
    "STATUS",
    "TEST"
]

print("=== Tests des diagnostics ===")

for commande in commandes:
    demande = {
        "type": "diagnostic_request",
        "commande": commande
    }

    print(traiter_demande(demande))

print("\n=== Tests des erreurs ===")

print(traiter_demande("Bonjour"))
print(traiter_demande({}))
print(traiter_demande({"type": "diagnostic_request"}))