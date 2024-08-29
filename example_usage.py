import random
import uuid
from datetime import datetime


import websocket

import utils

# Client configuration
server_address: str = "dgx4:8188"
client_id: str = "alex"  # for random -> str(uuid.uuid4())
prompt_path = "./dgx_workflow.json"
output_path = "output"

prompt = utils.load_prompt(prompt_path)

# Modify the workflow
prompt["39"]["inputs"]["text"] = "masterpiece best quality painting"
prompt["40"]["inputs"][
    "text"
] = "naked, nude, nsfw, erotic, sexy"  # Negative text if needed
seed = random.randint(0, 1000000)
prompt["3"]["inputs"]["seed"] = seed


# Connect to the WebSocket server
ws = websocket.WebSocket()
ws.connect(f"ws://{server_address}/ws?clientId={client_id}")

# Get the images
images = utils.get_images(ws, prompt, server_address, client_id)
# image = Image.open(io.BytesIO(image_data))

# Save the images optional
for node_id in images:
    for image_data in images[node_id]:
        formatted_time = datetime.now().strftime("%y%m%d_%H%M")
        utils.save_image(
            image_data, f"{output_path}/{client_id}_{formatted_time}_s{seed}.png"
        )


# Close the WebSocket connection
ws.close()
