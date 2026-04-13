import serial
import os
import sys
import io
import time
import csv
from datetime import datetime

# --- Configuration des fichiers ---
file_txt = 'dataFullSetDev.txt'
file_lidar = 'dataSetLidar.csv'
file_accel = 'dataSetAcc.csv'

def initialiser_fichiers(mode='a'):
    """Crée ou réinitialise les fichiers et ajoute les en-têtes si nécessaire."""
    # En-têtes pour les CSV
    if not os.path.exists(file_lidar) or mode == 'w' or os.stat(file_lidar).st_size == 0:
        with open(file_lidar, mode, newline='', encoding='utf-8') as f:
            csv.writer(f).writerow(['timestamp', 'sensor_type', 'distance'])
            
    if not os.path.exists(file_accel) or mode == 'w' or os.stat(file_accel).st_size == 0:
        with open(file_accel, mode, newline='', encoding='utf-8') as f:
            csv.writer(f).writerow(['timestamp', 'acc_x', 'acc_y', 'acc_z'])

    # Ouverture des flux globaux
    f_txt = open(file_txt, 'a', encoding='utf-8')
    f_lidar = open(file_lidar, 'a', newline='', encoding='utf-8')
    f_accel = open(file_accel, 'a', newline='', encoding='utf-8')
    
    return f_txt, f_lidar, f_accel, csv.writer(f_lidar), csv.writer(f_accel)

# Initialisation au démarrage
initialiser_fichiers() # Assure que les fichiers existent
fichier_txt, fichier_lidar, fichier_accel, writer_lidar, writer_accel = initialiser_fichiers()

if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

try:
    print("Connexion sur COM4...")
    arduino = serial.Serial(port='COM4', baudrate=115200, timeout=1)
    
    
    # Attente du SYSTEM_READY
    print("⏳ Attente du réveil de l'Arduino...")
    while True:
        line = arduino.readline().decode('utf-8', errors='ignore').strip()
        if "SYSTEM_READY" in line:
            print("✅ Robot prêt et connecté !")
            break
            
    fichier_txt.write(f"--- Session started at : {datetime.now()} ---\n")
    fichier_txt.flush()

except Exception as e:
    print(f"❌ Erreur de connexion : {e}")
    exit()

def traiter_data(raw_str):
    """Découpe la ligne de l'Arduino et enregistre dans les 3 fichiers."""
    if "," in raw_str:
        parts = raw_str.split(",")
        if len(parts) >= 5:
            ts = time.time()
            dist = parts[1]
            ax, ay, az = parts[2], parts[3], parts[4]
            
            # 1. Sauvegarde CSV
            writer_lidar.writerow([ts, "LIDAR", dist])
            writer_accel.writerow([ts, ax, ay, az])
            
            # 2. Sauvegarde Texte
            fichier_txt.write(f"[{datetime.now().strftime('%H:%M:%S')}] Lidar:{dist}mm | Acc:[{ax},{ay},{az}]\n")
            
            # 3. Flush (Sécurité)
            fichier_lidar.flush()
            fichier_accel.flush()
            fichier_txt.flush()
            
            print(f"💾 Enregistré : L:{dist}mm | Z:{az}")
    else:
        print(f"🤖 Robot dit : {raw_str}")

# --- Boucle principale ---
while True:
    cmd = input("\nCommande (GO/STOP/DATA/QUIT/CLEAR) : ").upper()
    
    if cmd == "QUIT":
        arduino.write("STOP\n".encode())
        print("Fermeture propre...")
        fichier_txt.write(f"--- Session ended at : {datetime.now()} ---\n\n")
        # Fermeture de tout
        for f in [fichier_txt, fichier_lidar, fichier_accel]: f.close()
        arduino.close()
        break

    elif cmd == "CLEAR":
        # 1. On écrit la fin de la session actuelle AVANT de tout effacer
        fichier_txt.write(f"--- Session ended by CLEAR at : {datetime.now()} ---\n")
        
        # 2. Fermeture des flux pour pouvoir manipuler les fichiers
        for f in [fichier_txt, fichier_lidar, fichier_accel]: f.close()
        
        # 3. Vidage des fichiers (mode 'w' pour repartir à zéro)
        open(file_txt, 'w', encoding='utf-8').close() 
        
        # 4. Réinitialisation complète (réouverture et en-têtes)
        fichier_txt, fichier_lidar, fichier_accel, writer_lidar, writer_accel = initialiser_fichiers(mode='w')
        
        # 5. On marque le début de la nouvelle session "propre"
        fichier_txt.write(f"--- New Session started (after CLEAR) at : {datetime.now()} ---\n")
        fichier_txt.flush()
        
        print("✨ Fichiers réinitialisés et horodatages conservés dans le nouveau log.")
    else:
        # Envoi de la commande à l'Arduino
        arduino.write((cmd + "\n").encode())
        time.sleep(0.4) # Temps de traitement
        
        while arduino.in_waiting > 0:
            raw = arduino.readline().decode('utf-8', errors='ignore').strip()
            if raw:
                traiter_data(raw)