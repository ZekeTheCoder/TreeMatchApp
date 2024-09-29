import React, { useState, useEffect } from 'react';
import axios from 'axios';
import SoilProperty from './SoilProperty';

const SoilLocations = ({ onSelectLocation }) => {
	const [locations, setLocations] = useState([]);
	const [formData, setFormData] = useState({ name: '', latitude: '', longitude: '' });
	const [editData, setEditData] = useState({ id: '', name: '', latitude: '', longitude: '' });
	const [showCreateForm, setShowCreateForm] = useState(false);
	const [showEditForm, setShowEditForm] = useState(false);
	const [loading, setLoading] = useState(false);
	const [error, setError] = useState('');

	const BASE_URL = import.meta.env.VITE_APP_BASE_URL;

	// Get all soil locations
	const fetchLocations = async () => {
		const jwt_token = localStorage.getItem('authToken')
		try {
			setLoading(true);
			const response = await axios.get(`${BASE_URL}/soil_locations/locations`, {
				headers: {
					Authorization: `Bearer ${jwt_token}`,
				},
			});
			setLocations(response.data);
			setLoading(false);
		} catch (err) {
			setError('Error fetching locations');
			console.error(err);
			setLoading(false);
		}
	};

	// Create soil location
	const createLocation = async (e) => {
		e.preventDefault();
		const jwt_token = localStorage.getItem('authToken');
		try {
			const response = await axios.post(`${BASE_URL}/soil_locations/locations`, formData, {
				headers: {
					Authorization: `Bearer ${jwt_token}`,
				},
			});
			setLocations([...locations, response.data]);
			setFormData({ name: '', latitude: '', longitude: '' });
			setShowCreateForm(false);
		} catch (err) {
			console.error(err);
			setError('Error creating location');
		}
	};

	// Update soil location
	const updateLocation = async (e) => {
		e.preventDefault();
		const jwt_token = localStorage.getItem('authToken');
		try {
			const response = await axios.put(`${BASE_URL}/soil_locations/${editData.id}`, editData, {
				headers: {
					Authorization: `Bearer ${jwt_token}`,
				},
			});
			setLocations(
				locations.map((loc) =>
					loc.id === editData.id ? response.data : loc
				)
			); // Update the location in the list
			setEditData({ id: '', name: '', latitude: '', longitude: '' });
			setShowEditForm(false);
		} catch (err) {
			console.error(err);
			setError('Error updating location');
		}
	};

	// Delete a soil location
	const deleteLocation = async (id) => {
		const jwt_token = localStorage.getItem('authToken');
		try {
			await axios.delete(`${BASE_URL}/soil_locations/locations/${id}`, {
				headers: {
					Authorization: `Bearer ${jwt_token}`,
				},
			});
			setLocations(locations.filter((loc) => loc.id !== id));
		} catch (err) {
			console.error(err);
			setError('Error deleting location');
		}
	};

	useEffect(() => {
		fetchLocations();
	}, []);

	return (
		<div>
			{/* <SoilProperty /> */}

			{/* <h1 className="text-success">Soil Locations</h1> */}
			{error && <p style={{ color: 'red' }}>{error}</p>}
			{loading ? (
				<p>Loading...</p>
			) : (
				<ul>
					{locations.map((location) => (
						<li key={location.id}>
							<p>{location.name}</p>
							<p>Latitude: {location.latitude}</p>
							<p>Longitude: {location.longitude}</p>
							<button className="btn btn-primary" onClick={() => onSelectLocation(location)}>Select</button>
							<button className="btn btn-warning mx-2" onClick={() => { setEditData(location); setShowEditForm(true); }}>Edit</button>
							<button className="btn btn-danger" onClick={() => deleteLocation(location.id)}>Delete</button>
						</li>
					))}
				</ul>
			)}

			{/* Toggle button for creating new location */}
			<button className="btn btn-success" onClick={() => setShowCreateForm(!showCreateForm)}>
				{showCreateForm ? 'Hide Create Form' : 'Show Create Form'}
			</button>

			{/* Create Form */}
			{showCreateForm && (
				<>
					<h2 className="text-success">Create New Location</h2>
					<form onSubmit={createLocation}>
						<input
							type="text"
							placeholder="Name"
							value={formData.name}
							onChange={(e) => setFormData({ ...formData, name: e.target.value })}
						/>
						<input
							type="number"
							step="any"
							placeholder="Latitude"
							value={formData.latitude}
							onChange={(e) => setFormData({ ...formData, latitude: e.target.value })}
						/>
						<input
							type="number"
							step="any"
							placeholder="Longitude"
							value={formData.longitude}
							onChange={(e) => setFormData({ ...formData, longitude: e.target.value })}
						/>
						<button type="submit">Create</button>
					</form>
				</>
			)}

			{/* Edit Form */}
			{showEditForm && editData.id && (
				<>
					<h2>Edit Location</h2>
					<form onSubmit={updateLocation}>
						<input
							type="text"
							placeholder="Name"
							value={editData.name}
							onChange={(e) => setEditData({ ...editData, name: e.target.value })}
						/>
						<input
							type="number"
							step="any"
							placeholder="Latitude"
							value={editData.latitude}
							onChange={(e) => setEditData({ ...editData, latitude: e.target.value })}
						/>
						<input
							type="number"
							step="any"
							placeholder="Longitude"
							value={editData.longitude}
							onChange={(e) => setEditData({ ...editData, longitude: e.target.value })}
						/>
						<button type="submit">Update</button>
						<button type="button" onClick={() => setShowEditForm(false)}>Cancel</button>
					</form>
				</>
			)}
		</div>
	);
};


export default SoilLocations;
