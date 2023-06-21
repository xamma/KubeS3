import React from 'react'

const Item = (props) => {

  const handleDownload = () => {
    fetch(`/api/download/${props.filename}`)
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        response.blob().then(blob => {
          let url = window.URL.createObjectURL(blob);
          let a = document.createElement('a');
          a.href = url;
          a.download = props.filename;
          a.click();
        });
      })
      .catch(error => {
        console.error('Error downloading file:', error);
        // show error message to user here
      });
  };

  return (
    <div className='item--card'>
      <div className='item--container'>
        <h3>File Name: {props.filename}</h3>
        <img src={props.thumbnailUrl} alt={`Thumbnail for ${props.filename}`} />
        <p>Uploaded: {props.uploaded}</p>
        <p>Size: {props.size}</p>
        <button className='item--download--button' onClick={handleDownload}>Download</button>
      </div>
    </div>
  )
}

export default Item