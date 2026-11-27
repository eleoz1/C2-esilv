import winreg

try:
    with winreg.OpenKey(
        winreg.HKEY_CURRENT_USER,
        r"Software\ProjetESILV"
    ) as cle:

        valeur, type_valeur = winreg.QueryValueEx(cle, "Test")

        print("Lecture du registre reussie")
        print("Nom : Test")
        print("Valeur :", valeur)

except FileNotFoundError:
    print("Erreur : cle ou valeur introuvable")

except PermissionError:
    print("Erreur : acces refuse")

except OSError as erreur:
    print("Erreur :", erreur)