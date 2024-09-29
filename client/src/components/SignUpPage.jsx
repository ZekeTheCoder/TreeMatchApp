import React, { useState } from 'react'
import axios from 'axios';
import { Form, Button, Alert } from 'react-bootstrap'
import { Link } from 'react-router-dom'
import { useForm } from 'react-hook-form'
import { useNavigate } from 'react-router-dom';
import { isLoggedIn } from '/src/utils/auth.js';


const SignUpPage = () => {
	const { register, handleSubmit, reset, formState: { errors } } = useForm();
	const [show, setShow] = useState(false)
	const [serverResponse, setServerResponse] = useState('')

	const navigate = useNavigate();

	const submitSignUpForm = async (data) => {

		if (data.password === data.confirmPassword) {
			const requestBody = {
				username: data.username,
				email: data.email,
				password: data.password
			};

			try {
				const response = await axios.post('http://localhost:5000/auth/signup', requestBody);
				console.log(response.data);

				setServerResponse(response.data.message);
				setShow(true);
				navigate('/login');
				// window.location.href ="/login"
			} catch (error) {
				console.error('There was an error!', error);
			}
			reset();
		} else {
			alert("Passwords do not match");
		}
	};

	return (
		<div className="container">
			{/* Form Rendering */}
			<div className="form">
				{/* Conditional Alert success message */}
				{show ?
					<>
						<Alert variant="success" onClose={() => {
							setShow(false)
						}} dismissible>
							<p>
								{serverResponse}
							</p>
						</Alert>
						<h1>Create an account</h1>
					</>
					:
					<h1 className="mb-3 text-success mx-auto" >Create an account</h1>
				}
				<form className="form-container">
					{/* Username field */}
					<div className="form-group">
						<label htmlFor="username">Username</label>
						<input
							type="text"
							id="username"
							className="form-control"
							placeholder="your username*"
							{...register("username", { required: true, maxLength: 25 })}
						/>
						{errors.username && <small style={{ color: "red" }}>Username is required</small>}
						{errors.username?.type === "maxLength" && <p style={{ color: "red" }}><small>Max characters should be 25</small></p>}
					</div>
					<br />

					{/* Email field */}
					<div className="form-group">
						<label htmlFor="email">Email</label>
						<input
							type="email"
							id="email"
							className="form-control"
							placeholder="your email*"
							{...register("email", { required: true, maxLength: 80 })}
						/>
						{errors.email && <p style={{ color: "red" }}><small>Email is required</small></p>}
						{errors.email?.type === "maxLength" && <p style={{ color: "red" }}><small>Max characters should be 80</small></p>}
					</div>
					<br />

					{/* Password field */}
					<div className="form-group">
						<label htmlFor="password">Password</label>
						<input
							type="password"
							id="password"
							className="form-control"
							placeholder="your password*"
							{...register("password", { required: true, minLength: 8 })}
						/>
						{errors.password && <p style={{ color: "red" }}><small>Password is required</small></p>}
						{errors.password?.type === "minLength" && <p style={{ color: "red" }}><small>Min characters should be 8</small></p>}
					</div>
					<br />

					{/* Confirm Password field */}
					<div className="form-group">
						<label htmlFor="confirmPassword">Confirm Password</label>
						<input
							type="password"
							id="confirmPassword"
							className="form-control"
							placeholder="confirm your password*"
							{...register("confirmPassword", { required: true, minLength: 8 })}
						/>
						{errors.confirmPassword && <p style={{ color: "red" }}><small>Confirm Password is required</small></p>}
						{errors.confirmPassword?.type === "minLength" && <p style={{ color: "red" }}><small>Min characters should be 8</small></p>}
					</div>
					<br />

					{/* Submit Button: Calls handleSubmit(submitSignUpForm) to handle form submission */}
					<div className="form-group">
						<button type="button" className="btn btn-success" onClick={handleSubmit(submitSignUpForm)}>Sign Up</button>
					</div>
					<br />

					{/* Link to the login page */}
					<div className="form-group">
						<small>Already have an account? <Link to="/login">Log In</Link></small>
					</div>
					<br />
				</form>

			</div>
		</div>
	)
}

export default SignUpPage