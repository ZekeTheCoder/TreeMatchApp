import React from 'react';
// import './App.css';
import './PremiumServices.css';
import Header from "./components/Header";
import { FaFacebookF, FaTwitter, FaInstagram, FaLinkedinIn, FaLeaf, FaDollarSign, FaArrowUp } from 'react-icons/fa';
import { GiPlantWatering } from 'react-icons/gi';
import { RiPlantLine, RiFlowerLine } from 'react-icons/ri';

const PremiumHomePage = () => {
	return (
		<>
			{/* <Header /> */}

			<div className="hero bg-primary text-white text-center py-5">
				<div className="container">
					<h1><span className="text-warning">Elevate</span> your gardening experience <br /> with <span className="text-warning">TreeMatch</span></h1>
					<p>Experience premium services and exclusive offers.</p>
					<a href="#get-started" className="btn btn-light btn-lg">Get Started</a>
				</div>
			</div>

			<div id="about" className="container my-5">
				<h2 className="text-center">About TreeMatch Premium</h2>
				<p>Unlock premium features and get the best plant recommendations and care tips. Enjoy a curated selection of exclusive plants and personalized gardening advice designed to enhance your gardening journey.</p>
			</div>

			<div id="services" className="container my-5">
				<h2 className="text-center">Our Premium Services</h2>
				<div className="row">
					<div className="col-md-3 text-center mb-4">
						<div className="card service-card">
							<div className="card-body">
								<FaLeaf size={50} className="mb-3" />
								<h5 className="card-title">Expert Advice</h5>
								<p className="card-text">Get personalized plant care tips from experts to ensure your plants thrive.</p>
							</div>
						</div>
					</div>
					<div className="col-md-3 text-center mb-4">
						<div className="card service-card">
							<div className="card-body">
								<RiFlowerLine size={50} className="mb-3" />
								<h5 className="card-title">Exclusive Plants</h5>
								<p className="card-text">Access a curated selection of rare and unique plant varieties.</p>
							</div>
						</div>
					</div>
					<div className="col-md-3 text-center mb-4">
						<div className="card service-card">
							<div className="card-body">
								<FaDollarSign size={50} className="mb-3" />
								<h5 className="card-title">Special Discounts</h5>
								<p className="card-text">Enjoy exclusive discounts and offers on all purchases.</p>
							</div>
						</div>
					</div>
					<div className="col-md-3 text-center mb-4">
						<div className="card service-card">
							<div className="card-body">
								<GiPlantWatering size={50} className="mb-3" />
								<h5 className="card-title">Premium Support</h5>
								<p className="card-text">Receive priority customer support to assist with all your gardening needs.</p>
							</div>
						</div>
					</div>
				</div>
			</div>

			<footer className="bg-dark text-white text-center py-3">
				<p><span className="text-warning">Subscribe</span> for exclusive updates and offers</p>
				<form className="form-inline justify-content-center">
					<input type="email" placeholder="Enter your email" className="form-control mr-sm-2" />
					<button className="btn btn-outline-light">Subscribe</button>
				</form>
				<div className="mt-2">
					<FaFacebookF className="mx-2" />
					<FaTwitter className="mx-2" />
					<FaInstagram className="mx-2" />
					<FaLinkedinIn className="mx-2" />
				</div>
				<p className="mt-3">&copy; 2024 TreeMatch. All rights reserved.</p>
				<FaArrowUp className="position-fixed bottom-0 end-0 mb-3 mr-3" />
			</footer>
		</>
	);
};

export default PremiumHomePage;
