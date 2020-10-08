import moment from "moment";

import { TIME_FORMAT } from "../conf/constants";


/**
 * 
 * @param date convert timestamp to string
 */
export const timestampToString = (date: number): string => {
    return moment.unix(date).format(TIME_FORMAT)

}