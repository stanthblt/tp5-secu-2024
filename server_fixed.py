import socket
import re
import ast

def is_malicious(data):
    patterns = [
        r'(__import__|exec|os\.|subprocess|popen|compile|marshal|pickle)',
        r'(\bsh\b|\bbash\b|;|\||&|&&|\bexec\b|\brm\b)',                  
        r'([\\x00-\\x08\\x0B\\x0C\\x0E-\\x1F\\x7F-\\x9F]+)'          
    ]
    for pattern in patterns:
        if re.search(pattern, data):
            return True
    return False

def validate_math_expression(expression):
    if re.fullmatch(r'^[\d+\-*/\s]+$', expression):
        return True
    return False

def safe_parse(expression):
    """Analyse et évalue l'expression mathématique de manière sécurisée"""
    try:
        node = ast.parse(expression, mode='eval')
        for subnode in ast.walk(node):
            if not isinstance(subnode, (ast.Expression, ast.BinOp, ast.Num, ast.UnaryOp, ast.Add, ast.Sub, ast.Mult, ast.Div)):
                raise ValueError("Expression non autorisée.")
        return eval(compile(node, "<string>", mode="eval"))
    except Exception as e:
        return f"Erreur : {e}"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('0.0.0.0', 13337))
s.listen(1)

print("Le serveur écoute sur le port 13337...")
conn, addr = s.accept()
print(f"Connexion établie avec {addr}")

while True:
    try:
        data = conn.recv(1024)
        if not data: 
            break
        print(f"Données reçues du client : {data}")

        conn.send("Hello".encode())

        data = conn.recv(1024)
        expression = data.decode().strip()

        if is_malicious(expression):
            conn.send("Erreur : Contenu non autorisé".encode())
        elif validate_math_expression(expression):
            result = safe_parse(expression)
            conn.send(str(result).encode())
        else:
            conn.send("Erreur : Expression invalide".encode())

    except socket.error:
        print("Erreur de connexion avec le client.")
        break

conn.close()