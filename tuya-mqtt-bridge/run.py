import tinytuya
import paho.mqtt.client as mqtt
import time

# Gerätekonfiguration
DEVICE_ID = "bf5f0c871e4597465fesgs"
LOCAL_KEY = "!u6PFVH[rA/nAkPQ"
IP_ADDRESS = "20.20.20.53"  # IP der Steckdose

# MQTT-Konfiguration
MQTT_BROKER = "20.20.20.57"
MQTT_PORT = 1883
MQTT_USER = "mqtt_user"
MQTT_PASSWORD = "SuzukiKawasaki2233!"
MQTT_TOPIC_PREFIX = "tuya/steckdose_klipper"

# Tuya-Gerät initialisieren
device = tinytuya.OutletDevice(DEVICE_ID, IP_ADDRESS, LOCAL_KEY)
device.set_version(3.3)

# MQTT initialisieren
client = mqtt.Client()
client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
client.connect(MQTT_BROKER, MQTT_PORT, 60)

def publish_data():
    try:
        data = device.status()
        dps = data.get('dps', {})

        leistung = dps.get(18, 0)  # W
        strom = dps.get(19, 0) / 1000  # mA → A
        spannung = dps.get(20, 0) / 10  # V
        gesamtverbrauch = dps.get(17, 0) / 100.0  # kWh

        client.publish(f"{MQTT_TOPIC_PREFIX}/power", leistung)
        client.publish(f"{MQTT_TOPIC_PREFIX}/current", strom)
        client.publish(f"{MQTT_TOPIC_PREFIX}/voltage", spannung)
        client.publish(f"{MQTT_TOPIC_PREFIX}/energy_total", gesamtverbrauch)

        print(f"Gesendet: {leistung} W, {strom:.3f} A, {spannung:.1f} V, {gesamtverbrauch:.2f} kWh")

    except Exception as e:
        print("Fehler beim Abruf:", e)

while True:
    publish_data()
    time.sleep(30)
