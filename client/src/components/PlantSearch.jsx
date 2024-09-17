import { useState } from 'react';
import axios from 'axios';

function PlantSearch() {
	const [searchQuery, setSearchQuery] = useState('aloe vera');
	const [plantData, setPlantData] = useState(null);
	const [loading, setLoading] = useState(false);
	const [error, setError] = useState('');

	const apiKey = import.meta.env.VITE_REACT_APP_API_KEY;

	const fetchPlantData = async () => {
		setLoading(true);
		setError('');
		setPlantData(null);

		const apiKey1 = '';
		const url = `https://api/v3/kb/plants/name_search?q=${encodeURIComponent(searchQuery)}`;

		try {
			const response = await axios.get(url, {
				headers: {
					Authorization: `Bearer ${apiKey1}`
				}
			});
			setPlantData(response.data);
		} catch (err) {
			setError('Error fetching plant data. Please try again.');
		} finally {
			setLoading(false);
		}
	};

	const handleSearch = () => {
		fetchPlantData();
	};

	return (
		<div className="plant-search">
			<h1>Plant Name Search</h1>
			<div>
				<input
					type="text"
					value={searchQuery}
					onChange={(e) => setSearchQuery(e.target.value)}
					placeholder="Enter plant name"
				/>
				<button onClick={handleSearch} disabled={loading}>
					{loading ? 'Searching...' : 'Search'}
				</button>
			</div>

			{error && <p style={{ color: 'red' }}>{error}</p>}

			{plantData && (
				<div>
					<h2>Plant Data:</h2>
					{plantData.plants && plantData.plants.length > 0 ? (
						<ul>
							{plantData.plants.map((plant, index) => (
								<li key={index}>
									<strong>{plant.common_name || 'No common name available'}</strong>
									<p><strong>Scientific Name:</strong> {plant.scientific_name}</p>
									<p><strong>Family:</strong> {plant.family}</p>
									<p><strong>Genus:</strong> {plant.genus}</p>
									<p><strong>Family:</strong> {plant.family}</p>
								</li>
							))}
						</ul>
					) : (
						<p>No plants found.</p>
					)}
				</div>
			)}
		</div>
	);
}

export default PlantSearch;
