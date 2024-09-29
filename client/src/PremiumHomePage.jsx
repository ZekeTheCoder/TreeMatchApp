import React, { useState } from 'react';
import './PremiumServices.css';
import Header from "./components/Header";
import { FaFacebookF, FaTwitter, FaInstagram, FaLinkedinIn, FaLeaf, FaDollarSign, FaArrowUp } from 'react-icons/fa';
import { GiPlantWatering } from 'react-icons/gi';
import { RiPlantLine, RiFlowerLine } from 'react-icons/ri';

const PremiumHomePage = () => {
	const [expandedIndex, setExpandedIndex] = useState(null);

	const toggleFAQ = (index) => {
		setExpandedIndex(expandedIndex === index ? null : index);
	};

	const faqData = [
		{
			question: "What is TreeMatch Premium?",
			answer: "TreeMatch Premium offers exclusive access to expert gardening advice, rare plants, and special discounts to enhance your gardening experience."
		},
		{
			question: "How do I access premium features?",
			answer: "You can access premium features by subscribing to TreeMatch Premium through our website."
		},
		{
			question: "Can I cancel my subscription at any time?",
			answer: "Yes, you can cancel your subscription at any time through your account settings."
		},
		{
			question: "Is there a free trial available?",
			answer: "Yes, we offer a 7-day free trial for new users to explore premium features."
		}
	];

	return (
		<>
			{/* Hero section */}
			<div className="hero bg-dark text-white text-center py-5 d-flex align-items-center justify-content-center" style={{ height: '80vh' }}>
				<div className="container">
					<h1><span className="text-success">Elevate</span> your gardening experience
						<br /> with <span className="text-success">TreeMatch</span></h1>
					<p>Experience premium services and exclusive offers.</p>
					{/* <a href="#get-started" className="btn btn-info  btn-lg">Get Started</a> */}
				</div>
			</div>

			{/* About section */}
			<div id="about" className="container my-5">
				<h2 className="text-center bg-success">About TreeMatch Premium</h2>
				<p>Unlock premium features and get the best plant recommendations and care tips. Enjoy a curated selection of exclusive plants and personalized gardening advice designed to enhance your gardening journey.</p>
			</div>


			{/* Services section */}
			<div id="services" className="container my-5 ">
				<h2 className="text-center bg-success">Our Premium Services</h2>
				<div className="row">
					<div className="col-md-3 text-center mb-4">
						<div className="card service-card">
							<div className="card-body ">
								<FaLeaf size={50} className="mb-3 text-success" />
								<h5 className="card-title">Expert Advice</h5>
								<p className="card-text">Get personalized plant care tips from experts to ensure your plants thrive.</p>
							</div>
						</div>
					</div>
					<div className="col-md-3 text-center mb-4">
						<div className="card service-card">
							<div className="card-body">
								<RiFlowerLine size={50} className="mb-3 text-success" />
								<h5 className="card-title">Exclusive Plants</h5>
								<p className="card-text">Access a curated selection of rare and unique plant varieties.</p>
							</div>
						</div>
					</div>
					<div className="col-md-3 text-center mb-4">
						<div className="card service-card">
							<div className="card-body">
								<FaDollarSign size={50} className="mb-3 text-success" />
								<h5 className="card-title">Special Discounts text-success</h5>
								<p className="card-text">Enjoy exclusive discounts and offers on all purchases.</p>
							</div>
						</div>
					</div>
					<div className="col-md-3 text-center mb-4">
						<div className="card service-card">
							<div className="card-body">
								<GiPlantWatering size={50} className="mb-3 text-success" />
								<h5 className="card-title">Premium Support</h5>
								<p className="card-text">Receive priority customer support to assist with all your gardening needs.</p>
							</div>
						</div>
					</div>
				</div>
			</div>


			{/* FAQs section */}
			<div id="faq" className="container my-5">
				<h2 className="text-center bg-success">Frequently Asked Questions</h2>
				{faqData.map((item, index) => (
					<div key={index} className="faq-item">
						<h5 onClick={() => toggleFAQ(index)} className="faq-question">
							{item.question}
						</h5>
						{expandedIndex === index && (
							<p className="faq-answer bg-success">{item.answer}</p>
						)}
					</div>
				))}
			</div>

			{/* Footer srction */}
			<footer className="bg-dark text-white text-center py-3">
				<p><span className="text-success">Subscribe</span> for exclusive updates and offers</p>
				<form className="form-inline justify-content-center">
					<input type="email" placeholder="Enter your email" className="form-control mr-sm-2" />
					<button className="btn btn-outline-success">Subscribe</button>
				</form>
				{/* social media icons */}
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
