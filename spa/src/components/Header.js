import React from "react"
import { Link, Outlet } from "react-router-dom";
import { FaLayerGroup } from "react-icons/fa"

const Header = () => {

  const HeaderIcon = FaLayerGroup

  //static content
  return (
    <header className="header">
      <HeaderIcon className="header--icon"/>
      <h2 className="header--title">S3 API Frontend</h2>
      <nav className="header--nav">
        <Link to="/">Home</Link> |{" "}
        <Link to="/upload">Upload</Link> |{" "}
        <Link to="/delete">Delete</Link> |{" "}
        <Link to="/about">About</Link>
      </nav>
      {/* for using inside of header component */}
      <Outlet />
      {/* <h4 className="header--version">Version 1.0</h4> */}
    </header>

  )

}

export default Header