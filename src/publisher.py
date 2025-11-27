import time
import paho.mqtt.client as mqtt

BROKER_HOST = "localhost"
BROKER_PORT = 1883
TOPIC = "test/topic"


def on_connect(client, userdata, flags, rc):
    """Callback when the client receives a CONNACK response from the server."""
    print(f"[PUBLISHER] Connected with result code {rc}")


def main():
    print(f"[PUBLISHER] Connecting to broker at {BROKER_HOST}:{BROKER_PORT}...")

    # Create MQTT client instance
    client = mqtt.Client(client_id="python-publisher")
    client.on_connect = on_connect

    # Connect to the broker
    client.connect(BROKER_HOST, BROKER_PORT, keepalive=60)

    # Start a background network loop so callbacks work
    client.loop_start()

    try:
        counter = 1
        while True:
            message = f"Hello MQTT! (#{counter})"
            print(f"[PUBLISHER] Publishing message {counter}: {message}")
            client.publish(TOPIC, payload=message, qos=0)
            counter += 1
            time.sleep(2)  # send a message every 2 seconds
    except KeyboardInterrupt:
        print("\n[PUBLISHER] Stopping publisher...")
    finally:
        client.loop_stop()
        client.disconnect()
        print("[PUBLISHER] Disconnected from broker.")


if __name__ == "__main__":
    main()
