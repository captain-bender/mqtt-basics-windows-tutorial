import time

import paho.mqtt.client as mqtt

from mqtt_settings import BROKER_HOST, BROKER_PORT, USERNAME, PASSWORD

# This subscriber listens to:
# - test/+/qos      (e.g. test/0/qos, test/1/qos, test/2/qos)
# - test/retained   (for the retained message demo)
# - test/status     (for the Last Will and Testament demo)
TOPICS = [
    ("test/+/qos", 2),   # subscribe with QoS 2
    ("test/retained", 2),
    ("test/status", 2),
]


def on_connect(client, userdata, flags, reason_code, properties):
    """Called when the broker answers our connection request (CONNACK)."""
    if reason_code.is_failure:
        print(f"[QOS-SUB] Connection refused: {reason_code}")
        client.disconnect()
        return
    print(f"[QOS-SUB] Connected: {reason_code}")
    for topic, qos in TOPICS:
        client.subscribe(topic, qos=qos)
        print(f"[QOS-SUB] Subscribed to {topic} with QoS {qos}")
    print("Waiting for messages... Press Ctrl+C to exit.")


def on_message(client, userdata, msg):
    """Called when a PUBLISH message is received from the broker."""
    payload = msg.payload.decode("utf-8")
    print("[QOS-SUB] Message received")
    print(f"    Topic: {msg.topic}")
    print(f"    Payload: {payload}")
    print(f"    QoS: {msg.qos}")
    print(f"    Retained: {msg.retain}")
    print("-" * 40)


def main():
    print(f"[QOS-SUB] Connecting to broker at {BROKER_HOST}:{BROKER_PORT}...")

    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="python-qos-subscriber")
    if USERNAME:
        client.username_pw_set(USERNAME, PASSWORD)
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(BROKER_HOST, BROKER_PORT, keepalive=60)
    client.loop_forever()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[QOS-SUB] Exiting...")
        time.sleep(0.5)
