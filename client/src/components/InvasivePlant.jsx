import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Pagination, Spinner } from 'react-bootstrap';

function InvasivePlant() {

	const [plantName, setPlantName] = useState('');
	const [plants, setPlants] = useState([]);
	const [page, setPage] = useState(1);
	const [perPage, setPerPage] = useState(10);
	const [totalPages, setTotalPages] = useState(0);
	const [loading, setLoading] = useState(false);
	const [error, setError] = useState('');

	const BASE_URL = import.meta.env.VITE_APP_BASE_URL;

	const fetchPlants = async (page = 1) => {
		setLoading(true);
		setError('');

		const jwt_token = localStorage.getItem('authToken')
		// console.log(jwt_token)

		try {
			const response = await axios.get(`${BASE_URL}/invasive_plants/search`, {
				params: {
					invasive_plant_name: plantName,
					page,
					per_page: perPage,
				},
				headers: {
					Authorization: `Bearer ${jwt_token}`,
				},
			});

			const { results, pages, current_page } = response.data;
			setPlants(results);
			setTotalPages(pages);
			setPage(current_page);
		} catch (err) {
			console.error(err);
			setError('Failed to fetch data. Please try again.');
		} finally {
			setLoading(false);
		}
	};

	// reset page to 1 to display the results from the first page.
	const handleSearch = () => {
		setPage(1);
		fetchPlants(1);
	};

	// Pagination
	const handlePageChange = (newPage) => {
		if (newPage >= 1 && newPage <= totalPages) {
			fetchPlants(newPage);
		}
	};

	return (
		<div className="container mt-4">
			<h2>Invasive Plant Search</h2>

			<div className="input-group mb-3">
				{/* Search Input */}
				<input
					type="text"
					className="form-control"
					placeholder="Enter invasive plant name"
					value={plantName}
					onChange={(e) => setPlantName(e.target.value)}
				/>
				{/* Search Button */}
				<div className="input-group-append">
					<button className="btn btn-primary" onClick={handleSearch} disabled={loading}>
						{loading ? <Spinner animation="border" size="sm" /> : 'Search'}
					</button>
				</div>
			</div>

			{error && <div className="alert alert-danger">{error}</div>}

			{/* Loading Indicator */}
			{loading ? (
				<div className="text-center">
					<Spinner animation="border" />
				</div>
			) : (
				<div>
					{plants.length > 0 ? (
						// Results Table
						<table className="table table-bordered">
							<thead>
								<tr>
									<th>Scientific Name</th>
									<th>Common Name</th>
									<th>Category</th>
								</tr>
							</thead>
							<tbody>
								{plants.map((plant) => (
									<tr key={plant.id}>
										<td>{plant.scientific_name || 'N/A'}</td>
										<td>{plant.common_name || 'N/A'}</td>
										<td>{plant.category || 'N/A'}</td>
									</tr>
								))}
							</tbody>
						</table>
					) : (
						<p>No plants found.</p>
					)}

					{/* Pagination */}
					{totalPages > 1 && (
						<Pagination className="justify-content-center">
							<Pagination.Prev onClick={() => handlePageChange(page - 1)} disabled={page === 1} />
							{[...Array(totalPages)].map((_, index) => (
								<Pagination.Item
									key={index + 1}
									active={index + 1 === page}
									onClick={() => handlePageChange(index + 1)}
								>
									{index + 1}
								</Pagination.Item>
							))}
							<Pagination.Next onClick={() => handlePageChange(page + 1)} disabled={page === totalPages} />
						</Pagination>
					)}
				</div>
			)}
		</div>
	);
}

export default InvasivePlant