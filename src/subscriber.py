import time
import paho.mqtt.client as mqtt

BROKER_HOST = "localhost"
BROKER_PORT = 1883
TOPIC = "test/topic"


def on_connect(client, userdata, flags, rc):
    """Callback when the client receives a CONNACK response from the server."""
    print(f"[SUBSCRIBER] Connected with result code {rc}")
    client.subscribe(TOPIC)
    print(f"[SUBSCRIBER] Subscribed to topic: {TOPIC}")


def on_message(client, userdata, msg):
    """Callback when a PUBLISH message is received from the server."""
    print("[SUBSCRIBER] Message received!")
    print(f"    Topic: {msg.topic}")
    print(f"    Payload: {msg.payload.decode('utf-8')}")


def main():
    print(f"[SUBSCRIBER] Connecting to broker at {BROKER_HOST}:{BROKER_PORT}...")

    # Create MQTT client instance
    client = mqtt.Client(client_id="python-subscriber")

    # Attach callback functions
    client.on_connect = on_connect
    client.on_message = on_message

    # Connect to the broker
    client.connect(BROKER_HOST, BROKER_PORT, keepalive=60)

    print("Waiting for messages... Press Ctrl+C to exit.")

    # Blocking call that processes network traffic, dispatches callbacks, and
    # handles reconnecting.
    client.loop_forever()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[SUBSCRIBER] Exiting...")
        time.sleep(0.5)
