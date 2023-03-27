import React, { useState } from 'react';

const Upload = () => {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState(null);

  const handleFileInputChange = (e) => {
    setFile(e.target.files[0]);
  }
  const fileInputRef = React.useRef(null);

  const handleFileUpload = (e) => {
    e.preventDefault();
  
    const formData = new FormData();
    formData.append('file', file);
  
    fetch('/api/upload', {
      method: 'POST',
      body: formData
    })
      .then(response => {
        if (!response.ok) {
          throw new Error('Error uploading file');
        }
        setFile(null); // reset file input after upload
        setMessage('File uploaded successfully.');
        setTimeout(() => setMessage(null), 3000); // hide message after 3 seconds
        fileInputRef.current.value = null; // reset file input value
      })
      .catch(error => {
        console.error(error);
        setMessage('An error occurred.');
      });
  }
  
  return (
    <div className='upload--view'>
      <h1>Upload File to S3</h1>
      <form className='upload--form' onSubmit={handleFileUpload}>
        <input className='upload--input' type="file" onChange={handleFileInputChange} ref={fileInputRef} />
        <button className='upload--button' type="submit">Upload File</button>
      </form>
      {message && <p>{message}</p>}
    </div>
  );  
};

export default Upload;
