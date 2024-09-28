import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { isLoggedIn } from './utils/auth';
import Header from "./components/Header";
import LoginPage from "./components/LoginPage";
import SignUpPage from './components/SignUpPage';
import NotFound from './components/NotFound';
import PlantIdentify from './components/PlantIdentify';
import PlantSearch from './components/PlantSearch';
import PremiumHomePage from "./PremiumHomePage";
import LandingPage from './LandingPage';
import Trees from './components/Trees';
// import Map from './components/Map'; //
// import Soil from './components/Soil';
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
					<Route path="/" element={<LandingPage />} />
					<Route path="/login" element={<LoginPage />} />
					<Route path="/signup" element={<SignUpPage />} />
					{/* Protected Routes */}
					{loggedIn && (
						<>
							{/* <Route path="/" element={<LandingPage />} /> */}
							<Route path="/premium" element={<PremiumHomePage />} />
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
