
import requests


def get_soil_property(lat: float, lon: float, property_name: str) -> dict:
    """
    Calls the soil property API to retrieve information for a specific location.

    Args:
        lat (float): Latitude of the location.
        lon (float): Longitude of the location.
        property_name (str): The soil property to query (e.g., "ph").
        depth (str): The depth at which the property is measured (e.g., "0-20").
        auth_header (str): The authorization header to include in the request.

    Returns:
        dict: The response from the API as a JSON object.
    """
    # Define the API key and the base URL
    api_key = "AIzaSyCruMPt43aekqITCooCNWGombhbcor3cf4"
    base_url = "https://api.isda-africa.com/v1/soilproperty"
    depth = "0-20"

    # Set up the query parameters
    params = {
        'key': api_key,
        'lat': lat,
        'lon': lon,
        'property': property_name,
        'depth': depth
    }

    # Print the URL for debugging
    print(
        f"Request URL: {base_url}?key={api_key}&lat={lat}&lon={lon}&property={property_name}&depth={depth}")

    # Make the API request
    try:
        response = requests.get(base_url, params=params)
        # Check if the request was successful
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()  # Raises an HTTPError for bad responses
    except requests.exceptions.RequestException as e:
        print(f"Error making the API request: {e}")
        return {}


def get_recommendation(property_name: str, value: float) -> str:
    """
    Determine the threshold (low, moderate, high) for a given soil property
    value and provide a recommendation.

    Args:
        property_name (str): The name of the soil property (e.g., "ph", "nitrogen_total").
        value (float): The value of the soil property.

    Returns:
        str: A recommendation based on the threshold category.
    """
    recommendations = {
        'ph': {
            'thresholds': {'low': (0, 5.5), 'moderate': (5.5, 7.5), 'high': (7.5, 14)},
            'recommendation': {
                'low': 'Low pH (acidic soil). Apply lime to raise pH.',
                'moderate': 'Ideal pH range for most crops.',
                'high': 'High pH (alkaline soil). Apply sulfur to lower pH.'
            }
        },
        'nitrogen_total': {
            'thresholds': {'low': (0, 0.5), 'moderate': (0.5, 1.5), 'high': (1.5, 10)},
            'recommendation': {
                'low': 'Low nitrogen. Apply nitrogen-based fertilizers.',
                'moderate': 'Adequate nitrogen for crops.',
                'high': 'High nitrogen. Monitor for nutrient leaching and avoid over-fertilizing.'
            }
        },
        'phosphorous_extractable': {
            'thresholds': {'low': (0, 10), 'moderate': (10, 50), 'high': (50, 100)},
            'recommendation': {
                'low': 'Low phosphorus. Apply phosphate fertilizers or bone meal.',
                'moderate': 'Adequate phosphorus. No specific action needed.',
                'high': 'High phosphorus. Avoid over-fertilizing with phosphorus.'
            }
        },
        'aluminium_extractable': {
            'thresholds': {'low': (0, 10), 'moderate': (10, 20), 'high': (20, 100)},
            'recommendation': {
                'low': 'Low aluminium. No action needed.',
                'moderate': 'Moderately high aluminium. Apply lime to reduce toxicity.',
                'high': 'High aluminium. Apply lime or soil amendments to neutralize excess aluminium.'
            }
        },
        'bulk_density': {
            'thresholds': {'low': (0, 1.0), 'moderate': (1.0, 1.5), 'high': (1.5, 3)},
            'recommendation': {
                'low': 'Low bulk density. Continue with current soil management practices.',
                'moderate': 'Moderate bulk density. Consider tilling or adding organic matter.',
                'high': 'High bulk density. Aerate soil and add organic matter to alleviate compaction.'
            }
        },
        'calcium_extractable': {
            'thresholds': {'low': (0, 200), 'moderate': (200, 600), 'high': (600, 2000)},
            'recommendation': {
                'low': 'Low calcium. Apply lime or gypsum to raise calcium levels.',
                'moderate': 'Adequate calcium. No specific action needed.',
                'high': 'High calcium. Monitor other nutrients for potential imbalances.'
            }
        },
        'carbon_organic': {
            'thresholds': {'low': (0, 10), 'moderate': (10, 30), 'high': (30, 100)},
            'recommendation': {
                'low': 'Low organic carbon. Add organic matter (compost, manure).',
                'moderate': 'Moderate organic carbon. Continue soil conservation practices.',
                'high': 'High organic carbon. Maintain fertility with organic matter.'
            }
        },
        'carbon_total': {
            'thresholds': {'low': (0, 15), 'moderate': (15, 40), 'high': (40, 100)},
            'recommendation': {
                'low': 'Low total carbon. Increase organic amendments and reduce tillage.',
                'moderate': 'Adequate total carbon for most plants.',
                'high': 'High total carbon. Monitor nitrogen levels to ensure balanced nutrient availability.'
            }
        },
        'clay_content': {
            'thresholds': {'low': (0, 20), 'moderate': (20, 40), 'high': (40, 100)},
            'recommendation': {
                'low': 'Low clay content (sandy soil). Add organic matter to improve water retention.',
                'moderate': 'Moderate clay content. Good soil structure for most plants.',
                'high': 'High clay content. Use raised beds or organic matter to improve drainage.'
            }
        }
        # Add more soil properties as needed...
    }

    if property_name not in recommendations:
        return f"No thresholds defined for {property_name}"

    thresholds = recommendations[property_name]['thresholds']
    recs = recommendations[property_name]['recommendation']

    # Determine the threshold category
    if thresholds['low'][0] <= value <= thresholds['low'][1]:
        return recs['low']
    elif thresholds['moderate'][0] < value <= thresholds['moderate'][1]:
        return recs['moderate']
    elif thresholds['high'][0] < value <= thresholds['high'][1]:
        return recs['high']
    else:
        return f"Value {value} is out of range for {property_name}."
