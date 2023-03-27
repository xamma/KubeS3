import React from 'react'
import Item from '../components/Item'

const Home = () => {

  const [data, setData] = React.useState({})

  React.useEffect(() => {
    fetch("/api/get")
      .then(res => res.json())
      .then(data => setData(data))
  }, [])
  console.log(data)

  const objects = data.objects || []

  const apiElements = objects.map((product, id) => {
    return <Item key={id}
      filename={product.filename}
      size={product.size}
      uploaded={product.uploaded}
      />
  })

  return (
    <div className='home--view'>
      <h1>Hostname: {data.hostname}</h1>
      {apiElements}
    </div>
  )
}

export default Home