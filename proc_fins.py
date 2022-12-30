import numpy as np
import sys
from PIL import Image
import os
import requests
import wget
import json


def compute(INPUT_FG: str, INPUT_BG: str, OUTPUT: str, DOOD_TKN: str,
            DRINK_TKN: str):

  # download doodle image
  url = f"https://deep-index.moralis.io/api/v2/nft/0x8a90CAb2b38dba80c64b7734e58Ee1dB38B8992e/{DOOD_TKN}"

  params = {
    "chain": "eth",
  }

  headers = {
    "X-API-KEY":
    "Yj6gNd9QGdurZ3PXaAW8rRA5XSyl4wBb0qhSTOKUpXS5sml0Zvt6pKjubkgN7jXh"
  }

  response = requests.request("GET", url, headers=headers, params=params)

  metadata = json.loads(response.text)

  image_metadata = metadata["metadata"]

  image_metadata_json = json.loads(image_metadata)

  image_hash = image_metadata_json["image"][7:]

  image_URL = f'https://ipfs.moralis.io:2053/ipfs/{image_hash}'

  print(image_URL)

  #wget.download(image_URL)

  img_data = requests.get(image_URL).content

  with open('image_name.jpg', 'wb') as handler:
    handler.write(img_data)

  drink_dict = {
    "all_time_merlot": "https://i.ibb.co/j6S4ZMy/all-time-merlot-1.png",
    "bandit_ipa": "https://i.ibb.co/V311sPX/bandit-ipa-1.png",
    "blocktini": "https://i.ibb.co/9tndL8P/blocktini-1.png",
    "bull_run_brut": "https://i.ibb.co/cx6k6Md/bull-run-brut-1.png",
    "downbad_daquiri": "https://i.ibb.co/3rRmkmh/downbad-daquiri-1.png",
    "gm_and_tonic": "https://i.ibb.co/nBSJ2kx/gm-and-tonic-1.png",
    "grail": "https://i.ibb.co/j3s6Xwc/grail-1.png",
    "juicy_brew": "https://i.ibb.co/DKYy16c/juicy-brew-1.png",
    "long_island": "https://i.ibb.co/59Z9hsD/long-island-1.png",
    "metaverse_mule": "https://i.ibb.co/cxxB8sK/metaverse-mule-1.png",
    "moonhattan": "https://i.ibb.co/B3M1FRb/moonhattan-1.png",
    "poopiecolada": "https://i.ibb.co/VpTgY1h/poopiecolada-1.png",
    "ruggarita": "https://i.ibb.co/SmqQdMV/ruggarita-1.png",
    "wagmi": "https://i.ibb.co/hcS5L8Z/wagmi-1.png",
    "water": "https://i.ibb.co/wsQJ2Yg/water-1.png",
    "wen_mint": "https://i.ibb.co/Gct6ZCM/wen-mint-1.png",
    "zaddy_chill": "https://i.ibb.co/VmGQtvD/zaddy-chill-1.png",
  }

  # download drink image

  drink_img = requests.get(drink_dict[DRINK_TKN]).content

  with open('drink.png', 'wb') as handler:
    handler.write(drink_img)

  # Back Image
  filename = 'image_name.jpg'

  # Mid Image
  filename1 = f'drink.png'

  # Open Back Image
  backImage = Image.open(filename)

  # Open Mid Image
  midImage = Image.open(filename1)

  # Convert image to RGBA
  backImage = backImage.convert("RGBA")

  # Convert image to RGBA
  midImage = midImage.convert("RGBA")

  #WIDTH = backImage.size[0]
  #HEIGHT = backImage.size[0]

  WIDTH = 800
  HEIGHT = 800

  resized_img = midImage.resize((WIDTH, HEIGHT))
  resized_img.save("resized_image.png")

  back_resized_img = backImage.resize((WIDTH, HEIGHT))
  back_resized_img.save("back_resized_img.png")

  # Paste the frontImage at (width, height)
  back_resized_img.paste(resized_img, (0, 0), resized_img)

  # Save this image
  back_resized_img.save(f"static/results/framed_doodle1.png", format="png")
