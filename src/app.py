from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = '../files/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    # Save the file
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    # After saving the file, perform your image processing here (e.g., deep learning model)
    # For example, generating links to buy the clothing item
    
    return get_dummy_data()

def get_dummy_data():
    data = {
        "type": "Shirt",
        "links": [
            {
                "name": "Men Cotton Planet & Slogan Graphic Tee",
                "price": "$10.39",
                "img_url": "https://encrypted-tbn2.gstatic.com/shopping?q=tbn:ANd9GcTaELHfHxUQVOvhEMO2rYgGOeVyZP-LsRosXyYFARy8EaOCMRbICvNzONTQJ9Ike3HFDTfcfURJBuyy5iep5URYXVVHTULRzA_8TS43cgCT21z6ZvyX5nbczLz1OIwyOSjfu0i30Qg&usqp=CAc",
                "shop_name": "Shein",
                "shop_url": "https://sg.shein.com/goods-p-15938321.html?goods_id=15938321&test=5051&url_from=shein_google_sgadplaEN_Men01_20240606&scene=1&pf=google&ad_type=DPA&language=en&siteuid=sg&landing_page_id=1510&ad_test_id=1190&requestId=olw-48lppq8ld1y6&gad_source=1&skucode=I8j4tqqdnv6a&onelink=0/googlefeed_sg&gclid=Cj0KCQiApNW6BhD5ARIsACmEbkXm9QjMgmzliptvpIjY87bTJfTDGZEsAmgHeRNBc7PWhG6qzhz_5nUaAqWREALw_wcB&setid=151265421519&currency=SGD&lang=en&cid=20418213309"
            },
            {
                "name": "Manfinity UrbanChill Men T-Shirts",
                "price": "$7.64",
                "img_url": "https://encrypted-tbn0.gstatic.com/shopping?q=tbn:ANd9GcTxeE7p9tNkaMXnpoe5We28TRlITuS7ijITXO36zWVNfpHvgyPJ0eNPrtL3LrIsrsq-ZrSSWSV_t9TH0GSZbbP1VXDblPfEgxrgfjX1tC8X3Q1IqK_ODNRJNA&usqp=CAc",
                "shop_name": "Shein",
                "shop_url": "https://sg.shein.com/goods-p-11163687.html?goods_id=11163687&test=5051&url_from=shein_google_sgadplaEN_Men01_20240606&scene=1&pf=google&ad_type=DPA&language=en&siteuid=sg&landing_page_id=1510&ad_test_id=1190&requestId=olw-48lqmc7zf3t2&gad_source=1&skucode=I62ep9jwf38b&onelink=0/googlefeed_sg&gclid=Cj0KCQiApNW6BhD5ARIsACmEbkX4GOQQtG8Hww1IJKUj1-2BuvV_NWRdWPKnEkqbweUqS69VlyYmcWgaAqJbEALw_wcB&setid=151265421519&currency=SGD&lang=en&cid=20418213309"
            },
            {
                "name": "Manfinity Modomio Men T-Shirts",
                "price": "$9.34",
                "img_url": "https://encrypted-tbn0.gstatic.com/shopping?q=tbn:ANd9GcS8gaD_thBDRf2vyAcXojeIEr0TdWW7L2lnlmwvAnkOMIgWdsadxmZQI_LNf5DJOOKdNsMFrdIvEJhNOi8RCoIxDz_-MIL_RYjuktOBp7h05Ow3dx6WTx4eSiFoY-J4b37Rr5-p4ZDYPgU&usqp=CAc",
                "shop_name": "Shein",
                "shop_url": "https://sg.shein.com/goods-p-11371152.html?goods_id=11371152&test=5051&url_from=shein_google_sgadplaEN_Men01_20240606&scene=1&pf=google&ad_type=DPA&language=en&siteuid=sg&landing_page_id=1510&ad_test_id=1190&requestId=olw-48lqr1wmy7ev&gad_source=1&skucode=I33csz3nnxq2&onelink=0/googlefeed_sg&gclid=Cj0KCQiApNW6BhD5ARIsACmEbkVc2EsAYT4h9vLy3c4FFHDhVG9LAwQD-KSTx4LI5qCvFiu8d6Pc6DsaAqdAEALw_wcB&setid=151265421519&currency=SGD&lang=en&cid=20418213309"
            },
            {
                "name": "DAZY Men's Summer Solid Short Sleeve Casual Shirt",
                "price": "$11.47",
                "img_url": "https://encrypted-tbn0.gstatic.com/shopping?q=tbn:ANd9GcRpBUpfmO-vT9FkleJGflvNKTYbE-Ubpy7AfBQIyvF7FZ5S68Uhq3gx3satMvwh7G_2hJxP-j7MV6_870woDirCuoGxuZI9Z50uNhE_RJA01G6nTkIzLKv-hCI&usqp=CAc",
                "shop_name": "Shein",
                "shop_url": "https://sg.shein.com/goods-p-34246252.html?goods_id=34246252&test=5051&url_from=shein_google_sgadplaEN_Men01_20240606&scene=1&pf=google&ad_type=DPA&language=en&siteuid=sg&landing_page_id=1510&ad_test_id=1190&requestId=olw-48lquxzu2bcw&gad_source=1&skucode=I114x57epn0w&onelink=0/googlefeed_sg&gclid=Cj0KCQiApNW6BhD5ARIsACmEbkWQ09ZomLzTHSNGH6uOK8ICVvqbnkyycG-BNtkoJReBpA8ipasOgJ0aAqrWEALw_wcB&setid=151265421519&currency=SGD&lang=en&cid=20418213309"
            },
            {
                "name": "Men Cotton Japanese Letter & Cartoon Graphic Tee",
                "price": "$10.62",
                "img_url": "https://encrypted-tbn2.gstatic.com/shopping?q=tbn:ANd9GcS_5JPcoA-JFngatHXKTlb7YsigaXQk7VOTFGkt_SQuLrlYrrkG6JMH2u4of8NReT23yF02lZKtcQVSEV68sqNrfMU_j1zkocYewW87aet6yuhh2BHu1nbCgcM&usqp=CAc",
                "shop_name": "Shein",
                "shop_url": "https://sg.shein.com/goods-p-14610414.html?goods_id=14610414&test=5051&url_from=shein_google_sgadplaEN_Men01_20240606&scene=1&pf=google&ad_type=DPA&language=en&siteuid=sg&landing_page_id=1510&ad_test_id=1190&requestId=olw-48lqzlpgirk1&gad_source=1&skucode=I5399etrqbgg&onelink=0/googlefeed_sg&gclid=Cj0KCQiApNW6BhD5ARIsACmEbkUoYi4UkAnNWEo0ErT3h7SI94HugTGRucOQIrLDDEnf15osR6iiDVkaAk4WEALw_wcB&setid=151265421519&currency=SGD&lang=en&cid=20418213309"
            }
        ]
    }

    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)