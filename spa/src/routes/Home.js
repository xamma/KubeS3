import React from 'react'
import Item from '../components/Item'

const Home = () => {
  
  const [loading, setLoading] = React.useState(true)
  const [data, setData] = React.useState({})

  React.useEffect(() => {
    fetch("/api/get")
      .then(res => res.json())
      .then(data => {
        setData(data);
        setLoading(false);
      })
      .catch(error => {
        console.error("Error fetching data:", error);
        setLoading(false);
      });

  }, [])
  // console.log(data)

  // React.useEffect(() => {
  //   // Simulate API fetch
  //   const fakeData = {
  //     hostname: 'example.com',
  //     objects: [
  //       { filename: 'file1.txt', size: '10 KB', uploaded: '2023-06-09' },
  //       { filename: 'file2.jpg', size: '2 MB', uploaded: '2023-06-08' },
  //       { filename: 'file3.pdf', size: '500 KB', uploaded: '2023-06-07' }
  //     ]
  //   };

  //   // Simulate delay before setting the fake data
  //   setTimeout(() => {
  //   // Set the fake data to the state
  //     setData(fakeData);
  //     setLoading(false);
  //   }, 2000); // Simulate a 2-second delay  
  // }, []);

  if (loading) {
    return (
      <div className='home--view'>
        <div className='loading--spinner'></div>
      </div>
    )
  }

  const objects = data.objects || []

  const apiElements = objects.map((object, id) => {
    return <Item
        key={id}
        filename={object.filename}
        size={object.size}
        uploaded={object.uploaded}
      />
  })

  return (
    <div className='home--view'>
      <h1>Hostname: {data.hostname}</h1>
      { apiElements.length !== 0 ?
        apiElements
      : <p className='no--elements'>No elements yet. Try uploading some!</p> }
    </div>
  )
}

export default Home