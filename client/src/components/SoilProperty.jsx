import React, { useState } from 'react';
import axios from 'axios';
import { Spinner, Form, Button, Table, Alert } from 'react-bootstrap';
import { Container, Row, Col, Card } from 'react-bootstrap';
import SoilLocations from './SoilLocations';

function SoilProperty() {
	const [latitude, setLatitude] = useState('');
	const [longitude, setLongitude] = useState('');
	// const [propertyName, setPropertyName] = useState('');
	const [soilData, setSoilData] = useState(null);
	const [loading, setLoading] = useState(false);
	const [error, setError] = useState('');

	const BASE_URL = import.meta.env.VITE_APP_BASE_URL;

	const fetchSoilProperty = async () => {
		setLoading(true);
		setError('');
		setSoilData(null);

		const jwt_token = localStorage.getItem('authToken')

		try {
			const response = await axios.get(`${BASE_URL}/soil_measurements/get_soil_property`, {
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

	const handleLocationSelect = (location) => {
		setLatitude(location.latitude);
		setLongitude(location.longitude);
	};

	return (
		<div className="container mt-4">
			<h2 className="text-success">Soil Property Search</h2>

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

				<Button className="mt-3" variant="success" type="submit" disabled={loading}>
					{loading ? <Spinner animation="border" size="sm" /> : 'Search'}
				</Button>
			</Form>

			{error && <Alert variant="danger" className="mt-3">{error}</Alert>}

			{soilData && (
				<div className="mt-4">
					<h4 className="text-success">Soil Property Details</h4>
					<Table striped bordered hover>
						<thead>
							<tr className="bg-success">
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

			{/* use SoilLocations to select location*/}
			<h2 className="text-success mt-4">Select a Location</h2>
			<SoilLocations onSelectLocation={handleLocationSelect} />

			{/* Geojson Instruction to find coordinates */}
			<Container className="mt-4">
				<Row>
					<Col md={12}>
						<Card className="shadow">
							<Card.Body>
								<Card.Title>How to Find Coordinates for Your Location</Card.Title>
								<Card.Text>
									To add a new soil location, you can use GeoJSON to find the coordinates of the location you wish to add.
									Follow these steps:
								</Card.Text>
								<ol className="pl-3">
									<li>
										Go to the GeoJSON tool by clicking this link:{' '}
										<a
											href="https://geojson.io/"
											target="_blank"
											rel="noopener noreferrer"
											className="text-primary"
										>
											https://geojson.io/
										</a>
									</li>
									<li>Once the page is open, search for the location you want to add using the search bar or by clicking on the map.</li>
									<li>After finding the location, click Draw point and place on the map, and a popup will display the latitude and longitude of the point you clicked.</li>
									<li>Copy the latitude and longitude values, and use them to create a new soil location in the form.</li>
								</ol>
								<Button
									variant="primary"
									href="https://geojson.io/"
									target="_blank"
									rel="noopener noreferrer"
									className="mt-3 bg-success"
								>
									Open GeoJSON Tool
								</Button>
							</Card.Body>
						</Card>
					</Col>
				</Row>
			</Container>
		</div>
	);
}

export default SoilProperty;
