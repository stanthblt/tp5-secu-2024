import socket
import re

# Fonction de détection de motifs dangereux
def is_malicious(data):
    patterns = [
        r'(__import__|exec|os\.|subprocess|popen|compile|marshal|pickle)',
        r'(\bsh\b|\bbash\b|;|\||&|&&|\bexec\b|\brm\b)',
        r'([\x00-\x08\x0B\x0C\x0E-\x1F\x7F-\x9F]+)'
    ]
    for pattern in patterns:
        if re.search(pattern, data):
            return True
    return False

# Validation du format mathématique (nombres et opérateurs seulement)
def validate_math_expression(expression):
    return bool(re.fullmatch(r'^[\d+\-*/\s]+$', expression))

# Évaluation mathématique sécurisée
def safe_eval(expression):
    pattern = r'^(\d+)\s*([+\-*/])\s*(\d+)$'  # Permet uniquement les opérations de base avec deux opérandes
    match = re.match(pattern, expression)

    if not match:
        return "Erreur : Expression non autorisée"

    num1, operator, num2 = match.groups()
    num1, num2 = int(num1), int(num2)
    
    if operator == '+':
        return num1 + num2
    elif operator == '-':
        return num1 - num2
    elif operator == '*':
        return num1 * num2
    elif operator == '/':
        return num1 / num2 if num2 != 0 else 'Erreur : Division par zéro'
    else:
        return "Erreur : Opérateur invalide"

# Configuration et écoute du serveur
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('0.0.0.0', 13337))
s.listen(1)

print("Le serveur écoute sur le port 13337...")
conn, addr = s.accept()
print(f"Connexion établie avec {addr}")

while True:
    try:
        # Réception et validation du message de bienvenue
        data = conn.recv(1024)
        if not data: 
            break
        print(f"Données reçues du client : {data}")
        conn.send("Hello".encode())

        # Réception de l'expression arithmétique du client
        data = conn.recv(1024)
        expression = data.decode(errors="ignore").strip()  # Ignore les erreurs de décodage

        # Validation de sécurité et de structure du message
        if is_malicious(expression):
            conn.send("Erreur : Contenu non autorisé".encode())
        elif validate_math_expression(expression):
            # Évaluation sécurisée et envoi du résultat
            result = safe_eval(expression)
            conn.send(str(result).encode())
        else:
            conn.send("Erreur : Expression invalide".encode())

    except socket.error:
        print("Erreur de connexion avec le client.")
        break

conn.close()
