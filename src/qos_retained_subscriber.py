import time
import paho.mqtt.client as mqtt

BROKER_HOST = "localhost"
BROKER_PORT = 1883

# This subscriber listens to:
# - test/+/qos      (e.g. test/0/qos, test/1/qos, test/2/qos)
# - test/retained   (for retained message demo)
TOPICS = [
    ("test/+/qos", 2),   # subscribe with QoS 2
    ("test/retained", 2)
]


def on_connect(client, userdata, flags, rc):
    """Callback when the client receives a CONNACK response from the server."""
    print(f"[QOS-SUB] Connected with result code {rc}")
    for topic, qos in TOPICS:
        client.subscribe(topic, qos=qos)
        print(f"[QOS-SUB] Subscribed to {topic} with QoS {qos}")
    print("Waiting for messages... Press Ctrl+C to exit.")


def on_message(client, userdata, msg):
    """Callback when a PUBLISH message is received from the server."""
    payload = msg.payload.decode("utf-8")
    print("[QOS-SUB] Message received")
    print(f"    Topic: {msg.topic}")
    print(f"    Payload: {payload}")
    print(f"    QoS: {msg.qos}")
    print(f"    Retained: {msg.retain}")
    print("-" * 40)


def main():
    print(f"[QOS-SUB] Connecting to broker at {BROKER_HOST}:{BROKER_PORT}...")

    client = mqtt.Client(client_id="python-qos-subscriber")
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
