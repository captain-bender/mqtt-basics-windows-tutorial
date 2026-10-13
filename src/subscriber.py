import time

import paho.mqtt.client as mqtt

from mqtt_settings import BROKER_HOST, BROKER_PORT, USERNAME, PASSWORD

TOPIC = "test/topic"


def on_connect(client, userdata, flags, reason_code, properties):
    """Called when the broker answers our connection request (CONNACK)."""
    if reason_code.is_failure:
        # For example "Not authorized" when the username or password is wrong.
        print(f"[SUBSCRIBER] Connection refused: {reason_code}")
        client.disconnect()  # stops loop_forever() below
        return
    print(f"[SUBSCRIBER] Connected: {reason_code}")
    # Subscribing here (not in main) means we subscribe again after a reconnect.
    client.subscribe(TOPIC)
    print(f"[SUBSCRIBER] Subscribed to topic: {TOPIC}")


def on_message(client, userdata, msg):
    """Called when a PUBLISH message is received from the broker."""
    print("[SUBSCRIBER] Message received!")
    print(f"    Topic: {msg.topic}")
    print(f"    Payload: {msg.payload.decode('utf-8')}")


def main():
    print(f"[SUBSCRIBER] Connecting to broker at {BROKER_HOST}:{BROKER_PORT}...")

    # Create the MQTT client. VERSION2 selects the current callback style
    # used by the on_connect and on_message functions above.
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="python-subscriber")
    if USERNAME:
        client.username_pw_set(USERNAME, PASSWORD)

    # Attach callback functions
    client.on_connect = on_connect
    client.on_message = on_message

    # Connect to the broker
    client.connect(BROKER_HOST, BROKER_PORT, keepalive=60)

    print("Waiting for messages... Press Ctrl+C to exit.")

    # Blocking call that processes network traffic, dispatches callbacks and
    # handles reconnecting. It returns after client.disconnect().
    client.loop_forever()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[SUBSCRIBER] Exiting...")
        time.sleep(0.5)
