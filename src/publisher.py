import time

import paho.mqtt.client as mqtt

from mqtt_settings import BROKER_HOST, BROKER_PORT, USERNAME, PASSWORD

TOPIC = "test/topic"


def on_connect(client, userdata, flags, reason_code, properties):
    """Called when the broker answers our connection request (CONNACK)."""
    if reason_code.is_failure:
        print(f"[PUBLISHER] Connection refused: {reason_code}")
        client.disconnect()
        return
    print(f"[PUBLISHER] Connected: {reason_code}")
    userdata["ready"] = True  # tells main() it can start publishing


def wait_for_connection(userdata, timeout=5.0):
    """Wait until on_connect has run successfully. Returns True or False."""
    end = time.time() + timeout
    while time.time() < end:
        if userdata["ready"]:
            return True
        time.sleep(0.1)
    return False


def main():
    print(f"[PUBLISHER] Connecting to broker at {BROKER_HOST}:{BROKER_PORT}...")

    # Create the MQTT client (VERSION2 = current callback style)
    userdata = {"ready": False}  # shared with on_connect
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="python-publisher", userdata=userdata)
    if USERNAME:
        client.username_pw_set(USERNAME, PASSWORD)
    client.on_connect = on_connect

    # Connect to the broker
    client.connect(BROKER_HOST, BROKER_PORT, keepalive=60)

    # Start a background network loop so callbacks work
    client.loop_start()

    # Only start publishing once the broker has accepted us
    if not wait_for_connection(userdata):
        print("[PUBLISHER] Not connected. Is the broker running? Are the username and password correct?")
        client.loop_stop()
        return

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
        client.disconnect()
        client.loop_stop()
        print("[PUBLISHER] Disconnected from broker.")


if __name__ == "__main__":
    main()
