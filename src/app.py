from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from PIL import Image, ImageOps
import numpy as np
import tensorflow as tf
import openai
from serpapi import GoogleSearch
from dotenv import load_dotenv
import json

app = Flask(__name__)
CORS(app)

class_mapping = {0: "T-Shirt", 1: "Trouser", 2: "Pullover", 3: "Dress", 4: "Coat",
                 5: "Sandal", 6: "Shirt", 7: "Sneaker", 8: "Bag", 9: "Ankle Boot"}

# model = tf.keras.models.load_model("src/model3_improved.keras")

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
SERP_API_KEY = os.getenv('SERP_API_KEY')

@app.route('/upload', methods=['POST'])
def upload_image():

    # Get the image file
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    # Get the preference
    preferences = request.form.get('preferences', '')
    print(f"PREFERENCES: {preferences}")
    
    # Transform the image and predict the category
    # category = predict_image(file)
    category = "shirt"

    # Generate links to buy the clothing item with gpt model and serpapi
    gpt_response = str(generate_response(category, preferences))
    print(f"GPT RESPONSE RAW: {gpt_response}")
    if not gpt_response.startswith('{'):
        gpt_response = gpt_response[gpt_response.find('{'):].strip()
    print(f"GPT RESPONSE JSON: {gpt_response_json}")
    gpt_response_json = json.loads(gpt_response)
    keyword = gpt_response_json['keyword']
    response = gpt_response_json['response']
    links = google_shopping_search(keyword)
    data = {
        "gpt_response": response,
        "links": links
    }
    return jsonify(data)

def load_and_preprocess_image(image_path):
    """
    Load and preprocess the image:
    1. Open the image file.
    2. Resize it to (28, 28).
    3. Convert it to grayscale.
    4. Normalize pixel values to the range [0, 1].
    5. Reshape to add the batch dimension.
    """
    image = Image.open(image_path)
    image = image.resize((28, 28))
    grayscale = ImageOps.grayscale(image)
    grayscale_np = np.array(grayscale).astype("float32") / 255.0  # Normalize to [0, 1]
    return np.expand_dims(grayscale_np, axis=(0, -1))  # Add batch and channel dimensions

def predict_image(image_path):
    """
    Given the image path, preprocess the image and predict its class.
    """
    processed_image = load_and_preprocess_image(image_path)
    predictions = model.predict(processed_image)
    predicted_class = np.argmax(predictions)
    return class_mapping[predicted_class]

def generate_response(category, preferences = ""):
    prompt = f"category: {category}. preferences: {preferences}"
    system_msg = """You are a helpful assistant for fashion and shopping recommendations. Based on the clothes category and preferences, generate json format of an effective keyword to be used in serpapi google shopping search api and a short sentence of response. Starts the response with '{' and ends with '}'
                    The format: {
                        "keyword": <the keyword>
                        "response": <1 short sentence of response> (example: Here are the recommended blue shirts:)
                    }
                """

    response = openai.ChatCompletion.create(
        model = "gpt-4o",
        api_key = OPENAI_API_KEY,
        messages = [
            {"role": "system", "content": system_msg},
            {"role": "user", "content": prompt}
        ]
    )

    return response['choices'][0]['message']['content'].strip()

def google_shopping_search(query, num_results = 5):
    params = {
        "api_key": SERP_API_KEY,
        "engine": "google_shopping",
        "q": query,
        "hl": "en",
        "gl": "sg",
        "num": num_results
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    products = []

    for item in results.get("shopping_results", []):
        product = {
            "name": shorten_text(item.get("title"), 5, 8),
            "product_url": item.get("link"),
            "shop_name": shorten_text(item.get("source"), 1, 3),
            "img_url": item.get("thumbnail"),
            "price": item.get("price")
        }
        products.append(product)

    return products

def shorten_text(text, min, max):
    system_msg = "You are a helpful assistant that is good at shortening text."
    prompt = f"Shorten this text into {min} to {max} (inclusive) words: {text}"

    response = openai.ChatCompletion.create(
        model = "gpt-4o",
        api_key = OPENAI_API_KEY,
        messages = [
            {"role": "system", "content": system_msg},
            {"role": "user", "content": prompt}
        ]
    )
    
    return response['choices'][0]['message']['content'].strip()

def get_dummy_data():
    data = {
        "gpt_response": "Here are the recommended shirts:",
        "links": [
            {
                "name": "Men Cotton Planet & Slogan Graphic Tee",
                "price": "$10.39",
                "img_url": "https://encrypted-tbn2.gstatic.com/shopping?q=tbn:ANd9GcTaELHfHxUQVOvhEMO2rYgGOeVyZP-LsRosXyYFARy8EaOCMRbICvNzONTQJ9Ike3HFDTfcfURJBuyy5iep5URYXVVHTULRzA_8TS43cgCT21z6ZvyX5nbczLz1OIwyOSjfu0i30Qg&usqp=CAc",
                "shop_name": "Shein",
                "product_url": "https://sg.shein.com/goods-p-15938321.html?goods_id=15938321&test=5051&url_from=shein_google_sgadplaEN_Men01_20240606&scene=1&pf=google&ad_type=DPA&language=en&siteuid=sg&landing_page_id=1510&ad_test_id=1190&requestId=olw-48lppq8ld1y6&gad_source=1&skucode=I8j4tqqdnv6a&onelink=0/googlefeed_sg&gclid=Cj0KCQiApNW6BhD5ARIsACmEbkXm9QjMgmzliptvpIjY87bTJfTDGZEsAmgHeRNBc7PWhG6qzhz_5nUaAqWREALw_wcB&setid=151265421519&currency=SGD&lang=en&cid=20418213309"
            },
            {
                "name": "Manfinity UrbanChill Men T-Shirts",
                "price": "$7.64",
                "img_url": "https://encrypted-tbn0.gstatic.com/shopping?q=tbn:ANd9GcTxeE7p9tNkaMXnpoe5We28TRlITuS7ijITXO36zWVNfpHvgyPJ0eNPrtL3LrIsrsq-ZrSSWSV_t9TH0GSZbbP1VXDblPfEgxrgfjX1tC8X3Q1IqK_ODNRJNA&usqp=CAc",
                "shop_name": "Shein",
                "product_url": "https://sg.shein.com/goods-p-11163687.html?goods_id=11163687&test=5051&url_from=shein_google_sgadplaEN_Men01_20240606&scene=1&pf=google&ad_type=DPA&language=en&siteuid=sg&landing_page_id=1510&ad_test_id=1190&requestId=olw-48lqmc7zf3t2&gad_source=1&skucode=I62ep9jwf38b&onelink=0/googlefeed_sg&gclid=Cj0KCQiApNW6BhD5ARIsACmEbkX4GOQQtG8Hww1IJKUj1-2BuvV_NWRdWPKnEkqbweUqS69VlyYmcWgaAqJbEALw_wcB&setid=151265421519&currency=SGD&lang=en&cid=20418213309"
            },
            {
                "name": "Manfinity Modomio Men T-Shirts",
                "price": "$9.34",
                "img_url": "https://encrypted-tbn0.gstatic.com/shopping?q=tbn:ANd9GcS8gaD_thBDRf2vyAcXojeIEr0TdWW7L2lnlmwvAnkOMIgWdsadxmZQI_LNf5DJOOKdNsMFrdIvEJhNOi8RCoIxDz_-MIL_RYjuktOBp7h05Ow3dx6WTx4eSiFoY-J4b37Rr5-p4ZDYPgU&usqp=CAc",
                "shop_name": "Shein",
                "product_url": "https://sg.shein.com/goods-p-11371152.html?goods_id=11371152&test=5051&url_from=shein_google_sgadplaEN_Men01_20240606&scene=1&pf=google&ad_type=DPA&language=en&siteuid=sg&landing_page_id=1510&ad_test_id=1190&requestId=olw-48lqr1wmy7ev&gad_source=1&skucode=I33csz3nnxq2&onelink=0/googlefeed_sg&gclid=Cj0KCQiApNW6BhD5ARIsACmEbkVc2EsAYT4h9vLy3c4FFHDhVG9LAwQD-KSTx4LI5qCvFiu8d6Pc6DsaAqdAEALw_wcB&setid=151265421519&currency=SGD&lang=en&cid=20418213309"
            },
            {
                "name": "DAZY Men's Summer Solid Short Sleeve Casual Shirt",
                "price": "$11.47",
                "img_url": "https://encrypted-tbn0.gstatic.com/shopping?q=tbn:ANd9GcRpBUpfmO-vT9FkleJGflvNKTYbE-Ubpy7AfBQIyvF7FZ5S68Uhq3gx3satMvwh7G_2hJxP-j7MV6_870woDirCuoGxuZI9Z50uNhE_RJA01G6nTkIzLKv-hCI&usqp=CAc",
                "shop_name": "Shein",
                "product_url": "https://sg.shein.com/goods-p-34246252.html?goods_id=34246252&test=5051&url_from=shein_google_sgadplaEN_Men01_20240606&scene=1&pf=google&ad_type=DPA&language=en&siteuid=sg&landing_page_id=1510&ad_test_id=1190&requestId=olw-48lquxzu2bcw&gad_source=1&skucode=I114x57epn0w&onelink=0/googlefeed_sg&gclid=Cj0KCQiApNW6BhD5ARIsACmEbkWQ09ZomLzTHSNGH6uOK8ICVvqbnkyycG-BNtkoJReBpA8ipasOgJ0aAqrWEALw_wcB&setid=151265421519&currency=SGD&lang=en&cid=20418213309"
            },
            {
                "name": "Men Japanese Letter & Cartoon Graphic Tee",
                "price": "$10.62",
                "img_url": "https://encrypted-tbn2.gstatic.com/shopping?q=tbn:ANd9GcS_5JPcoA-JFngatHXKTlb7YsigaXQk7VOTFGkt_SQuLrlYrrkG6JMH2u4of8NReT23yF02lZKtcQVSEV68sqNrfMU_j1zkocYewW87aet6yuhh2BHu1nbCgcM&usqp=CAc",
                "shop_name": "Shein",
                "product_url": "https://sg.shein.com/goods-p-14610414.html?goods_id=14610414&test=5051&url_from=shein_google_sgadplaEN_Men01_20240606&scene=1&pf=google&ad_type=DPA&language=en&siteuid=sg&landing_page_id=1510&ad_test_id=1190&requestId=olw-48lqzlpgirk1&gad_source=1&skucode=I5399etrqbgg&onelink=0/googlefeed_sg&gclid=Cj0KCQiApNW6BhD5ARIsACmEbkUoYi4UkAnNWEo0ErT3h7SI94HugTGRucOQIrLDDEnf15osR6iiDVkaAk4WEALw_wcB&setid=151265421519&currency=SGD&lang=en&cid=20418213309"
            }
        ]
    }

    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)