import serial
import time
import random
from datetime import datetime

fichier = open('dataTest.txt', 'a')

try:
    print("Connexion sur COM3...")
    arduino = serial.Serial(port='COM3', baudrate=9600, timeout=1)
    time.sleep(2) # Attente du reboot de l'Arduino
    print("✅ Connecté !")
    fichier.write(f"Session Started at : " + str(datetime.now()))
except Exception as e:
    print(f"❌ Erreur : {e}")
    exit()

def send_order(order):
    message = order + "\n"
    arduino.write(message.encode()) # Envoi en octets
    time.sleep(0.1)
    value = 0
    print(f"Robot dit :")

    if cmd == "DATA" :
        print(f"DATA : " + str(datetime.now()))
        fichier.write("\nData : " + str(datetime.now()) + " \n")
        for i in range (0, 5) :
            arduino.reset_input_buffer()
            time.sleep(0.1)
            arduino.write(message.encode())
            value = arduino.readline().decode().strip()
            
            if(value!=None) :
                print(f"Value : {value}")
                fichier.write(f"Value #{i+1} : {value}\n")
                fichier.flush()

# Boucle principale interactive
while True:
    cmd = input("Commande (GO/STOP/DATA/QUIT/CLEAR) : ").upper()
    
    if cmd == "QUIT":
        send_order("QUIT")
        print("Fermeture...")
        fichier.write(f"Session Stopped at : " + str(datetime.now()) + "\n\n")
        fichier.close()
        arduino.close()
        break

    elif cmd == "CLEAR":
        # Procédure de nettoyage du fichier
        fichier.close()
        open('dataTest.txt', 'w').close() # Écrase tout
        fichier = open('dataTest.txt', 'a') # Prêt pour la suite
        print("✨ Le fichier dataTest.txt est de nouveau vierge.")
        # On ne l'envoie pas à l'Arduino car c'est une commande interne au PC
  
    else:
        # Pour GO, STOP et DATA, on envoie à l'Arduino
        send_order(cmd)