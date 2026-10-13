"""Connection settings shared by all the example scripts.

Change the values here once, and every script uses them.

Sections 1-14 of the README use the open broker (mosquitto/mosquitto.conf),
so leave USERNAME and PASSWORD as None.

Section 15 switches to the password-protected broker
(mosquitto/mosquitto_secure.conf). Then set USERNAME and PASSWORD to the user
you created with mosquitto_passwd, for example:

    USERNAME = "alice"
    PASSWORD = "the password you typed for alice"
"""

BROKER_HOST = "localhost"
BROKER_PORT = 1883

USERNAME = None
PASSWORD = None