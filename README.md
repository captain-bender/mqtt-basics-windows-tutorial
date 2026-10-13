# MQTT Tutorial on Windows 11  
## Eclipse Mosquitto Broker + Python venv + Paho MQTT

This repo is a minimal, step-by-step tutorial for **Windows** that shows how to:

1. Create and use a **Python virtual environment** (`venv`).
2. Install and run the **Eclipse Mosquitto** MQTT broker.
3. Use the **Paho MQTT** Python client library.
4. Exchange basic messages between:
   - one **subscriber** (listening), and  
   - one **publisher** (sending messages).
5. Experiment with **QoS levels**, **retained messages** and the **Last Will and Testament (LWT)**.
6. Protect the broker with **usernames, passwords** and an **access control list (ACL)**.

This tutorial assumes **no prior MQTT experience** and only very basic command-line familiarity.

Tested with Python 3.13, Eclipse Mosquitto 2.0 and paho-mqtt 2.1.
The tutorial is written for Windows; section 17 lists the differences for macOS and Ubuntu.

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
Python 3.13.x
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

All the following commands assume you are inside the project folder (the one that contains this `README.md`).

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
(.venv) C:\path\to\mqtt-basics-windows-tutorial>
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

You should see `paho-mqtt` with version **2.1 or newer**.
If you see `1.6.1`, you are using an old environment: run `pip install --upgrade paho-mqtt`.

---

## 5. Install Eclipse Mosquitto MQTT broker (Windows)

Mosquitto is the **MQTT broker** (the "server" that routes messages between clients).

1. Download the **Windows installer** for *Eclipse Mosquitto* from the official website.
2. Run the installer and accept the defaults (you can install it as a service, but for this tutorial we'll run it from the command line so you can see the logs).

After installation, Mosquitto is usually available in:

```text
C:\Program Files\mosquitto
```

or a similar folder.

You may want to add that folder to your **PATH** or just refer to it directly in commands.

---

## 6. The broker configuration files

From version 2.0 onward, Mosquitto only accepts connections from the same
computer unless a configuration file says otherwise. This repo includes two
configuration files in the `mosquitto/` folder:

| File | Used in | What it does |
|---|---|---|
| `mosquitto.conf` | sections 7-14 | listens on port **1883** and allows **anonymous** clients |
| `mosquitto_secure.conf` | section 15 | listens on port 1883 and requires a **username and password**, with an **ACL** |

The first one contains just:

```conf
listener 1883
allow_anonymous true
```

> **Important:** allowing anonymous clients is fine for a local tutorial,
> but **not for any real system**. Section 15 shows how to lock the broker down.

---

## 7. Start the Mosquitto broker

Open a **new** terminal window (so it is separate from your Python venv) and
go to the **project folder**, the one that contains `README.md`:

```bash
cd path\to\mqtt-basics-windows-tutorial
```

Then start the broker with the tutorial's configuration file.

In **Command Prompt**:

```bash
"C:\Program Files\mosquitto\mosquitto.exe" -c mosquitto\mosquitto.conf -v
```

In **PowerShell** (note the `&` at the start):

```powershell
& "C:\Program Files\mosquitto\mosquitto.exe" -c mosquitto\mosquitto.conf -v
```

- `-c` tells Mosquitto which configuration file to use.
- `-v` enables **verbose** logging, so you can see every connection and message.

You should now see output like:

```text
... mosquitto version 2.0.x starting
... Config loaded from mosquitto\mosquitto.conf.
... Opening ipv4 listen socket on port 1883.
... mosquitto version 2.0.x running
```

Check that the second line names **this repo's** configuration file. Leave this
window **open**: the broker must keep running.

If you see `Only one usage of each socket address is normally permitted`,
another copy of Mosquitto is already running as a Windows service: see
section 16.3.

---

## 8. Basic example: subscriber (listener)

In the window where your virtual environment is active (`(.venv)`), from the project root run:

```bash
python src/subscriber.py
```

You should see something like:

```text
[SUBSCRIBER] Connecting to broker at localhost:1883...
Waiting for messages... Press Ctrl+C to exit.
[SUBSCRIBER] Connected: Success
[SUBSCRIBER] Subscribed to topic: test/topic
```

Leave this running.

> All the scripts read the broker address, port, username and password from
> `src/mqtt_settings.py`. You only need to change that file in section 15.

---

## 9. Basic example: publisher (sender)

Open **another** Command Prompt window, go to the project folder, and activate the virtual environment again:

```bash
cd path\to\mqtt-basics-windows-tutorial
.venv\Scripts\activate
python src/publisher.py
```

You should see:

```text
[PUBLISHER] Connecting to broker at localhost:1883...
[PUBLISHER] Connected: Success
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
[QOS-SUB] Connected: Success
[QOS-SUB] Subscribed to test/+/qos with QoS 2
[QOS-SUB] Subscribed to test/retained with QoS 2
[QOS-SUB] Subscribed to test/status with QoS 2
Waiting for messages... Press Ctrl+C to exit.
```

This subscriber listens on:

- `test/+/qos`  → will match `test/0/qos`, `test/1/qos`, `test/2/qos`
- `test/retained`
- `test/status` (used in section 14)

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

Now look at the **broker window**. Because the broker runs with `-v`, it logs
every packet it sends and receives. Compare the lines logged for the QoS 0,
QoS 1 and QoS 2 messages: what is different, and why?

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

A retained message stays on the broker until it is replaced or deleted. To
**delete** it, publish an empty retained message to the same topic:

```bash
"C:\Program Files\mosquitto\mosquitto_pub.exe" -t test/retained -r -n
```

(`-r` = retained, `-n` = empty message.) Clearing old retained messages
before a new test keeps the results easy to read.

---

## 12. Stopping everything

- To stop the **publisher scripts**: go to their window and press `Ctrl + C`.
- To stop the **subscriber scripts**: go to their window and press `Ctrl + C`.
- To stop the **broker** (Mosquitto): go to the Mosquitto window and press `Ctrl + C`.

---

## 13. How this example works (in simple terms)

- The **Mosquitto broker** is the **middleman** that receives and routes messages.
- The **subscriber** tells the broker:  
  "I am interested in messages on topic `test/topic` (or similar)."
- The **publisher** sends messages to the broker on that topic.
- The broker forwards those messages to any client subscribed to that topic.

QoS levels change **how hard MQTT tries to deliver** a message:

- **QoS 0** – *at most once*: fire-and-forget, no acknowledgement.
- **QoS 1** – *at least once*: the broker will retry until it knows the client got it (can result in duplicates).
- **QoS 2** – *exactly once*: more expensive handshake to ensure no duplicates.

Retained messages let the broker remember the **last known value** for a topic and give it immediately to new subscribers.

The **Last Will and Testament** is a message the client gives the broker when
it connects. The broker publishes it for the client if the client disappears
without disconnecting properly (section 14).

This pattern is called **publish/subscribe**, and it's very popular in IoT and distributed systems.

---

## 14. Last Will and Testament (LWT)

A client can leave a **will** with the broker when it connects. If the
client later disappears without disconnecting properly (a crash, a power cut,
a lost network), the broker publishes the will for it. Other clients can then
tell that the client has gone.

`src/lwt_publisher.py` sets the will before connecting:

```python
client.will_set("test/status", payload="offline (connection lost)", qos=1, retain=True)
```

It then publishes `online` on `test/status` and waits.

### 14.1 Try it

1. Start the QoS subscriber (it also listens to `test/status`):

   ```bash
   python src/qos_retained_subscriber.py
   ```

2. In another terminal, start the LWT publisher:

   ```bash
   python src/lwt_publisher.py
   ```

   The subscriber shows `online`. Note the **process ID** the publisher prints.

3. **Clean stop:** press `Ctrl + C` in the publisher window. The script
   publishes `offline (clean stop)` itself and disconnects properly, so the
   broker **throws the will away**.

4. Start the publisher again, then stop it **without** a clean disconnect,
   as if it had crashed. In a new terminal:

   ```bash
   taskkill /F /PID <process ID>
   ```

   or end the `python.exe` task in **Task Manager**.

   The subscriber now shows `offline (connection lost)`: the broker published
   the will.

> **Important:** `Ctrl + C` does **not** trigger the will in these scripts,
> because they catch it and disconnect cleanly. To test a will, the client
> must disappear without disconnecting.

Watch the broker window as well: it logs `Will message specified` when the
publisher connects, and what happens to the will when it goes away.

---

## 15. Protecting the broker: usernames, passwords and an ACL

So far, anyone who can reach port 1883 can read and send any message. In this
section, the broker refuses clients that do not log in, and an **access
control list (ACL)** decides which topics each user may use.

Stop the broker from section 7 (`Ctrl + C` in its window) before you start.

### 15.1 Create a password file

From the **project folder**, create the file `mosquitto\passwd` with one user
called `alice`. You will be asked to type her password twice:

```bash
"C:\Program Files\mosquitto\mosquitto_passwd.exe" -c mosquitto\passwd alice
```

- `-c` **creates** the file, replacing any existing one. To add more users
  later, run the command again **without** `-c`.
- Open `mosquitto\passwd`: the password is stored as a hash, not as plain text.

### 15.2 Look at the ACL and the secure configuration

`mosquitto/mosquitto_secure.conf` contains:

```conf
listener 1883
allow_anonymous false
password_file mosquitto/passwd
acl_file mosquitto/acl
```

`mosquitto/acl` gives `alice` read and write access to every topic under
`test/`:

```conf
user alice
topic readwrite test/#
```

`topic read` allows subscribing, `topic write` allows publishing and
`topic readwrite` allows both. Anything the ACL does not allow is denied.
The comments in `mosquitto/acl` explain the format.

### 15.3 Start the secure broker and log in

Start the broker with the secure configuration, from the project folder:

```bash
"C:\Program Files\mosquitto\mosquitto.exe" -c mosquitto\mosquitto_secure.conf -v
```

(In PowerShell, put `&` at the start, as in section 7.)

Now run `python src/subscriber.py`. Because it does not log in yet, you see:

```text
[SUBSCRIBER] Connection refused: Not authorized
```

Open `src/mqtt_settings.py` and set the user you created:

```python
USERNAME = "alice"
PASSWORD = "the password you typed"
```

Every script reads these settings, so sections 8-14 now work again, as `alice`.

### 15.4 See the ACL at work

Publish to a topic **outside** `test/`:

```bash
"C:\Program Files\mosquitto\mosquitto_pub.exe" -u alice -P <password> -t other/topic -m hello -q 1
```

The command appears to succeed, but the broker window shows
`Denied PUBLISH ... 'other/topic'`. The message was dropped. MQTT 3.1.1 has
no way to tell the client, so the broker log is the place to check.

> **Note:** the connection is still **not encrypted**. Usernames, passwords
> and messages cross the network as plain text.

---

## 16. Troubleshooting

### 16.1 `ModuleNotFoundError: No module named 'paho'`

- Make sure your **virtual environment is activated** (`(.venv)` visible in the prompt).
- Run `pip install -r requirements.txt`.

### 16.2 The broker does not start, or the scripts cannot connect

- Is the broker window open and showing `running`, with no errors?
- Did you start the broker **from the project folder**? The configuration
  files use paths such as `mosquitto/passwd` that are relative to the folder
  you start the broker in.
- `Error: Unable to open pwfile` means the password file is missing or the
  broker was started from another folder (section 15.1).

### 16.3 Port 1883 already in use

On Windows, the Mosquitto installer may start the broker **as a background
service**, so port 1883 is already taken when you start your own. You will see:

```text
Error: Only one usage of each socket address is normally permitted.
```

Open **PowerShell as Administrator** and check the service:

```powershell
Get-Service mosquitto
```

If it shows `Running`, stop it and stop it from starting automatically:

```powershell
Stop-Service mosquitto
Set-Service -Name mosquitto -StartupType Manual
```

Alternatively, change `listener 1883` to `listener 1884` in the configuration
file and set `BROKER_PORT = 1884` in `src/mqtt_settings.py`.

### 16.4 `Connection refused: Not authorized`

The broker requires a login (you are using `mosquitto_secure.conf`):

- Set `USERNAME` and `PASSWORD` in `src/mqtt_settings.py` (section 15.3).
- Check that the password is the one you typed for `mosquitto_passwd`.

### 16.5 A script keeps reconnecting, or messages go missing

Two running copies of the same script use the same **client ID**. The broker
allows only one connection per client ID, so each copy keeps disconnecting the
other (the broker window shows `already connected, closing old connection`).
Close the extra copy.

### 16.6 `DeprecationWarning: Callback API version 1 is deprecated`

Your own code creates the client the old way. Use:

```python
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="...")
```

and the new callback arguments shown in the example scripts.

---

## 17. Using macOS or Ubuntu

Everything works the same way, apart from installation and paths.

| | Ubuntu | macOS |
|---|---|---|
| Install | `sudo apt install mosquitto mosquitto-clients` | `brew install mosquitto` |
| Stop the broker the installer started | `sudo systemctl stop mosquitto` | `brew services stop mosquitto` (only if you started it) |
| Start the tutorial broker (from the project folder) | `mosquitto -c mosquitto/mosquitto.conf -v` | `$(brew --prefix)/sbin/mosquitto -c mosquitto/mosquitto.conf -v` |
| Create the password file | `mosquitto_passwd -c mosquitto/passwd alice` | same |
| Activate the venv | `source .venv/bin/activate` | same |
| Kill a script ungracefully (section 14) | `kill -9 <process ID>` | same |

- Use `python3` instead of `python` if `python` is not found.
- Start the broker as your normal user, **not** with `sudo`. A broker started
  as root switches to the `mosquitto` user, which cannot read files in your
  home folder.
- Mosquitto may warn that `passwd` or `acl` are readable by other users. Fix
  it with `chmod 600 mosquitto/passwd mosquitto/acl`.
