import React from 'react'

const About = () => {
  return (
    <div className='about--screen'>
      <h1>About</h1>
      <p>This is a project made with the <b>React.js</b> Framework and made for transfering and sharing knowledge.</p>
      <p>I tried my best to develop this with the best-practices I know as well as an OOP approach.</p>
      <p>The Services are containerized as well, so you can download the images from my Dockerhub and run them locally on Docker.</p>
      <br></br>
      <h3>Check my GitHub for more content</h3>
      <a className="github--link" href="https://github.com/xamma" target="_blank" rel="noreferrer">
        Check my GitHub
      </a>
      <br></br>
      <h3>Visit my personal Website</h3>
      <a className="github--link" href="https://github.com/xamma" target="_blank" rel="noreferrer">
        Visit me
      </a>
    </div>
  )
}

export default About