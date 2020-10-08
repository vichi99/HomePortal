import React from 'react'
import { NavLink } from "react-router-dom"

// styles
import "./TheNavigation.scss"

const TheNavigation = () => {
    return (
        < nav className="navigation" >
            <NavLink to="/" exact>Home</NavLink>
            <NavLink to="/about">About</NavLink>
        </nav >
    )
}

export default TheNavigation
