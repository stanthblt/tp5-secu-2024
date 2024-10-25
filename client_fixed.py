import socket
import sys
import re
import logging

# Configuration du logger pour la console et le fichier
class CustomFormatter(logging.Formatter):
    red = "\x1b[31;20m"
    reset = "\x1b[0m"
    
    FORMATS = {
        logging.ERROR: red + "%(levelname)s %(asctime)s %(message)s" + reset,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno) 
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

try:
    # Création et configuration du logger
    logger = logging.getLogger("bs_server")
    logger.setLevel(logging.DEBUG)
    c_handler = logging.StreamHandler()
    f_handler = logging.FileHandler('/var/log/bs_client/bs_client.log')
    c_handler.setLevel(logging.ERROR)
    f_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    c_handler.setFormatter(CustomFormatter())
    f_handler.setFormatter(formatter)
    logger.addHandler(c_handler)
    logger.addHandler(f_handler)
except Exception as e:
    print(f"Failed to configure logging: {e}")
    sys.exit(1)

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('10.1.1.11', 13337))
    logger.info("Connexion réussie à %s:%s", '10.1.1.11', 13337)
    s.send("Ok".encode())
    data = s.recv(1024)
    logger.info(f"Réponse reçue du serveur : {repr(data)}")
    
    userMessage = input("Veuillez saisir une opération arithmétique : ")

    # Validation stricte de l'expression arithmétique
    pattern = r'^(-?\d{1,5})\s*([+*/-])\s*(-?\d{1,5})$'
    match= re.match(pattern, userMessage)
    if match:
        num1, operator, num2 = match.groups()
        num1, num2 = int(num1), int(num2)

        if -100000 <= num1 <= 100000 and -100000 <= num2 <= 100000:
            s.sendall(userMessage.encode("utf-8"))
            logger.info("Message envoyé au serveur : %s", userMessage)
        else:
            raise ValueError("Les nombres doivent être entre -100000 et +100000.")
    else:
        raise ValueError("Format invalide. Utilisez seulement des entiers et les opérateurs (+, -, *, /).")
    
    # Réception et affichage du résultat
    data = s.recv(1024)
    s.close()
    logger.info(f"Réponse reçue du serveur : {repr(data)}")
    print(repr(data.decode()))
    sys.exit(0)
except socket.error as e :
    logger.error("Impossible de se connecter au serveur.")
    s.close()
    sys.exit(1)
