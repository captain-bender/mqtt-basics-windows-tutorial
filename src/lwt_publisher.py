import os
import time

import paho.mqtt.client as mqtt

from mqtt_settings import BROKER_HOST, BROKER_PORT, USERNAME, PASSWORD

STATUS_TOPIC = "test/status"


def on_connect(client, userdata, flags, reason_code, properties):
    """Called when the broker answers our connection request (CONNACK)."""
    if reason_code.is_failure:
        print(f"[LWT-PUB] Connection refused: {reason_code}")
        client.disconnect()
        return
    print(f"[LWT-PUB] Connected: {reason_code}")
    # Tell everyone we are online. Retained, so late subscribers see it too.
    client.publish(STATUS_TOPIC, payload="online", qos=1, retain=True)


def main():
    print(f"[LWT-PUB] Connecting to broker at {BROKER_HOST}:{BROKER_PORT}...")

    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="python-lwt-publisher")
    if USERNAME:
        client.username_pw_set(USERNAME, PASSWORD)
    client.on_connect = on_connect

    # The Last Will and Testament must be set BEFORE connecting: it is sent to
    # the broker inside the CONNECT packet. The broker publishes it for us only
    # if we disappear without a clean disconnect.
    client.will_set(STATUS_TOPIC, payload="offline (connection lost)", qos=1, retain=True)

    print(f"[LWT-PUB] Running with process ID {os.getpid()}.")
    print("[LWT-PUB] Press Ctrl+C for a CLEAN stop, or kill this process to trigger the LWT.")

    client.connect(BROKER_HOST, BROKER_PORT, keepalive=60)
    client.loop_start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        # Clean stop: we say goodbye ourselves and disconnect properly,
        # so the broker throws the will away and does NOT publish it.
        print("\n[LWT-PUB] Clean stop...")
        info = client.publish(STATUS_TOPIC, payload="offline (clean stop)", qos=1, retain=True)
        info.wait_for_publish(timeout=5)
        client.disconnect()
        client.loop_stop()
        print("[LWT-PUB] Disconnected from broker.")


if __name__ == "__main__":
    main()
