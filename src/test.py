import tensorflow as tf
from PIL import Image, ImageOps
import numpy as np

model = tf.keras.models.load_model("model3.keras")

class_mapping = {0: "T-Shirt", 1: "Trouser", 2: "Pullover", 3: "Dress", 4: "Coat",
                 5: "Sandal", 6: "Shirt", 7: "Sneaker", 8: "Bag", 9: "Ankle Boot"}

def load_and_preprocess_image(image_path):
    image = Image.open(image_path)
    image = image.resize((28, 28))
    grayscale = ImageOps.grayscale(image)
    grayscale_np = np.array(grayscale).astype("float32") / 255.0  # Normalize to [0, 1]
    return np.expand_dims(grayscale_np, axis=(0, -1))  # Add batch and channel dimensions

def predict_image(image_path):
    processed_image = load_and_preprocess_image(image_path)
    predictions = model.predict(processed_image)
    predicted_class = np.argmax(predictions)
    return class_mapping[predicted_class]

print(predict_image("dress.png"))