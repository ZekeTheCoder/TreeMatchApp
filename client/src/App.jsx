import './App.css';
// import { useState } from 'react'
import { BrowserRouter, Routes, Route } from 'react-router-dom';
// import { Login } from "./components1/Login";
import LoginPage from "./components/LoginPage";
import Header from "./components/Header";
import { Home } from "./components1/Home";
import LandingPage from './components/LandingPage';
import SignUpPage from './components/SignUpPage';
// import { Register } from "./components1/Register";
// import Map from './components/Map'; //
// import Soil from './components/Soil';
import Trees from './components/Trees';
import { isLoggedIn } from './utils/auth';
import NotFound from './components/NotFound';
import PlantIdentify from './components/PlantIdentify';
import PlantSearch from './components/PlantSearch';
// import Profile from './components/Profile';

function App() {


	// Get login status
	const loggedIn = isLoggedIn();
	console.log('loggedIn: ' + loggedIn);

	return (
		<>
			<BrowserRouter>
				<Header />

				<Routes>
					{/* <Route path="/" element={<Home />} /> */}
					<Route path="/" element={<LandingPage />} />
					<Route path="/login" element={<LoginPage />} />
					{/* <Route path="/register" element={<Register />} /> */}
					<Route path="/signup" element={<SignUpPage />} />
					{/* Protected Routes */}
					{loggedIn && (
						<>
							<Route path="/trees" element={<Trees />} />
							<Route path="/plant_identify" element={<PlantIdentify />} />
							<Route path="/plant_search" element={<PlantSearch />} />
							{/* <Route path="/map" element={<Map />} />
							<Route path="/soil" element={<Soil />} />
							<Route path="/profile" element={<Profile />} /> */}
						</>
					)}

					<Route path="*" element={<NotFound />} />
				</Routes>
			</BrowserRouter>
		</>
	);
}

export default App;
