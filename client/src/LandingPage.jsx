// src/LandingPage.js
import React from 'react';
import { FaFacebookF, FaTwitter, FaInstagram, FaLinkedinIn, FaLeaf, FaArrowUp } from 'react-icons/fa';
import { GiPlantWatering } from 'react-icons/gi';  // alternative for FaPlant
import { RiPlantLine, RiFlowerLine } from 'react-icons/ri';  // alternative for FaFlower
import { FaSeedling, FaMountain } from 'react-icons/fa';  // alternative for FaFlower

const LandingPage = () => {
	return (
		<>
			{/* Hero Section */}
			<div className="hero bg-success text-white text-center py-5 d-flex align-items-center justify-content-center" style={{ borderTop: '5px solid black', height: '80vh' }}>
				<div className="container">
					<h1 className="display-4">Welcome to <span className="text-warning">TreeMatch Premium</span></h1>
					<p className="lead">Discover personalized plant care tips, exclusive plant varieties, and more!</p>
					<a href="/login" className="btn btn-light btn-lg">Get Started</a>
				</div>
			</div>

			{/* Features Section */}
			<div id="features" className="container my-5">
				<h2 className="text-center">Why Choose TreeMatch Premium?</h2>
				<div className="row text-center mt-4">
					{/* Soil Property Recommendation */}
					<div className="col-md-4">
						<div className="card">
							<FaMountain size={50} className="mb-3 text-success mx-auto" />
							<h5>Soil Property Recommendation</h5>
							<p>
								Get tailored recommendations on the best soil properties for your plants
								based on your exact location. Whether you're growing in sandy, clay, or loamy soil,
								we provide expert advice on amendments and treatments to ensure optimal plant health.
							</p>
						</div>
					</div>

					{/* Identify Plants via Search Image */}
					<div className="col-md-4"><div className="card">
						<RiPlantLine size={50} className="mb-3 text-success mx-auto" />
						<h5>Identify Plants via Image Search</h5>
						<p>
							Simply upload a photo of any plant, and our advanced AI-driven tool will identify
							it within seconds. Whether it's a common houseplant or an exotic species,
							TreeMatch Premium helps you learn its name, care requirements, and more, all from a single picture.
						</p>
					</div>
					</div>

					{/* Invasive Plants Identification */}
					<div className="col-md-4"><div className="card">
						<GiPlantWatering size={50} className="mb-3 text-success mx-auto" />
						<h5>Invasive Plants Identification</h5>
						<p>
							Protect your garden from harmful invasive species. Our service helps you quickly
							detect invasive plants in your area and provides guidance on effective removal methods.
							Stay informed and safeguard your ecosystem by learning which plants pose a threat.
						</p>
					</div>
					</div>
				</div>
			</div>


			{/* Pricing Section */}
			<div id="pricing" className="container my-5">
				<h2 className="text-center">Choose Your Plan</h2>
				<div className="row text-center mt-4">
					<div className="col-md-4">
						<div className="card pricing-card">
							<div className="card-body">
								<h5 className="card-title">Free Plan</h5>
								<p className="card-text">R0.00/month</p>
								<p>Access to basic plant care tips and limited plant varieties.</p>
								<a href="/login" className="btn btn-success">Try it now</a>
							</div>
						</div>
					</div>
					<div className="col-md-4">
						<div className="card pricing-card">
							<div className="card-body">
								<h5 className="card-title">Premium Plan</h5>
								<p className="card-text">R19.99/month</p>
								<p>Access to expert advice, exclusive plants, and premium support.</p>
								<a href="#subscribe" className="btn btn-secondary ">Subscribe</a>
							</div>
						</div>
					</div>
					<div className="col-md-4">
						<div className="card pricing-card">
							<div className="card-body">
								<h5 className="card-title">Annual Plan</h5>
								<p className="card-text">R199/year</p>
								<p>Save money by subscribing annually and get all premium benefits.</p>
								<a href="#subscribe" className="btn btn-dark">Subscribe</a>
							</div>
						</div>
					</div>
				</div>
			</div>

			{/* Footer */}
			<footer className="bg-success text-white text-center py-3">
				<p><span className="text-warning">Subscribe</span> for exclusive updates and offers</p>
				<form className="form-inline justify-content-center">
					<input type="email" placeholder="Enter your email" className="form-control w-50 mx-auto mt-2" />
					<button className="btn btn-outline-light mt-2">Subscribe</button>
				</form>
				<div className="mt-2">
					<FaFacebookF className="mx-2" />
					<FaTwitter className="mx-2" />
					<FaInstagram className="mx-2" />
					<FaLinkedinIn className="mx-2" />
				</div>
				<p className="mt-3">&copy; 2024 TreeMatch. All rights reserved.</p>
				<FaArrowUp className="bg-dark position-fixed bottom-0 end-0 mb-5 ms-4" />

			</footer>
		</>
	);
};

export default LandingPage;
