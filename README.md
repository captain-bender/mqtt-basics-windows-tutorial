# MQTT Tutorial on Windows 11  
## Eclipse Mosquitto Broker + Python venv + Paho MQTT

This repo is a minimal, step-by-step tutorial for **Windows** that shows how to:

1. Create and use a **Python virtual environment** (`venv`).
2. Install and run the **Eclipse Mosquitto** MQTT broker.
3. Use the **Paho MQTT** Python client library.
4. Exchange basic messages between:
   - one **subscriber** (listening), and  
   - one **publisher** (sending messages).
5. Experiment with **QoS levels** and **retained messages** in MQTT.

This tutorial assumes **no prior MQTT experience** and only very basic command-line familiarity.

---

## 1. Prerequisites

### 1.1. Install Python 3

1. Go to the official Python downloads page and install **Python 3.x for Windows**.
2. During installation, **check** the box:
   - `Add python.exe to PATH`
3. After installation, open **Command Prompt** and check:

```bash
python --version
```

You should see something like:

```text
Python 3.11.x
```

If you see an error, close and reopen Command Prompt and try again.

---

## 2. Clone or download this repository

You can either:

- **Clone with Git**:

```bash
git clone https://github.com/captain-bender/mqtt-basics-windows-tutorial
cd mqtt-basics-windows-tutorial
```

or

- **Download as ZIP** from GitHub, unzip it, and then open Command Prompt **inside the unzipped folder**.

All the following commands assume you are inside the project folder.

---

## 3. Create and activate a virtual environment (venv)

A virtual environment keeps the Python packages for this project isolated.
Please call the following command inside the project's folder.

### 3.1. Create the venv

```bash
python -m venv .venv
```

This creates a folder called `.venv` in the current directory.

### 3.2. Activate the venv (Windows)

```bash
.venv\Scripts\activate
```

If activation worked, your prompt should look similar to:

```text
(.venv) C:\path\to\mqtt-windows-tutorial>
```

Whenever you see `(.venv)` at the beginning of your prompt, it means the virtual environment is active.

To **deactivate** it later, you can run:

```bash
deactivate
```

---

## 4. Install Python dependencies (Paho MQTT)

With the virtual environment **activated**, run:

```bash
pip install -r requirements.txt
```

This will install the [Paho MQTT](https://pypi.org/project/paho-mqtt/) client library required by the example scripts.

You can verify:

```bash
pip list
```

You should see `paho-mqtt` in the list.

---

## 5. Install Eclipse Mosquitto MQTT broker (Windows)

Mosquitto is the **MQTT broker** (the "server" that routes messages between clients).

1. Download the **Windows installer** for *Eclipse Mosquitto* from the official website.
2. Run the installer and accept the defaults (you can install it as a service, but for this tutorial we’ll run it from the command line so you can see the logs).

After installation, Mosquitto is usually available in:

```text
C:\Program Files\mosquitto
```

or a similar folder.

You may want to add that folder to your **PATH** or just refer to it directly in commands.

---

## 6. Use the included Mosquitto config

From version 2.0 onward, Mosquitto is more restrictive by default.  
To keep things simple for a local tutorial, this repo includes a minimal config file that:

- listens on port **1883** (the default MQTT port), and  
- allows **anonymous** local connections.

> **Important:** This is fine for a local tutorial, but **not recommended for production**.

The config file is in:

```text
mosquitto/mosquitto.conf
```
The provided one is a template. You can rename it and create a new one with just 2 lines of code as it is the following (example [mosquitto.conf](./mosquitto.conf)):
It contains:

```conf
listener 1883
allow_anonymous true
```

---

## 7. Start the Mosquitto broker

Open a **new** Command Prompt window (so it’s separate from your Python venv), and run:

```bash
cd "C:\Program Files\mosquitto"
& "C:\Program Files\mosquitto\mosquitto.exe" -c "C:\Program Files\mosquitto\mosquitto.conf" -v
```

Replace `C:\path\to\your\project\...` with the actual path to this repository on your machine.

- `-c` tells Mosquitto which configuration file to use.
- `-v` enables **verbose** logging so you can see connections and messages.

You should now see Mosquitto output like:

```text
... mosquitto version x.x.x starting
... Opening ipv4 listen socket on port 1883.
```

Leave this window **open**. The broker must keep running.

---

## 8. Basic example: subscriber (listener)

In the window where your virtual environment is active (`(.venv)`), from the project root run:

```bash
python src/subscriber.py
```

You should see something like:

```text
[SUBSCRIBER] Connecting to broker at localhost:1883...
[SUBSCRIBER] Connected with result code 0
[SUBSCRIBER] Subscribed to topic: test/topic
Waiting for messages... Press Ctrl+C to exit.
```

Leave this running.

---

## 9. Basic example: publisher (sender)

Open **another** Command Prompt window, go to the project folder, and activate the virtual environment again:

```bash
cd path\to\mqtt-windows-tutorial
.venv\Scripts\activate
python src/publisher.py
```

You should see:

```text
[PUBLISHER] Connecting to broker at localhost:1883...
[PUBLISHER] Connected with result code 0
[PUBLISHER] Publishing message 1: Hello MQTT! (#1)
[PUBLISHER] Publishing message 2: Hello MQTT! (#2)
...
```

On the **subscriber** window, you should see:

```text
[SUBSCRIBER] Message received!
    Topic: test/topic
    Payload: Hello MQTT! (#1)
[SUBSCRIBER] Message received!
    Topic: test/topic
    Payload: Hello MQTT! (#2)
...
```

---

## 10. QoS and retained examples (separate scripts)

The basic example uses **QoS 0** and **non-retained** messages.  
To explore more MQTT features, this repo includes:

- `src/qos_retained_subscriber.py`
- `src/qos_retained_publisher.py`

These demonstrate:

- QoS 0, 1, and 2
- Retained messages

### 10.1. Run the QoS + retained subscriber

In a terminal with the virtual environment active:

```bash
python src/qos_retained_subscriber.py
```

Expected output (simplified):

```text
[QOS-SUB] Connecting to broker at localhost:1883...
[QOS-SUB] Connected with result code 0
[QOS-SUB] Subscribed to test/+/qos with QoS 2
[QOS-SUB] Subscribed to test/retained with QoS 2
Waiting for messages... Press Ctrl+C to exit.
```

This subscriber listens on:

- `test/+/qos`  → will match `test/0/qos`, `test/1/qos`, `test/2/qos`
- `test/retained`

For every received message it prints:

- the topic,
- the payload,
- the **QoS** used to deliver the message,
- whether the message is **retained** or not.

### 10.2. Run the QoS + retained publisher

In another terminal (with venv active):

```bash
python src/qos_retained_publisher.py
```

Expected behaviour:

- Publishes **three messages** on:
  - `test/0/qos` with QoS 0
  - `test/1/qos` with QoS 1
  - `test/2/qos` with QoS 2
- Publishes **one retained message** on:
  - `test/retained` with QoS 1 and `retain=True`

On the subscriber window you will see each message come in with its QoS, and you can check the `retained` flag in the output.

---

## 11. Testing the retained message

To see the effect of a retained message clearly:

1. Make sure the broker is running.
2. Run the **retained publisher** once:

   ```bash
   python src/qos_retained_publisher.py
   ```

   This sets a retained message on `test/retained`.

3. Stop any existing QoS subscriber (Ctrl + C).
4. Now **start the QoS subscriber** again:

   ```bash
   python src/qos_retained_subscriber.py
   ```

Notice that **immediately after subscribing**, the subscriber will receive the **retained** message, even though the publisher is no longer running.

The output will say something like:

```text
[QOS-SUB] Message received
    Topic: test/retained
    Payload: This is a retained status message.
    QoS: 1
    Retained: True
```

That is the key idea of retained messages:  
the broker keeps the **last retained message** on a topic and delivers it instantly to **new subscribers**.

---

## 12. Stopping everything

- To stop the **publisher scripts**: go to their window and press `Ctrl + C`.
- To stop the **subscriber scripts**: go to their window and press `Ctrl + C`.
- To stop the **broker** (Mosquitto): go to the Mosquitto window and press `Ctrl + C`.

---

## 13. Troubleshooting

**1. `ModuleNotFoundError: No module named 'paho'`**

- Make sure your **virtual environment is activated** (`(.venv)` visible in the prompt).
- Run:

```bash
pip install -r requirements.txt
```

**2. `Connection Refused` error in Python clients**

- Check that Mosquitto is running and listening:
  - Is the Mosquitto window open with no obvious errors?
  - Did you pass the correct path to `mosquitto.conf`?

- Confirm the broker is listening on port 1883 with this config:
  - `listener 1883`
  - `allow_anonymous true`

**3. Port 1883 already in use**

- Maybe you have another MQTT broker or service using this port.
- You can change the port number in `mosquitto/mosquitto.conf`, e.g.:

```conf
listener 1884
allow_anonymous true
```

- Then update the Python scripts to use port `1884`.

---

## 14. How this example works (in simple terms)

- The **Mosquitto broker** is the **middleman** that receives and routes messages.
- The **subscriber** tells the broker:  
  “I am interested in messages on topic `test/topic` (or similar).”
- The **publisher** sends messages to the broker on that topic.
- The broker forwards those messages to any client subscribed to that topic.

QoS levels change **how hard MQTT tries to deliver** a message:

- **QoS 0** – *at most once*: fire-and-forget, no acknowledgement.
- **QoS 1** – *at least once*: the broker will retry until it knows the client got it (can result in duplicates).
- **QoS 2** – *exactly once*: more expensive handshake to ensure no duplicates.

Retained messages let the broker remember the **last known value** for a topic and give it immediately to new subscribers.

This pattern is called **publish/subscribe**, and it’s very popular in IoT and distributed systems.

## Windows Users: Mosquitto Running as a Background Service (Port Conflict)

On Windows, the Mosquitto installer may automatically start the broker **as a background service**.  
This means port **1883** is already in use when you try to run your own broker manually.

If this happens, you’ll see:

```
Error: Only one usage of each socket address is normally permitted.
```

This means **port 1883 is already taken**.

You can fix this using one of the following options.

---

Open **PowerShell as Administrator**:

```powershell
Get-Service mosquitto
```

If it shows `Running`, stop it:

```powershell
Stop-Service mosquitto
```

Or:

```powershell
net stop mosquitto
```

Prevent auto-start:

```powershell
Set-Service -Name mosquitto -StartupType Manual
```

Now you can safely start your own visible broker:

```powershell
& "C:\Program Files\mosquitto\mosquitto.exe" -c "PATH_TO_PROJECT\mosquitto\mosquitto.conf" -v
```
