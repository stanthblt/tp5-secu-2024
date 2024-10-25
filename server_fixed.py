import socket
import re

# Fonction d'évaluation sécurisée des opérations
def safe_eval(expression):
    pattern = r'^(-?\d+)\s*([+\-*/])\s*(-?\d+)$'
    match = re.match(pattern, expression)

    if match:
        num1, operator, num2 = match.groups()
        num1, num2 = int(num1), int(num2)

        if operator == '+':
            return num1 + num2
        elif operator == '-':
            return num1 - num2
        elif operator == '*':
            return num1 * num2
        elif operator == '/':
            return num1 / num2 if num2 != 0 else 'Erreur: Division par zéro'
    else:
        return "Erreur: Expression invalide"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('0.0.0.0', 13337))
s.listen(1)

print("Le serveur écoute sur le port 13337...")
conn, addr = s.accept()
print(f"Connexion établie avec {addr}")

while True:
    try:
        # Réception du message de bienvenue
        data = conn.recv(1024)
        if not data: break
        print(f"Données reçues du client : {data}")

        conn.send("Hello".encode())

        # Réception de l'opération arithmétique du client
        data = conn.recv(1024)
        expression = data.decode().strip()

        # Évaluation sécurisée et envoi du résultat
        result = safe_eval(expression)
        conn.send(str(result).encode())
         
    except socket.error:
        print("Erreur de connexion avec le client.")
        break

conn.close()
