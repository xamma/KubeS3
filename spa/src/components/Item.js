import React from 'react'

const Item = (props) => {
  return (
    <div className='item--card'>
      <div className='item--container'>
        <h3>File Name: {props.filename}</h3>
        <p>Uploaded: {props.uploaded}</p>
        <p>Size: {props.size}</p>
      </div>
    </div>
  )
}

export default Item