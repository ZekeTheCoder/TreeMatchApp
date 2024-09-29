import React, { useState } from 'react';
import axios from 'axios';
import { Spinner, Form, Button, Table, Alert } from 'react-bootstrap';

function SoilProperty() {
	const [latitude, setLatitude] = useState('');
	const [longitude, setLongitude] = useState('');
	// const [propertyName, setPropertyName] = useState('');
	const [soilData, setSoilData] = useState(null);
	const [loading, setLoading] = useState(false);
	const [error, setError] = useState('');

	const fetchSoilProperty = async () => {
		setLoading(true);
		setError('');
		setSoilData(null);

		const jwt_token = localStorage.getItem('authToken')

		try {
			const response = await axios.get(`http://127.0.0.1:5000/soil_measurements/get_soil_property`, {
				params: {
					latitude,
					longitude,
					// property_name: propertyName,
				},
				headers: {
					Authorization: `Bearer ${jwt_token}`,
				},
			});

			setSoilData(response.data);
		} catch (err) {
			console.error(err);
			setError('Failed to retrieve soil data. Please try again.');
		} finally {
			setLoading(false);
		}
	};

	const handleSubmit = (e) => {
		e.preventDefault();
		fetchSoilProperty();
	};

	return (
		<div className="container mt-4">
			<h2>Soil Property Search</h2>

			<Form onSubmit={handleSubmit}>
				<Form.Group controlId="latitude">
					<Form.Label>Latitude</Form.Label>
					<Form.Control
						type="text"
						placeholder="Enter latitude"
						value={latitude}
						onChange={(e) => setLatitude(e.target.value)}
						required
					/>
				</Form.Group>

				<Form.Group controlId="longitude">
					<Form.Label>Longitude</Form.Label>
					<Form.Control
						type="text"
						placeholder="Enter longitude"
						value={longitude}
						onChange={(e) => setLongitude(e.target.value)}
						required
					/>
				</Form.Group>

				{/* <Form.Group controlId="propertyName">
					<Form.Label>Soil Property Name</Form.Label>
					<Form.Control
						type="text"
						placeholder="Enter soil property (e.g., ph)"
						value={propertyName}
						onChange={(e) => setPropertyName(e.target.value)}
						required
					/>
				</Form.Group> */}

				<Button variant="primary" type="submit" disabled={loading}>
					{loading ? <Spinner animation="border" size="sm" /> : 'Search'}
				</Button>
			</Form>

			{error && <Alert variant="danger" className="mt-3">{error}</Alert>}

			{soilData && (
				<div className="mt-4">
					<h4>Soil Property Details</h4>
					<Table striped bordered hover>
						<thead>
							<tr>
								<th>Property</th>
								<th>Value</th>
								<th>Recommendation</th>
							</tr>
						</thead>
						<tbody>
							{Object.entries(soilData).map(([key, data]) => (
								<tr key={key}>
									<td>{key}</td>
									<td>{data.value}</td>
									<td>{data.recommendation}</td>
								</tr>
							))}
						</tbody>
					</Table>
				</div>
			)}
		</div>
	);
}

export default SoilProperty;
