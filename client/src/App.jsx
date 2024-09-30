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
import InvasivePlant from './components/InvasivePlant';
import SoilProperty from './components/SoilProperty';
import SoilLocations from './components/SoilLocations';;
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
					{loggedIn ? (
						<>
							{/* Protected Routes */}
							<Route path="/" element={<PremiumHomePage />} />
							<Route path="/trees" element={<Trees />} />
							<Route path="/plant_identify" element={<PlantIdentify />} />
							<Route path="/plant_search" element={<PlantSearch />} />
							<Route path="/invasive_plant_search" element={<InvasivePlant />} />
							<Route path="/soil_property" element={<SoilProperty />} />
							<Route path="/soil_locations" element={<SoilLocations />} />
							{/* <Route path="/profile" element={<Profile />} /> */}
						</>
					) : (
						<>
							{/* Unprotected Routes */}
							<Route path="/" element={<LandingPage />} />
							<Route path="/login" element={<LoginPage />} />
							<Route path="/signup" element={<SignUpPage />} />
						</>
					)}
					<Route path="*" element={<NotFound />} />
				</Routes>
			</BrowserRouter>
		</>
	);
}

export default App;
