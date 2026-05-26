import io
import os
import sys

import requests
from PIL import Image, ImageDraw


def draw_bounding_box(image: Image.Image, bounding_box: dict) -> None:
    draw = ImageDraw.Draw(image)
    w, h = image.size
    left = bounding_box["left"] * w
    top = bounding_box["top"] * h
    box_w = bounding_box["width"] * w
    box_h = bounding_box["height"] * h
    draw.rectangle([left, top, left + box_w, top + box_h], outline="red", width=7)


def detect_containers(prediction_url: str, prediction_key: str, image_url: str) -> None:
    headers = {
        "Prediction-Key": prediction_key,
        "Content-Type": "application/json",
    }
    response = requests.post(prediction_url, headers=headers, json={"Url": image_url}, timeout=30)

    if response.status_code != 200:
        print(f"Erro na requisição: {response.status_code}\n{response.text}", file=sys.stderr)
        return

    predictions = response.json()
    print(predictions)

    img_response = requests.get(image_url, timeout=30)
    image = Image.open(io.BytesIO(img_response.content))

    for pred in predictions.get("predictions", []):
        if pred.get("tagName", "").lower() == "container" and pred.get("probability", 0) > 0.5:
            print(f"Container detectado com {pred['probability']:.1%} de confiança.")
            draw_bounding_box(image, pred["boundingBox"])

    image.show()


if __name__ == "__main__":
    key = os.getenv("AZURE_PREDICTION_KEY")
    url = os.getenv("AZURE_PREDICTION_URL")

    if not key or not url:
        sys.exit(
            "Erro: defina as variáveis de ambiente AZURE_PREDICTION_KEY e AZURE_PREDICTION_URL.\n"
            "Copie .env.example para .env e preencha os valores."
        )

    image_url = "https://containerdesign.com.br/wp-content/uploads/2024/01/alconet-1-4.jpg"
    detect_containers(url, key, image_url)
