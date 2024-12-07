from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads/'
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
    links = [
        "https://www.googleadservices.com/pagead/aclk?sa=L&ai=DChcSEwjY98PlpI2KAxWJEoMDHd7PEsMYABAWGgJzZg&ae=2&aspm=1&co=1&ase=2&gclid=CjwKCAiA9bq6BhAKEiwAH6bqoA4-3yBu4gBvr3SSfBQbTYxrDWmh38vgJxS12EXDwlyic4_KSOgiuRoC_C0QAvD_BwE&ohost=www.google.com&cid=CAESVuD2bTfWCGg1DRx7c3Gq0-RMJpJVMXdUzHMHTDo3q0HYDJumubGhiCIg-8gPrZ_vATFfVG8VLBQDDcyhzXEarplxPZUNZ1EVKLN-8La3XmruiR5908Wh&sig=AOD64_0sn6XU_P2Ik8_nyVDDRWEqO4bACw&ctype=5&q=&nis=4&ved=2ahUKEwiH2b7lpI2KAxVszTgGHTMOHgcQ9aACKAB6BAgMEBI&adurl=",
        "https://www.googleadservices.com/pagead/aclk?sa=L&ai=DChcSEwjY98PlpI2KAxWJEoMDHd7PEsMYABAfGgJzZg&ae=2&aspm=1&co=1&ase=2&gclid=CjwKCAiA9bq6BhAKEiwAH6bqoG7ZChojOWgMxFLC5QELve5AYmLtfkWc3c9UKvjV52IIP4WaPxp2MhoCBB8QAvD_BwE&ohost=www.google.com&cid=CAESVuD2bTfWCGg1DRx7c3Gq0-RMJpJVMXdUzHMHTDo3q0HYDJumubGhiCIg-8gPrZ_vATFfVG8VLBQDDcyhzXEarplxPZUNZ1EVKLN-8La3XmruiR5908Wh&sig=AOD64_1DC_mVwdcedn3QCeGbT6k_RFgh5Q&ctype=5&q=&nis=4&ved=2ahUKEwiH2b7lpI2KAxVszTgGHTMOHgcQ9aACKAB6BAgMEB8&adurl=",
        "https://www.googleadservices.com/pagead/aclk?sa=L&ai=DChcSEwjY98PlpI2KAxWJEoMDHd7PEsMYABAiGgJzZg&ae=2&aspm=1&co=1&ase=2&gclid=CjwKCAiA9bq6BhAKEiwAH6bqoGXHPpNcPg1GZ6a8Tk6vp0gw6L9pDOb8UOrdaqggF5n_7JVyeru2LBoCG3oQAvD_BwE&ohost=www.google.com&cid=CAESVuD2bTfWCGg1DRx7c3Gq0-RMJpJVMXdUzHMHTDo3q0HYDJumubGhiCIg-8gPrZ_vATFfVG8VLBQDDcyhzXEarplxPZUNZ1EVKLN-8La3XmruiR5908Wh&sig=AOD64_1nOnrds8aKOVk6QxMe-kuFHLZy7g&ctype=5&q=&nis=4&ved=2ahUKEwiH2b7lpI2KAxVszTgGHTMOHgcQ9aACKAB6BAgMECw&adurl=",
    ]
    
    return jsonify({"links": links})

if __name__ == '__main__':
    app.run(debug=True)
