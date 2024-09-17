// eslint-disable-next-line no-unused-vars
import React, { useState } from 'react'
import axios from 'axios'; // for making HTTP requests to the server.
import { Form, Button } from 'react-bootstrap' // for rendering the form and button UI.
import { Link } from 'react-router-dom'
import { useForm } from 'react-hook-form'
// import { useAuth } from '../AuthContext';
// import { login } from '../auth' //  handles storing the access token after login.
import { useNavigate } from 'react-router-dom';  // redirecting

const LoginPage = () => {
	/*Used to register form input fields for validation, Submits the form and
	executes the login function, resets the form fields after submission.
	and captures validation errors.*/
	const { register, handleSubmit, reset, formState: { errors } } = useForm()

	// to redirect the user 
	const navigate = useNavigate();
	// const { login } = useAuth();

	// Handles the login form submission.
	const loginUserForm = async (data) => {
		// console.log(data);

		// Prepare request payload
		const requestBody = {
			username: data.username,
			password: data.password
		};

		try {
			// Make POST request with axios
			const response = await axios.post('http://localhost:5000/auth/login', requestBody, {
				headers: {
					'Content-Type': 'application/json'
				}
			});
			// console.log(response.data);

			// destructure the access token from the response data
			const { access_token } = response.data;
			// console.log(access_token);

			if (access_token) {
				// login(access_token); // Save access token
				axios.defaults.headers.common['Authorization'] = `Bearer ${data['access_token']}`;
				// Log the Authorization header to the console
				console.log('login successfully: Authorization set');
				// console.log(axios.defaults.headers.common['Authorization']);
				// Save token after login
				localStorage.setItem("authToken", access_token);
				const token = localStorage.getItem("authToken");
				// console.log('authToken: ' + token);

				navigate('/'); // Redirect to home page
				// window.location.href ="/login"
			} else {
				alert('Invalid username or password');
			}
		} catch (error) {
			console.error('Error:', error);
			alert('An error occurred. Please try again.');
		}
		// Reset form fields
		reset();
	};

	return (
		<div className="container">
			{/* Rendering the Form */}
			<div className="form">
				<h1>Login Page</h1>
				{/*  Renders a login form with two fields: username and password. */}
				<form>
					{/* Username field */}
					<Form.Group>
						<Form.Label>Username</Form.Label>
						<Form.Control type="text"
							placeholder="Your username"
							{...register('username', { required: true, maxLength: 25 })}
						/>
					</Form.Group>
					{errors.username && <p style={{ color: 'red' }}><small>Username is required</small></p>}
					{errors.username?.type === "maxLength" && <p style={{ color: 'red' }}><small>Username should be 25 characters</small></p>}
					<br></br>

					{/* Password field */}
					<Form.Group>
						<Form.Label>Password</Form.Label>
						<Form.Control type="password"
							placeholder="Your password"
							{...register('password', { required: true, minLength: 8 })}
						/>
					</Form.Group>
					{errors.username && <p style={{ color: 'red' }}><small>Password is required</small></p>}
					{errors.password?.type === "maxLength" && <p style={{ color: 'red' }}>
						<small>Password should be more than 8 characters</small>
					</p>}
					<br></br>
					{/* Submit button */}
					<Form.Group>
						<Button as="sub" variant="primary" onClick={handleSubmit(loginUserForm)}>Login</Button>
					</Form.Group>
					<br></br>
					{/* Link to the sign-up page */}
					<Form.Group>
						<small>Do not have an account? <Link to='/signup'>Create One Here</Link></small>
					</Form.Group>
				</form>
			</div>
		</div>
	)
}

export default LoginPage