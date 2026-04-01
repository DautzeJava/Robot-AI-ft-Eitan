import serial
import time

try:
    print("Connexion sur COM3...")
    arduino = serial.Serial(port='COM3', baudrate=9600, timeout=1)
    time.sleep(2) # Attente du reboot de l'Arduino
    print("✅ Connecté !")
except Exception as e:
    print(f"❌ Erreur : {e}")
    exit()

def send_order(order):
    message = order + "\n"
    arduino.write(message.encode()) # Envoi en octets
    time.sleep(0.1)
    response = arduino.readline().decode().strip() # Réception et décodage
    print(f"Robot dit : {response}")

# Boucle principale interactive
while True:
    cmd = input("Commande (GO/STOP/QUIT) : ").upper()
    
    if cmd == "QUIT":
        send_order("QUIT") # On prévient l'Arduino
        print("Fin du programme. Fermeture du port...")
        arduino.close() # Libération du port COM3
        break # Sortie de la boucle
        
    send_order(cmd)

