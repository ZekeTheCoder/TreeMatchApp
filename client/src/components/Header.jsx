import React from 'react';
// import PropTypes from 'prop-types';
import axios from 'axios';
import { Link } from 'react-router-dom';
import { useNavigate } from 'react-router-dom';
import { isLoggedIn } from '/src/utils/auth.js';

const Header = () => {
	const navigate = useNavigate();


	// Get login status
	const loggedIn = isLoggedIn();
	console.log('loggedIn: ' + loggedIn);

	const logout = async () => {
		try {
			// Retrieve token from localStorage
			const token = localStorage.getItem("authToken");

			// If token exists, send the logout request with Authorization header
			if (token) {
				const response = await axios.post(
					'http://localhost:5000/auth/logout',
					{},
					{
						headers: {
							Authorization: `Bearer ${token}`
						},
						withCredentials: true, // Send cookies with the request if needed
					}
				);

				// Handle successful logout
				if (response.data.message === "Successfully logged out") {
					console.log('Successfully logged out');
					localStorage.removeItem("authToken"); // Delete token from localStorage
					// navigate('/login'); // Redirect to login page after logout
					window.location.href = "/login"
				} else {
					console.error('Unexpected response message:', response.data.message);
				}
			} else {
				console.error('No auth token found');
			}
		} catch (error) {
			console.error('Logout failed', error);
			if (error.response) {
				console.log('Error response data:', error.response.data);
				console.log('Error status:', error.response.status);
				console.log('Error headers:', error.response.headers);
			}
		}
	};

	return (
		<header className="p-3 bg-dark text-white">
			<div className="container">
				<div className="d-flex flex-wrap align-items-center justify-content-center justify-content-lg-start">
					<ul className="nav col-12 col-lg-auto me-lg-auto mb-2 justify-content-center mb-md-0">
						<li><Link to="/" className="nav-link px-2 text-white">Home</Link></li>
						{loggedIn ? (
							<>
								<li><Link to="/plant_identify" className="nav-link px-2 text-white">Plant Identify</Link></li>
								<li><Link to="/plant_search" className="nav-link px-2 text-white">Plant Search</Link></li>
								<li><Link to="/map" className="nav-link px-2 text-white">Map</Link></li>
								<li><Link to="/soil" className="nav-link px-2 text-white">Soil</Link></li>
								<li><Link to="/trees" className="nav-link px-2 text-white">Trees</Link></li>
								<li><Link to="/profile" className="nav-link px-2 text-white">Profile</Link></li>
								{/* <li><Link to="/logout" className="nav-link px-2 text-white">Logout</Link></li> */}
								<a href="javascript:void(0)" className="nav-link px-2 text-white"
									onClick={logout}
								>Logout</a></>
						) : (
							<>
								<li><Link to="/login" className="nav-link px-2 text-white">Login</Link></li>
								<li><Link to="/signup" className="nav-link px-2 text-white">Sign Up</Link></li>
							</>
						)}
					</ul>
				</div>
			</div>
		</header>
	);
};

// // prop-types
// Header.propTypes = {
// 	loggedIn: PropTypes.bool.isRequired,
// };

export default Header;
