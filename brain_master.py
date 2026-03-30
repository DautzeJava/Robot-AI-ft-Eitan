import serial
import time

# On essaie de se connecter avec un message d'erreur plus bavard
try:
    print("Tentative de connexion sur COM3...")
    arduino = serial.Serial(port='COM3', baudrate=9600, timeout=1)
    
    # TRÈS IMPORTANT : L'Arduino redémarre quand on se connecte en USB.
    # On doit attendre 2 secondes qu'il finisse son setup() avant d'envoyer un ordre.
    time.sleep(2) 
    
    print("✅ Connexion réussie sur COM3 !")
except Exception as e:
    print(f"❌ ÉCHEC DE CONNEXION : {e}")
    # On arrête le programme proprement si on n'a pas de connexion
    exit() 

def send_order(order):
    message = order + "\n"
    arduino.write(message.encode())
    # Attente d'une réponse courte
    time.sleep(0.1)
    response = arduino.readline().decode().strip()
    print(f"Arduino dit : {response}")

# Boucle principale
while True:
    cmd = input("Commande (GO/STOP) : ")
    send_order(cmd)