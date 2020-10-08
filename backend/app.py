from flask import Flask
from flask_mqtt import Mqtt


app = Flask(__name__)
app.config['MQTT_BROKER_URL'] = '192.168.100.101'  # use the free broker from HIVEMQ
app.config['MQTT_BROKER_PORT'] = 1883  # default port for non-tls connection
app.config['MQTT_USERNAME'] = ''  # set the username here if you need authentication for the broker
app.config['MQTT_PASSWORD'] = ''  # set the password here if the broker demands authentication
app.config['MQTT_KEEPALIVE'] = 5  # set the time interval for sending a ping to the broker to 5 seconds
app.config['MQTT_TLS_ENABLED'] = False  # set TLS to disabled for testing purposes
mqtt = Mqtt(app)

@app.route("/")
def view_welcome_page():
    # return render_template("welcome_page.jinja")
    return 'Hello, World!'

@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    print("#Handle Connect")
    mqtt.subscribe('testik')

@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    data = dict(
        topic=message.topic,
        payload=message.payload.decode()
    )
    print(f"client: {client}")
    print(f"userdata: {userdata}")
    print(f"data: {data}")

