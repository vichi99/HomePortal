import { IClientSubscribeOptions } from "mqtt";

/**
 * Setting for subscribe data from mqtt to Room component
 */
export interface SubcriberRoom {
    name: string // name for view in component
    topicHum: string
    topicHumOpt: IClientSubscribeOptions
    topicTemp: string
    topicTempOpt: IClientSubscribeOptions
    topicDev1Status: string
    topicDev1StatusOpt: IClientSubscribeOptions

}

/**
 * Format RoomData which will be income from mqtt broker
 */
export interface RoomDataSubscribe {
    date: number
    value: number
}
/**
 * Format DeviceStatus which will be income from mqtt broker
 */
export interface DeviceStatusSubscribe {
    value: boolean
}
