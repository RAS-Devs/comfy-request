import io
import json
import logging
import urllib.parse
import urllib.request

from PIL import Image

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")


def load_prompt(file_path):
    with open(file_path, "r") as file:
        prompt = json.load(file)
    return prompt


def save_image(image_data, filename):
    image = Image.open(io.BytesIO(image_data))
    image.save(filename)
    logging.info(f"Image saved to {filename}")


def queue_prompt(prompt, server_address, client_id):
    p = {"prompt": prompt, "client_id": client_id}
    data = json.dumps(p).encode("utf-8")
    req = urllib.request.Request(f"http://{server_address}/prompt", data=data)
    logging
    return json.loads(urllib.request.urlopen(req).read())


def get_image(filename, subfolder, folder_type, server_address):
    data = {"filename": filename, "subfolder": subfolder, "type": folder_type}
    url_values = urllib.parse.urlencode(data)
    with urllib.request.urlopen(
        f"http://{server_address}/view?{url_values}"
    ) as response:
        return response.read()


def get_history(prompt_id, server_address):
    with urllib.request.urlopen(
        f"http://{server_address}/history/{prompt_id}"
    ) as response:
        return json.loads(response.read())


def get_images(ws, prompt, server_address, client_id):
    prompt_id = queue_prompt(prompt, server_address, client_id)["prompt_id"]
    output_images = {}

    while True:
        out = ws.recv()
        if isinstance(out, str):
            message = json.loads(out)
            if message["type"] == "executing":
                data = message["data"]
                if data["node"] is None and data["prompt_id"] == prompt_id:
                    break  # Execution is done
        else:
            continue  # previews are binary data

    history = get_history(prompt_id, server_address)[prompt_id]
    for node_id in history["outputs"]:
        node_output = history["outputs"][node_id]
        images_output = []
        if "images" in node_output:
            for image in node_output["images"]:
                image_data = get_image(
                    image["filename"], image["subfolder"], image["type"], server_address
                )
                images_output.append(image_data)
        output_images[node_id] = images_output

    return output_images
