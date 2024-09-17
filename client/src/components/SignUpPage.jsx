import React, { useState } from 'react'
import axios from 'axios';
import { Form, Button, Alert } from 'react-bootstrap' // for form handling and user feedback.
import { Link } from 'react-router-dom' // for client-side navigation.
import { useForm } from 'react-hook-form' // for managing form state and validation.


const SignUpPage = () => {
	// State Management
	const { register, handleSubmit, reset, formState: { errors } } = useForm();
	const [show, setShow] = useState(false) // visibility of the alert message after form submission.
	const [serverResponse, setServerResponse] = useState('') // message returned from the server.

	// Form Submission Handling - submitSignUpForm is called when the form is submitted
	const submitSignUpForm = async (data) => {
		// Password Check
		if (data.password === data.confirmPassword) {
			// Prepares the data for submission to server.
			const requestBody = {
				username: data.username,
				email: data.email,
				password: data.password
			};

			try {
				// Use axios to make the POST request
				const response = await axios.post('http://localhost:5000/auth/signup', requestBody);
				console.log(response.data); // Handle the response data from the server
				setServerResponse(response.data.message); // Update state with the server's response
				setShow(true); // Show the response message
			} catch (error) {
				console.error('There was an error!', error); // Handle any errors that occurred during the request
			}

			reset(); // Resets the form fields after submission.
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
						<h1>Sign Up Page</h1>
					</>
					:
					<h1>Sign Up Page</h1>
				}
				{/* Form Fields with validation messages. */}
				<form>
					{/* Username field */}
					<Form.Group>
						<Form.Label>Username</Form.Label>
						<Form.Control type="text"
							placeholder="Your username"
							{...register("username", { required: true, maxLength: 25 })}
						/>

						{errors.username && <small style={{ color: "red" }}>Username is required</small>}
						{errors.username?.type === "maxLength" && <p style={{ color: "red" }}><small>Max characters should be 25 </small></p>}
					</Form.Group>
					<br></br>
					{/* Email field */}
					<Form.Group>
						<Form.Label>Email</Form.Label>
						<Form.Control type="email"
							placeholder="Your email"
							{...register("email", { required: true, maxLength: 80 })}
						/>

						{errors.email && <p style={{ color: "red" }}><small>Email is required</small></p>}

						{errors.email?.type === "maxLength" && <p style={{ color: "red" }}><small>Max characters should be 80</small></p>}
					</Form.Group>
					<br></br>
					{/* Password field */}
					<Form.Group>
						<Form.Label>Password</Form.Label>
						<Form.Control type="password"
							placeholder="Your password"
							{...register("password", { required: true, minLength: 8 })}

						/>

						{errors.password && <p style={{ color: "red" }}><small>Password is required</small></p>}
						{errors.password?.type === "minLength" && <p style={{ color: "red" }}><small>Min characters should be 8</small></p>}
					</Form.Group>
					<br></br>
					{/* Confirm Password field */}
					<Form.Group>
						<Form.Label>Confirm Password</Form.Label>
						<Form.Control type="password" placeholder="Your password"
							{...register("confirmPassword", { required: true, minLength: 8 })}
						/>
						{errors.confirmPassword && <p style={{ color: "red" }}><small>Confirm Password is required</small></p>}
						{errors.confirmPassword?.type === "minLength" && <p style={{ color: "red" }}><small>Min characters should be 8</small></p>}
					</Form.Group>
					<br></br>

					{/* Submit Button: Calls handleSubmit(submitSignUpForm) to handle form submission */}
					<Form.Group>
						<Button as="sub" variant="primary" onClick={handleSubmit(submitSignUpForm)}>SignUp</Button>
					</Form.Group>
					<br></br>
					{/* Link to the login page */}
					<Form.Group>
						<small>Already have an account, <Link to='/login'>Log In</Link></small>
					</Form.Group>
					<br></br>
				</form>
			</div>
		</div>
	)
}

export default SignUpPage