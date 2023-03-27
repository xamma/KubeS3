import React from 'react';

const Delete = () => {
  const [objectName, setObjectName] = React.useState('');
  const [message, setMessage] = React.useState(null);

  const handleObjectNameChange = (e) => {
    setObjectName(e.target.value);
  }

  const handleObjectDelete = (e) => {
    e.preventDefault();

    fetch(`/api/delete/${objectName}`, {
      method: 'DELETE'
    })
      .then(response => {
        if (!response.ok) {
          throw new Error('Error deleting object');
        }
        setMessage(`Successfully deleted object ${objectName}.`);
        setObjectName('');
        setTimeout(() => setMessage(null), 3000);
      })
      .catch(error => {
        console.error(error);
        setMessage('An error occurred.');
      });
  }
  
  return (
    <div className='delete--view'>
      <h1>Delete Object from S3</h1>
      <form className='delete--form' onSubmit={handleObjectDelete}>
        <input className='delete--input' type="text" placeholder="Enter object name" value={objectName} onChange={handleObjectNameChange} />
        <button className='delete--button' type="submit">Delete Object</button>
      </form>
      {message && <p>{message}</p>}
    </div>
  );  
};

export default Delete;
