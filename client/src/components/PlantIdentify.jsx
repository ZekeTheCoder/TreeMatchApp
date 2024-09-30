import { useState } from 'react';
import axios from 'axios';

const PlantIdentify = () => {
	const [plantInfo, setPlantInfo] = useState(null);
	const [loading, setLoading] = useState(false);
	const [error, setError] = useState(null);
	const [imageFile, setImageFile] = useState(null);
	const [imageUrl, setImageUrl] = useState('');
	const BASE_URL = import.meta.env.VITE_APP_BASE_URL;

	// const API_Response = 

	// handle image upload
	// const handleImageUpload = (e) => {
	// 	const file = e.target.files[0];
	// 	if (file) {
	// 		setImageFile(file);
	// 		setImageUrl('');
	// 	}
	// };

	// handle URL change
	const handleUrlChange = (e) => {
		setImageUrl(e.target.value);
		setImageFile(null);
	};

	const handleSubmit = async (e) => {
		e.preventDefault();
		setLoading(true);



		const request = {
			latitude: -26.20535546,
			longitude: 28.05110186,
			// ...(imageFile ? { image: imageFile } : {}),
			...(imageUrl ? { image: imageUrl } : {})
		};


		const jwt_token = localStorage.getItem('authToken')

		// setPlantInfo(API_Response); // Update state with the fetched data
		// console.table(plantInfo)

		try {
			const response = await axios.post(`${BASE_URL}/plants/identify`, request, {
				headers: {
					Authorization: `Bearer ${jwt_token}`,
				},
			});
			console.log(response.data);
			setPlantInfo(response.data);
			// setPlantInfo(API_Response); 
			// console.table(plantInfo)
			console.log(plantInfo);
			setError(null);
		} catch (err) {
			console.error(err);
			setError('Failed to identify the plant');
		} finally {
			setLoading(false);
		}
	};

	return (
		<div className="container mt-5">
			<h1>Plant Identifier</h1>
			<form onSubmit={handleSubmit} className="mb-3">
				{/* <div className="form-group">
					<label htmlFor="imageUpload">Upload Image</label>
					<input
						type="file"
						className="form-control"
						id="imageUpload"
						accept="image/*"
						onChange={handleImageUpload}
					/>
				</div> */}
				<div className="form-group mt-3">
					<label htmlFor="imageUrl">or Enter Image URL</label>
					<input
						type="url"
						className="form-control"
						id="imageUrl"
						placeholder="https://example.com/image.jpg"
						value={imageUrl}
						onChange={handleUrlChange}
					/>
				</div>
				<button type="submit" className="btn btn-primary mt-3">Identify Plant</button>
			</form>


			{error && (
				<div className="text-center text-danger">{error}</div>
			)}

			{plantInfo && (
				<div>
					<h2 className="text-center">{plantInfo.suggestions[0].plant_name}</h2>
					<h3 className="text-center text-muted">
						{plantInfo.suggestions[0].common_names.join(", ")}
					</h3>
					<div className="row">
						<div className="col-md-6">
							<img
								src={plantInfo.suggestions[0].image_url}
								alt={plantInfo.suggestions[0].plant_name}
								className="img-fluid rounded"
							/>
						</div>
						<div className="col-md-6">
							<p>
								<strong>Description:</strong> {plantInfo.suggestions[0].description}
							</p>
							<p>
								<strong>Best Soil Type:</strong> {plantInfo.suggestions[0].best_soil_type}
							</p>
							<p>
								<strong>Watering Guidelines:</strong> {plantInfo.suggestions[0].best_watering}
							</p>
							<p>
								<strong>Propagation Methods:</strong> {plantInfo.suggestions[0].propagation_methods || "N/A"}
							</p>
							<p>
								<strong>Edible Parts:</strong> {plantInfo.suggestions[0].edible_parts ? plantInfo.suggestions[0].edible_parts.join(", ") : "N/A"}
							</p>
							<p>
								<strong>Synonyms:</strong> {plantInfo.suggestions[0].synonyms.join(", ")}
							</p>
						</div>
					</div>

					<h3 className="mt-4">Similar Images</h3>
					<div className="row">
						{plantInfo.suggestions[0].similar_images.map((image, index) => (
							<div className="col-md-6 mb-3" key={index}>
								<img
									src={image.url}
									alt={`Similar plant ${index + 1}`}
									className="img-fluid rounded"
								/>
							</div>
						))}
					</div>

					<h3 className="mt-4">Suggestions for Alternative Plants</h3>
					{plantInfo.suggestions.map((suggestion, index) => (
						<div className="card mb-3" key={index}>
							<div className="row g-0">
								<div className="col-md-4">
									<img
										src={suggestion.image_url}
										alt={suggestion.plant_name}
										className="img-fluid rounded-start"
									/>
								</div>
								<div className="col-md-8">
									<div className="card-body">
										<h5 className="card-title">{suggestion.plant_name}</h5>
										<p className="card-text">
											<strong>Common Names:</strong> {suggestion.common_names.join(", ") || "N/A"}
										</p>
										<p className="card-text">
											<strong>Best Soil Type:</strong> {suggestion.best_soil_type}
										</p>
										<p className="card-text">
											<strong>Watering:</strong> {suggestion.best_watering}
										</p>
									</div>
								</div>
							</div>
						</div>
					))}
				</div>
			)}

		</div>
	);
};

export default PlantIdentify;
