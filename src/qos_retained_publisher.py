import time
import paho.mqtt.client as mqtt

BROKER_HOST = "localhost"
BROKER_PORT = 1883


def on_connect(client, userdata, flags, rc):
    """Callback when the client receives a CONNACK response from the server."""
    print(f"[QOS-PUB] Connected with result code {rc}")


def main():
    print(f"[QOS-PUB] Connecting to broker at {BROKER_HOST}:{BROKER_PORT}...")

    client = mqtt.Client(client_id="python-qos-publisher")
    client.on_connect = on_connect

    client.connect(BROKER_HOST, BROKER_PORT, keepalive=60)
    client.loop_start()

    try:
        # Publish three messages with different QoS levels
        messages = [
            ("test/0/qos", "Hello with QoS 0", 0),
            ("test/1/qos", "Hello with QoS 1", 1),
            ("test/2/qos", "Hello with QoS 2", 2),
        ]

        for topic, payload, qos in messages:
            print(f"[QOS-PUB] Publishing to {topic} with QoS {qos}: {payload}")
            client.publish(topic, payload=payload, qos=qos)
            time.sleep(1)

        # Publish a retained message
        retained_topic = "test/retained"
        retained_payload = "This is a retained status message."
        print(f"[QOS-PUB] Publishing RETAINED message to {retained_topic}: {retained_payload}")
        client.publish(retained_topic, payload=retained_payload, qos=1, retain=True)

        print("[QOS-PUB] Done publishing QoS and retained messages.")
    except KeyboardInterrupt:
        print("\n[QOS-PUB] Stopping publisher...")
    finally:
        time.sleep(1)
        client.loop_stop()
        client.disconnect()
        print("[QOS-PUB] Disconnected from broker.")


if __name__ == "__main__":
    main()
