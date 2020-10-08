import { SubcriberRoom } from "../types";

export const TIME_FORMAT = "HH:mm:ss"

export const MQTT_HOST: string = 'ws://localhost:9001'

/**
 * Setting Rooms for make component
 */
const janRoom: SubcriberRoom = {
    name: "Pokoj Jan",
    topicTemp: "room/jan/temperature",
    topicTempOpt: { qos: 1, rap: true },
    topicHum: "room/jan/humidity",
    topicHumOpt: { qos: 1, rap: true },
    topicDev1Status: "room/jan/device1/status",
    topicDev1StatusOpt: { qos: 1, rap: true },
}
/**
 * Add Rooms to topics for describe
 */
export const TOPICS_ROOM: SubcriberRoom[] = [
    janRoom,
]