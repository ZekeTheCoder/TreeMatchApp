import { useState, useEffect } from 'react'
import axios from 'axios'

function Trees() {
	const [trees, setTrees] = useState([]);

	const fetchData = async () => {
		const response = await axios.get('http://localhost:5000/plants/plants'); // https://jsonplaceholder.typicode.com/posts
		console.log(response.data);
		setTrees(response.data);
	};

	useEffect(() => {
		fetchData();
	}, []);

	return (
		<>
			<h1>TreeMatch</h1>
			{trees.map((tree) => (
				<div key={tree.id}>
					<h3>{tree.id}. {tree.title}</h3>
					<p>{tree.description}</p>
					{/* <br /> */}
				</div>
			))}
		</>
	)
}

export default Trees
