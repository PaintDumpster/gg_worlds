import requests
import json
import os
from io import BytesIO
from PIL import Image, UnidentifiedImageError
import requests.exceptions
from openai import OpenAI
import sys

# === Load API Keys from secrets.json ===
try:
    with open("secrets.json", "r") as f:
        secrets = json.load(f)
except (FileNotFoundError, json.JSONDecodeError) as e:
    print(f"Error loading secrets.json: {e}")
    secrets = {}

open_api_key = secrets.get("OPEN_API_KEY")
google_places_api_key = secrets.get("GOOGLE_PLACES_API_KEY")
google_cse_api_key = secrets.get("GOOGLE_CSE_API_KEY")
google_cse_id = secrets.get("GOOGLE_CSE_ID")

client = OpenAI(api_key=open_api_key)

# === Main Function to Classify Prompt and Fetch Images ===
def determine_strategy_and_fetch_images(user_prompt):
    chat_prompt = f"""
    You are an assistant that helps determine the strategy for fetching landmark images.
    Given the following user prompt: "{user_prompt}",
    please analyze the prompt and decide if the user is referring to a city name (STRATEGY A) or a descriptive query (STRATEGY B).
    If it is a city name, respond with JSON formatted as:
    {{
        "strategy": "A",
        "city": "<extracted_city_name>"
    }}
    If it is a descriptive query, respond with JSON formatted as:
    {{
        "strategy": "B",
        "description": "<extracted_description>"
    }}
    Do not include any additional text in your response.
    """

    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that classifies user prompts into strategies for fetching landmark images."
            },
            {"role": "user", "content": chat_prompt}
        ]
    )


    strategy_data = json.loads(response.choices[0].message.content)

    if strategy_data["strategy"] == "A":
        return get_landmarks_by_city(strategy_data["city"])
    elif strategy_data["strategy"] == "B":
        return get_landmarks_by_description(strategy_data["description"])
    else:
        return []

# === Strategy A: Get Images by City ===
def get_landmarks_by_city(city):
    endpoint = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {
        "query": f"famous landmarks in {city}",
        "key": google_places_api_key
    }

    response = requests.get(endpoint, params=params)
    data = response.json()

    print("Google Places API response:")
    print(json.dumps(data, indent=2))

    if "results" not in data:
        return []

    image_links = []
    for landmark in data["results"][:10]:
        if "photos" in landmark:
            ref = landmark["photos"][0]["photo_reference"]
            photo_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photo_reference={ref}&key={google_places_api_key}"
            image_links.append(photo_url)

    return download_images_from_urls(image_links)

# === Strategy B: Get Images by Description ===
def get_landmarks_by_description(description):
    endpoint = "https://www.googleapis.com/customsearch/v1"
    params = {
        "q": description,
        "cx": google_cse_id,
        "searchType": "image",
        "num": 10,
        "key": google_cse_api_key
    }

    response = requests.get(endpoint, params=params)
    results = response.json()

    if "items" not in results:
        return []

    image_links = [item["link"] for item in results["items"]]
    return download_images_from_urls(image_links)

# === Helper Function to Download Images from URLs ===
def download_images_from_urls(urls):
    pil_images = []
    for url in urls:
        try:
            img_response = requests.get(url, stream=True)
            img_response.raise_for_status()
            img = Image.open(BytesIO(img_response.content)).convert("RGB")
            pil_images.append(img)
        except (requests.exceptions.RequestException, UnidentifiedImageError) as e:
            print(f"Failed to process {url}: {e}")
    return pil_images

if __name__ == "__main__":

    prompt = sys.argv[1] if len(sys.argv) > 1 else "default"
    images = determine_strategy_and_fetch_images(prompt)

    print(f"\nGot {len(images)} images from: \"{prompt}\"")

    for i, img in enumerate(images):
        img_path = f"test_image_{i}.jpg"
        img.save(img_path)
        print(f"Saved: {img_path}")

