"""
utils.py - This module contains utility functions for the TreeMatch application.
--------------------------------------------------------------------------------
It includes functions for retrieving soil properties, generating soil recommendations,
and identifying plants using the Plant.id API.
"""
import os
import json
import datetime
import logging
import requests
from dotenv import load_dotenv
from flask import request, jsonify


# Load environment variables from .env file
load_dotenv()


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
        response = requests.get(base_url, params=params, timeout=10)
        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()
            # Extract the property and value
            property_data = data.get('property', {}).get(property_name, [])
            if property_data:
                value = property_data[0].get('value', {}).get('value')
                return {'property': property_name, 'value': value}
        else:
            # Raises an HTTPError for bad responses
            response.raise_for_status()
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


def soil_recommendation(lat: float, lon: float, properties: list) -> dict:
    """
    Generates a soil recommendation report based on a list of properties.

    Args:
        lat (float): Latitude of the location.
        lon (float): Longitude of the location.
        properties (list): List of soil properties to query (e.g., ["ph", "nitrogen"]).

    Returns:
        dict: A dictionary containing the soil recommendation report.
    """
    report = {}
    print("properties passed to function")
    print(properties)
    for property_name in properties:
        # Get the soil property value
        soil_property = get_soil_property(
            lat, lon, property_name)
        value = soil_property.get('value')

        if value is not None:
            # Get the recommendation based on the property value
            recommendation = get_recommendation(property_name, value)
            report[property_name] = {
                'value': value,
                'recommendation': recommendation
            }
        else:
            report[property_name] = {
                'value': None,
                'recommendation': None
            }

    return report


def identify_plant(image_data_base64: str, latitude: float, longitude: float) -> dict:
    """
    Identifies a plant using the Plant.id API.

    Args:
            image_data_base64 (str): Base64 encoded image data.
            latitude (float): Latitude of the location.
            longitude (float): Longitude of the location.

    Returns:
            dict: Plant identification information.
    """
    # Call Plant.id API using requests
    api_key = os.getenv('API_KEY')
    plant_id_url = "https://plant.id/api/v3/identification"
    plant_id_url1 = "https://plant.id/api/v3/identification?details=common_names,url,description,taxonomy,rank,gbif_id,inaturalist_id,image,synonyms,edible_parts,watering,propagation_methods,best_watering,best_light_condition,best_soil_type,common_uses,toxicity,cultural_significance"
    headers = {
        'Api-Key': api_key,
        'Content-Type': 'application/json'
    }
    plant_id_data = {
        "images": [image_data_base64],
        "latitude": latitude,
        "longitude": longitude,
        "similar_images": True
    }

    try:
        plant_id_response = requests.post(
            plant_id_url1, json=plant_id_data, headers=headers, timeout=30)
        logging.info(f"Plant.id API response: {plant_id_response.text}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Request failed: {e}")
        return {"error": "Request to Plant.id API failed"}

    if plant_id_response.status_code != 201:
        logging.error(
            f"Unexpected status code: {plant_id_response.status_code}")
        logging.error(f"Response content: {plant_id_response.text}")
        return {"error": "Unexpected response from Plant.id API"}

    try:
        plant_info = plant_id_response.json()
    except requests.exceptions.JSONDecodeError as e:
        logging.error(f"JSON decode error: {e}")
        logging.error(f"Response content: {plant_id_response.text}")
        return {"error": "Failed to decode JSON response from Plant.id API"}

    return plant_info

    # plant_id_response = requests.post(
    #     plant_id_url, json=plant_id_data, headers=headers, timeout=10)
    # plant_info = plant_id_response.json()

    # return plant_info


def get_simulated_response(api_response):
    """
    Reads the simulated response from a file and returns the parsed JSON.

    Args:
        api_response (dict): Parsed JSON response.

    Returns:
        str: JSON-formatted string of the plant response.
    """
    # with open(file_path, 'r') as file:
    #     plant_info = json.load(file)

    plant_info = api_response

    access_token = plant_info.get("access_token")
    model_version = plant_info.get("model_version")
    input_details = plant_info.get("input", {})
    latitude = input_details.get("latitude")
    longitude = input_details.get("longitude")
    image = input_details.get("images")
    status = plant_info.get("status")
    created = plant_info.get("created")
    is_plant = plant_info.get("result", {}).get("is_plant", {}).get("binary")
    is_plant_probability = plant_info.get(
        "result", {}).get("is_plant", {}).get("probability")

    suggestions = plant_info.get("result", {}).get(
        "classification", {}).get("suggestions", [])

    all_suggestions_info = []

    if suggestions:
        for suggestion in suggestions:
            details = suggestion.get("details", {})
            description = details.get("description")
            description_value = description.get(
                "value") if description else None

            suggestion_info = {
                "plant_name": suggestion.get("name"),
                "probability": suggestion.get("probability"),
                "similar_images": [],
                "common_names": details.get("common_names", []),
                "synonyms": details.get("synonyms", []),
                "rank": details.get("rank"),
                "description": description_value,
                "image_url": details.get("image", {}).get("value"),
                "edible_parts": details.get("edible_parts", []),
                "watering": details.get("watering", {}),
                "propagation_methods": details.get("propagation_methods"),
                "best_watering": details.get("best_watering"),
                "best_soil_type": details.get("best_soil_type")
            }

            similar_images = suggestion.get("similar_images", [])
            for img in similar_images:
                image_info = {
                    "url": img.get("url"),
                    "similarity": img.get("similarity")
                }
                suggestion_info["similar_images"].append(image_info)

            all_suggestions_info.append(suggestion_info)

    # Create plant_response dictionary
    plant_response = {
        "access_token": access_token,
        "model_version": model_version,
        "latitude": latitude,
        "longitude": longitude,
        "image": image,
        "is_image__plant": is_plant,
        "is_plant_probability": is_plant_probability,
        "suggestions": all_suggestions_info,
        "search_status": status,
        "created": created,
        "created_at": datetime.datetime.now().isoformat()
    }

    # Convert plant_response to JSON
    plant_response_json = json.dumps(plant_response, indent=4)

    # Print plant_response JSON for debugging
    # print(plant_response_json)

    return plant_response_json
