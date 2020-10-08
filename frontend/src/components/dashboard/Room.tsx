import React, { useState, useEffect } from 'react'
import { connect, Packet } from 'mqtt';
import ValueLine from "../ValueLine";
import LoaderProgress from "../LoaderProgress";

// constants & types
import { MQTT_HOST } from "../../conf/constants";
import {
    SubcriberRoom, RoomDataSubscribe,
    DeviceStatusSubscribe
} from "../../types";

// styles
import "./Room.scss"

interface Props {
    setting: SubcriberRoom

}

const Room = (props: Props) => {
    const [connected, setConnected] = useState<boolean>(false);
    const [temperature, setTemperature] = useState<number>();
    const [humidity, setHumidity] = useState<number>();
    const [device1Status, setDevice1Status] = useState<boolean>(false);
    const { setting } = props

    useEffect(() => {
        // Anything in here is fired on component mount.
        if (!setting) { return; }
        // connect to mqtt broker
        const client = connect(MQTT_HOST)

        // on connect
        client.on("connect", () => {
            setConnected(true);
            client.subscribe(setting.topicTemp, setting.topicTempOpt);
            client.subscribe(setting.topicHum, setting.topicHumOpt);
            client.subscribe(setting.topicDev1Status, setting.topicDev1StatusOpt);

            const handleMessage = (topic: string, message: string, packet: Packet) => {
                if (setting.topicTemp === topic) {
                    const inData: RoomDataSubscribe = JSON.parse(message.toString());
                    setTemperature(inData.value)
                } else if (setting.topicHum === topic) {
                    const inData: RoomDataSubscribe = JSON.parse(message.toString());
                    setHumidity(inData.value)
                } else if (setting.topicDev1Status === topic) {
                    const status: DeviceStatusSubscribe = JSON.parse(message.toString());
                    setDevice1Status(status.value)
                }
            }

            client.on('message', handleMessage)
        })

        client.on('offline', () => {
            setConnected(false);
        });

        return () => {
            // Anything in here is fired on component unmount.
            client.end()
            setConnected(false);
        }
    }, [setting])

    return (
        <div className="room">
            <h1>{setting.name}</h1>
            { connected ? (
                <div>
                    <ValueLine
                        name="Teplota"
                        value={temperature}
                        unit="°C"
                    ></ValueLine>
                    <ValueLine
                        name="Vlhkost"
                        value={humidity}
                        unit="%"
                    ></ValueLine>
                    Online: {device1Status ? (
                        <span role="img" aria-label="check">✅</span>
                    ) : (
                            <span role="img" aria-label="cross">❌</span>
                        )}
                </div>
            ) : (
                    <div>
                        <LoaderProgress />
                    </div>
                )}
        </div>
    )
}

export default Room
