import React, { useState } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';
import { useNavigate } from 'react-router-dom';
import { isLoggedIn } from '/src/utils/auth.js';
import { FaBars } from 'react-icons/fa';

const Header = () => {
	const navigate = useNavigate();
	const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

	const toggleMobileMenu = () => {
		setIsMobileMenuOpen(!isMobileMenuOpen);
	};

	const loggedIn = isLoggedIn();
	console.log('loggedIn: ' + loggedIn);

	const logout = async () => {
		try {
			const token = localStorage.getItem("authToken");

			if (token) {
				const response = await axios.post(
					'http://localhost:5000/auth/logout',
					{},
					{
						headers: {
							Authorization: `Bearer ${token}`
						}
					}
				);

				if (response.data.message === "Successfully logged out") {
					console.log('Successfully logged out');
					localStorage.removeItem("authToken");
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
		<nav className={`navbar navbar-expand-lg ${loggedIn ? 'navbar-dark bg-success' : 'navbar-dark bg-dark'}`}>
			<div className="container-fluid">
				{/* Logo */}
				<Link to="/" className="navbar-brand mx-auto">
					TreeMatch
				</Link>

				{/* Hamburger Menu for Mobile */}
				<button
					className="navbar-toggler"
					type="button"
					aria-label="Toggle navigation"
					onClick={toggleMobileMenu}
				>
					<FaBars className="text-white" />
				</button>

				{/* Navbar Links - Toggle Collapse on Smaller Screens */}
				<div className={`collapse navbar-collapse ${isMobileMenuOpen ? 'show' : ''}`}>
					<ul className="navbar-nav mx-auto">
						{loggedIn ? (
							// Links for logged-in users
							<>
								<li className="nav-item">
									<Link to="/plant_identify" className="nav-link px-2 text-white">Plant Identify</Link>
								</li>
								{/* <li className="nav-item">
									<Link to="/plant_search" className="nav-link px-2 text-white">Plant Search</Link>
								</li> */}
								<li className="nav-item">
									<Link to="/invasive_plant_search" className="nav-link px-2 text-white">Invasive Plant Search</Link>
								</li>
								<li className="nav-item">
									<Link to="/soil_property" className="nav-link px-2 text-white">Soil Properties</Link>
								</li>
								{/* <li className="nav-item">
									<Link to="soil_locations" className="nav-link px-2 text-white">Locations</Link>
								</li> */}
							</>
						) : (
							// Links for logged-out users
							<>
								<li className="nav-item">
									<a href="#features" className="nav-link px-2 text-white">Features</a>
								</li>
								<li className="nav-item">
									<a href="#pricing" className="nav-link px-2 text-white">Pricing</a>
								</li>
							</>
						)}
					</ul>

					{/* Conditional Links based on login status */}
					<ul className="navbar-nav ms-auto">
						{loggedIn ? (
							<>
								{/* Profile and Logout for logged-in users */}
								<li className="nav-item">
									<Link to="#profile" className="nav-link px-2 text-white">Profile</Link>
								</li>
								<li className="nav-item">
									<button className="nav-link px-2 text-white btn" onClick={logout}>Logout</button>
								</li>
							</>
						) : (
							<>
								{/* Login and Sign Up for non-logged-in users */}
								<li className="nav-item">
									<Link to="/login" className="nav-link px-2 text-white">Login</Link>
								</li>
								<li className="nav-item">
									<Link to="/signup" className="nav-link px-2 text-white">Sign Up</Link>
								</li>
							</>
						)}
					</ul>
				</div>
			</div>
		</nav>
	);
};

export default Header;
