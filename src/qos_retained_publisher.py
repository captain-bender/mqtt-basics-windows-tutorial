import time

import paho.mqtt.client as mqtt

from mqtt_settings import BROKER_HOST, BROKER_PORT, USERNAME, PASSWORD


def on_connect(client, userdata, flags, reason_code, properties):
    """Called when the broker answers our connection request (CONNACK)."""
    if reason_code.is_failure:
        print(f"[QOS-PUB] Connection refused: {reason_code}")
        client.disconnect()
        return
    print(f"[QOS-PUB] Connected: {reason_code}")
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
    print(f"[QOS-PUB] Connecting to broker at {BROKER_HOST}:{BROKER_PORT}...")

    userdata = {"ready": False}  # shared with on_connect
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="python-qos-publisher", userdata=userdata)
    if USERNAME:
        client.username_pw_set(USERNAME, PASSWORD)
    client.on_connect = on_connect

    client.connect(BROKER_HOST, BROKER_PORT, keepalive=60)
    client.loop_start()

    if not wait_for_connection(userdata):
        print("[QOS-PUB] Not connected. Is the broker running? Are the username and password correct?")
        client.loop_stop()
        return

    try:
        # Publish three messages with different QoS levels.
        # Tip: watch the broker window (started with -v) while this runs.
        messages = [
            ("test/0/qos", "Hello with QoS 0", 0),
            ("test/1/qos", "Hello with QoS 1", 1),
            ("test/2/qos", "Hello with QoS 2", 2),
        ]

        for topic, payload, qos in messages:
            print(f"[QOS-PUB] Publishing to {topic} with QoS {qos}: {payload}")
            info = client.publish(topic, payload=payload, qos=qos)
            info.wait_for_publish(timeout=5)  # returns when the broker has the message
            time.sleep(1)

        # Publish a retained message
        retained_topic = "test/retained"
        retained_payload = "This is a retained status message."
        print(f"[QOS-PUB] Publishing RETAINED message to {retained_topic}: {retained_payload}")
        info = client.publish(retained_topic, payload=retained_payload, qos=1, retain=True)
        info.wait_for_publish(timeout=5)

        print("[QOS-PUB] Done publishing QoS and retained messages.")
    except KeyboardInterrupt:
        print("\n[QOS-PUB] Stopping publisher...")
    finally:
        client.disconnect()
        client.loop_stop()
        print("[QOS-PUB] Disconnected from broker.")


if __name__ == "__main__":
    main()
