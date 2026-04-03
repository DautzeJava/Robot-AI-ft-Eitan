import serial
import os
import time
import random
import csv
from datetime import datetime

dataSetLidarOS = 'dataSetLidar.csv'
nouveau_fichier = not os.path.exists(dataSetLidarOS) or os.stat(dataSetLidarOS).st_size == 0

fichier_txt = open('dataFullSetDev.txt', 'a', encoding='utf-8')
fichier_csv = open('dataSetLidar.csv', 'a', newline='', encoding='utf-8')
csv_writer = csv.writer(fichier_csv)

if nouveau_fichier:
    csv_writer.writerow(['timestamp', 'sensor_type', 'distance'])
    fichier_csv.flush() # On force l'écriture pour être sûr
    print("📝 Nouveau fichier détecté : En-tête ajouté.")

try:
    print("Connexion sur COM3...")
    arduino = serial.Serial(port='COM3', baudrate=9600, timeout=1)
    time.sleep(2) # Attente du reboot de l'Arduino
    print("✅ Connecté !")
    fichier_txt.write(f"--- Session started at : {datetime.now()} ---\n")
    

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
        fichier_txt.write("\nData : " + str(datetime.now()) + " \n")
        for i in range (0, 5) :
            arduino.reset_input_buffer()
            time.sleep(0.1)
            arduino.write(message.encode())
            value = arduino.readline().decode().strip()
        
            if value :
                horodatage = time.time()
                print(f"Value : {value}")
                csv_writer.writerow([horodatage, "LIDAR", value])
                fichier_csv.flush()
                fichier_txt.write(f"Value #{i+1} : {value}\n")
                fichier_txt.flush()

# Boucle principale interactive
while True:
    cmd = input("Commande (GO/STOP/DATA/QUIT/CLEAR) : ").upper()
    
    if cmd == "QUIT":
        send_order("QUIT")
        print("Fermeture...")
        fichier_txt.write(f"Session Stopped at : " + str(datetime.now()) + "\n\n")
        fichier_txt.close()
        fichier_csv.close()
        arduino.close()
        break

    elif cmd == "CLEAR":
        # 1. Fermeture des fichiers en cours
        fichier_txt.close()
        fichier_csv.close()
        # 2. Vidage des fichiers (ATTENTION : ajout de .txt ici)
        open('dataFullSetDev.txt', 'w', encoding='utf-8').close() 
        open('dataSetLidar.csv', 'w', encoding='utf-8').close()
        # 3. Réouverture propre
        fichier_txt = open('dataFullSetDev.txt', 'a', encoding='utf-8') 
        fichier_csv = open('dataSetLidar.csv', 'a', newline='', encoding='utf-8')
        csv_writer = csv.writer(fichier_csv)
        # 4. RÉÉCRITURE DE L'EN-TÊTE ICI
        csv_writer.writerow(['timestamp', 'sensor_type', 'distance'])
        fichier_csv.flush()
        
        print("✨ Les fichiers sont de nouveau vierges et l'en-tête CSV a été replacé.")
  
    else:
        # Pour GO, STOP et DATA, on envoie à l'Arduino
        send_order(cmd)