import { useState, useEffect } from 'react'
import axios from 'axios'
import './App.css'

function App() {
  const [users, setUsers] = useState([])

//   function to fetch data from the API
const fetchData = async () => {
	const response = await axios.get('http://localhost:5000/api/users'); // https://jsonplaceholder.typicode.com/posts
	// console.log(response.data.users);
	setUsers(response.data.users);
};

useEffect(() => {
	fetchData();
}, []);

  return (
    <>
      <h1>TreeMatch</h1>
		{users.map((user, index) => (
			<div key={index}>
				<span>{user}</span>
				{/* <h3>{user.name}</h3> */}
				{/* <p>{user.email</p> */}
				<br />
				</div>
		))}
    </>
  )
}

export default App
