import { useState } from 'react'
import axios from 'axios';
import { Link } from 'react-router-dom'
import { useForm } from 'react-hook-form'
import { useNavigate } from 'react-router-dom';

const LoginPage = () => {
	const { register, handleSubmit, reset, formState: { errors } } = useForm()

	const navigate = useNavigate();

	const loginUserForm = async (data) => {
		// console.log(data);

		const requestBody = {
			username: data.username,
			password: data.password
		};

		try {
			const response = await axios.post('http://localhost:5000/auth/login', requestBody, {
				headers: {
					'Content-Type': 'application/json'
				}
			});
			// console.log(response.data);

			const { access_token } = response.data;
			// console.log(access_token);

			if (access_token) {
				axios.defaults.headers.common['Authorization'] = `Bearer ${data['access_token']}`;
				// Log the Authorization header to the console
				console.log('login successfully: Authorization set');

				localStorage.setItem("authToken", access_token);

				// navigate('/'); // Redirect to home page
				window.location.href = "/"
			} else {
				alert('Invalid username or password');
			}
		} catch (error) {
			console.error('Error:', error);
			alert('An error occurred. Please try again.');
		}
		reset();
	};

	return (
		<div className="container">
			{/* Rendering the Form */}
			<div className="form">
				<h1 className="mb-3 text-success mx-auto" >Login Page - Welcome back</h1>
				{/*  Renders a login form with two fields: username and password. */}
				<form className="form-container">
					{/* Username field */}
					<div className="form-group">
						<label htmlFor="username">Username</label>
						<input
							type="text"
							id="username"
							className="form-control"
							placeholder="your username*"
							{...register('username', { required: true, maxLength: 25 })}
						/>
					</div>
					{errors.username && <p style={{ color: 'red' }}><small>Username is required</small></p>}
					{errors.username?.type === "maxLength" && <p style={{ color: 'red' }}><small>Username should be 25 characters</small></p>}
					<br />

					{/* Password field */}
					<div className="form-group">
						<label htmlFor="password">Password</label>
						<input
							type="password"
							id="password"
							className="form-control"
							placeholder="your password*"
							{...register('password', { required: true, minLength: 8 })}
						/>
					</div>
					{errors.password && <p style={{ color: 'red' }}><small>Password is required</small></p>}
					{errors.password?.type === "minLength" && <p style={{ color: 'red' }}><small>Password should be more than 8 characters</small></p>}
					<br />

					{/* Submit button */}
					<div className="form-group">
						<button type="button" className="btn btn-success" onClick={handleSubmit(loginUserForm)}>Login</button>
					</div>
					<br />

					{/* Link to the sign-up page */}
					<div className="form-group">
						<small>Don't have an account? <Link to='/signup'>Sign up Here</Link></small>
					</div>
					<br />
				</form>

			</div>
		</div>
	)
}

export default LoginPage