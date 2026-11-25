
import socket
import platform
import subprocess


def get_hostname():
    """Récupère le nom de la machine."""
    return socket.gethostname()


def get_os():
    """Récupère le système d'exploitation."""
    return platform.system() + " " + platform.release()


def get_architecture():
    """Récupère l'architecture."""
    return platform.machine()


def get_network():
    """Récupère les interfaces IPv4."""
    try:
        result = subprocess.run(
            ["ip", "-o", "-4", "addr", "show", "scope", "global"],
            capture_output=True,
            text=True,
            check=True,
            timeout=5
        )

        return result.stdout

    except (OSError, subprocess.SubprocessError) as error:
        return f"Erreur réseau : {error}"


def get_system_info():
    """Regroupe les informations système."""
    return {
        "hostname": get_hostname(),
        "os": get_os(),
        "architecture": get_architecture(),
        "network": get_network()
    }
