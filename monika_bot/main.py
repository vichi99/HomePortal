import json
import logging
import os
from datetime import datetime, timedelta

import paho.mqtt.client as mqtt
import telebot
from dotenv import load_dotenv

load_dotenv()

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
LOGGER = logging.getLogger(__name__)

# Load settings
AUTH_USERS = json.loads(os.getenv("AUTH_USERS"))
MQTT_USERNAME = os.getenv("MQTT_USERNAME")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD")
MQTT_IP = os.getenv("MQTT_IP")
MQTT_PORT = int(os.getenv("MQTT_PORT"))
MQTT_KEEPALIVE = int(os.getenv("MQTT_KEEPALIVE"))
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
LIMIT_MESSAGE_SECOND = int(os.getenv("LIMIT_MESSAGE_SECOND"))
TOPIC_LED_SET = os.getenv("TOPIC_LED_SET")
TOPIC_LED_STATUS = os.getenv("TOPIC_LED_STATUS")
TOPIC_LED_TIMER_OFF = os.getenv("TOPIC_LED_TIMER_OFF")
TOPIC_LED_TIMER_OFF_STATUS = os.getenv("TOPIC_LED_TIMER_OFF_STATUS")

income_led_status = 0
income_led_timer_off_status = ""
actual_chat_id = 0

LOGGER.info("Starting monika bot")

# make telegram bot
bot = telebot.TeleBot(TELEGRAM_TOKEN)
keyboard = telebot.types.ReplyKeyboardMarkup(True)
keyboard.row("Off", "Status")
keyboard.row("1%", "5%", "50%", "100%")

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    LOGGER.info(f"Connected to mqtt broker. Code: {rc}")

    client.subscribe(TOPIC_LED_STATUS)
    client.subscribe(TOPIC_LED_TIMER_OFF_STATUS)


# The callback for when a PUBLISH message is received from the server.
def on_message(client: mqtt.Client, userdata, msg: mqtt.MQTTMessage):
    global income_led_status, income_led_timer_off_status, actual_chat_id
    if msg.topic == TOPIC_LED_STATUS:
        try:
            income_led_status = int(msg.payload)
            LOGGER.info(f"Income led status: {income_led_status}")
            if actual_chat_id:
                try:
                    bot.send_message(
                        actual_chat_id, f"Successfully led set to {income_led_status}%"
                    )
                    actual_chat_id = 0
                except telebot.apihelper.ApiTelegramException:
                    LOGGER.error(
                        f"Send led value message to telegram failed.",
                        f" Chat ID: {actual_chat_id}",
                        exc_info=True,
                    )
        except ValueError:
            LOGGER.error(f"Value error '{msg.payload}' for topic: {TOPIC_LED_STATUS}")
    elif msg.topic == TOPIC_LED_TIMER_OFF_STATUS:
        try:
            if check_time_format(msg.payload.decode("utf-8")):
                income_led_timer_off_status = msg.payload.decode("utf-8")
                LOGGER.info(f"Income timer of status: {income_led_timer_off_status}")
                if actual_chat_id:
                    try:
                        bot.send_message(
                            actual_chat_id,
                            f"Successfully timer off set to {income_led_timer_off_status}.",
                        )
                        actual_chat_id = 0
                    except telebot.apihelper.ApiTelegramException:
                        LOGGER.error(
                            f"Send timer message to telegram failed.",
                            f" Chat ID: {actual_chat_id}",
                            exc_info=True,
                        )
        except ValueError:
            LOGGER.error(f"Value error '{msg.payload}' for topic: {TOPIC_LED_STATUS}")


def on_disconnect(client, userdata, msg):
    LOGGER.info(f"Disonnected from mqtt broker")


# start client
mqtt_client = mqtt.Client()
mqtt_client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.on_disconnect = on_disconnect
mqtt_client.connect_async(MQTT_IP, MQTT_PORT, MQTT_KEEPALIVE)
mqtt_client.loop_start()


def is_message_old(message: telebot.types.Message) -> bool:
    """
    Compare time at the message with actual time minus `LIMIT_MESSAGE_SECOND`.

    :param message: Income message from telegram.
    :type message: telebot.types.Message
    :return: Return True if message is older then actual time and offset.
    :rtype: bool
    """
    now_minus_offset = datetime.now() - timedelta(seconds=LIMIT_MESSAGE_SECOND)
    message_date = datetime.fromtimestamp(message.date)
    if now_minus_offset < message_date:
        LOGGER.info(f"Message {message.text} is not old {message_date}.")
        return True
    else:
        LOGGER.info(f"Message {message.text} is to old {message_date}.")
        return False


def is_auth_user(message: telebot.types.Message) -> bool:
    """
    Check if user is in the variable `AUTH_USERS`.

    :param message: Income message from telegram.
    :type message: telebot.types.Message
    :return: Return True if user is authorized.
    :rtype: bool
    """
    for key, value in AUTH_USERS.items():
        if message.chat.id == value:
            LOGGER.info(f"User {key} is authorized.")
            return True
    LOGGER.info(
        f"User ID: {message.chat.id}",
        f"Name: {message.chat.first_name} {message.chat.last_name} is not authorized.",
    )
    return False


def set_led_percent(value: int):
    """
    Publish percent value for led`s to mqtt broker.

    :param int value: Percent value.
    """
    mqtt_client.publish(TOPIC_LED_SET, str(value), qos=1, retain=False)
    LOGGER.info(f"Published led percent value to : {value}%.")


def check_already_set_led_value(value: int):
    """
    If sending value and incomed value is the same send message to telegram chat.

    :param int value: Sending percent value for set led.
    """
    if actual_chat_id and income_led_status == value:
        bot.send_message(
            actual_chat_id, f"Led value is already set to {income_led_status}%"
        )


def check_already_set_timer_off(value: str):
    """
    If sending value and incomed value is the same send message to telegram chat.

    :param str value: Sending timer off value for set led.
    """
    if actual_chat_id and income_led_timer_off_status == value:
        bot.send_message(
            actual_chat_id,
            f"Timer off value is already set to {income_led_timer_off_status}%",
        )


def check_time_format(value: str) -> bool:
    """
    Control income time format for set timer switching off led.

    :param str value: String time `5:06`, `23:59`.
    :return: Return True if format is valid
    :rtype: bool
    """
    try:
        hours, minutes = value.split(":")
        assert 1 <= len(hours) <= 2
        assert len(minutes) == 2
        assert 0 <= int(hours) <= 23
        assert 0 <= int(minutes) <= 59
        return True
    except (TypeError, ValueError, AssertionError, AttributeError):
        LOGGER.warning(f"Bad income time format: {value}")
        return False


def set_timer_off(message: telebot.types.Message):
    """
    Handle message for setting timer off on the Monika bed.

    :param message: Income message from telegram.
    :type message: telebot.types.Message
    """
    global actual_chat_id
    actual_chat_id = message.chat.id
    mqtt_client.publish(TOPIC_LED_TIMER_OFF, str(message.text), qos=1, retain=True)
    LOGGER.info(f"Published timer off value to: {message.text}.")
    check_already_set_timer_off(message.text)


def handling_messages(message: telebot.types.Message):
    """
    Handle message for setting's led on the Monika bed.

    :param message: Income message from telegram.
    :type message: telebot.types.Message
    """
    global actual_chat_id

    if message.text.lower() == "off":
        actual_chat_id = message.chat.id
        set_led_percent(0)
        check_already_set_led_value(0)
    elif message.text == "1%":
        actual_chat_id = message.chat.id
        set_led_percent(1)
        check_already_set_led_value(1)
    elif message.text == "5%":
        actual_chat_id = message.chat.id
        set_led_percent(5)
        check_already_set_led_value(5)
    elif message.text == "50%":
        actual_chat_id = message.chat.id
        set_led_percent(50)
        check_already_set_led_value(50)
    elif message.text == "100%":
        actual_chat_id = message.chat.id
        set_led_percent(100)
        check_already_set_led_value(100)
    elif message.text == "Status":
        msg = (
            f"Led: {income_led_status}% ; "
            + f"Timer off: {income_led_timer_off_status}"
            + f"\nPro nastavení vypnutí napíš např. 23:05"
        )

        bot.send_message(message.chat.id, msg)
    elif check_time_format(message.text):
        set_timer_off(message)
    else:
        msg = (
            "Ahoj\n"
            + "Zadán nesprávný příkaz.\n"
            + "Ovládání je pomocí tlačítek níže. Pro nastavení času vypnutí "
            + "napiš konkretní čas např. 15:05",
        )
        bot.send_message(message.chat.id, msg, reply_markup=keyboard)


@bot.message_handler(content_types=["text"])
def send_text(message: telebot.types.Message):
    """
    Handling income text from telegram chat.

    :param message: Income message from telegram.
    :type message: telebot.types.Message
    """
    if not is_auth_user(message) or not is_message_old(message):
        return
    handling_messages(message)


bot.polling()
