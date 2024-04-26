import RPi.GPIO as GPIO
import MFRC522
import signal
import time
import requests
import json

def send_data(uid):
    url = 'http://192.168.0.246/api/pointage'
    headers = {'Content-Type': 'application/json'}
    data = {
        'badgeId': '.'.join(str(x) for x in uid),
        'heureEntree': time.strftime('%Y-%m-%dT%H:%M:%S'),
        'heureSortie': None
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 201:
        print("Pointage enregistré avec succès")
    else:
        print("Erreur lors de l'enregistrement:", response.status_code)

while continue_reading:
    time.sleep(3)
    (status, TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
    if status == MIFAREReader.MI_OK:
        print("Carte detectee")
        (status, uid) = MIFAREReader.MFRC522_Anticoll()
        if status == MIFAREReader.MI_OK:
            print("UID de la carte : " + '.'.join(str(x) for x in uid))
            key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
            MIFAREReader.MFRC522_SelectTag(uid)
            status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 8, key, uid)
            if status == MIFAREReader.MI_OK:
                MIFAREReader.MFRC522_Read(8)
                MIFAREReader.MFRC522_StopCrypto1()
                send_data(uid)
            else:
                print("Erreur d'Authentification")
