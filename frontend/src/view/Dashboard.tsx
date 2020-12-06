import React from 'react'
import Room from "../components/dashboard/Room";

// constants
import { TOPICS_ROOM } from "../conf/constants";


const Home = () => {
    return (
        <div className="home">
            {/* {TOPICS_ROOM.map((room, index) => (
                <Room key={index} setting={room} ></Room>
            ))} */}
        </div>
    )
}

export default Home
