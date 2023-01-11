import numpy as np
import sys
from PIL import Image

Image.LOAD_TRUNCATED_IMAGES = True
import os
import requests
import wget
import json

#https://dood-collection-test.s3.amazonaws.com/8686.png


def computeUnderwater(INPUT_FG: str, INPUT_BG: str, OUTPUT: str, DOOD_TKN: str,
                      FG_TKN: str):

  image_URL = f'https://i.ibb.co/PZzzcjr/back.png'

  print(image_URL)

  #wget.download(image_URL)

  img_data = requests.get(image_URL).content

  with open('back_image.jpg', 'wb') as handler:
    handler.write(img_data)

  image_URL = f'https://dood-collection-test.s3.amazonaws.com/{DOOD_TKN}.png'

  print(image_URL)

  #wget.download(image_URL)

  img_data = requests.get(image_URL).content

  with open('dood_image.png', 'wb') as handler:
    handler.write(img_data)

  # download drink image

  drink_img = requests.get(FG_TKN).content

  with open('front_image.png', 'wb') as handler:
    handler.write(drink_img)

  # Back Image
  filename = 'back_image.jpg'

  # Mid Image
  filename1 = f'dood_image.png'

  # Front Image
  filename2 = f'front_image.png'

  # Open Back Image
  backImage = Image.open(filename)

  # Open Mid Image
  midImage = Image.open(filename1)

  # Open Front Image
  frontImage = Image.open(filename2)

  # Convert image to RGBA
  backImage = backImage.convert("RGBA")

  # Convert image to RGBA
  midImage = midImage.convert("RGBA")

  # Convert image to RGBA
  frontImage = frontImage.convert("RGBA")

  #WIDTH = backImage.size[0]
  #HEIGHT = backImage.size[0]

  WIDTH = 800
  HEIGHT = 800

  resized_img = midImage.resize((510, 510))
  resized_img.save("resized_image.png")

  back_resized_img = backImage.resize((WIDTH, HEIGHT))
  back_resized_img.save("back_resized_img.png")

  front_resized_img = frontImage.resize((WIDTH, HEIGHT))

  # Paste the frontImage at (width, height)
  back_resized_img.paste(resized_img, (150, 150), resized_img)

  # Paste the frontImage at (width, height)
  back_resized_img.paste(front_resized_img, (0, 0), front_resized_img)

  # Save this image
  back_resized_img.save(f"static/results/underwater_doodle1.png", format="png")


########################################################################
################################  PIP   ################################
########################################################################


def computePip(INPUT_FG: str, INPUT_BG: str, OUTPUT: str, DOOD_TKN: str,
               PIP_TKN: str):

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

  # print(DOOD_TKN)
  # print(url)

  image_metadata = metadata["metadata"]

  image_metadata_json = json.loads(image_metadata)

  image_hash = image_metadata_json["image"][7:]

  #image_URL = f'https://ipfs.moralis.io:2053/ipfs/{image_hash}'
  image_URL = f'https://gateway.moralisipfs.com/ipfs/{image_hash}'

  print(image_URL)

  #wget.download(image_URL)

  img_data = requests.get(image_URL).content

  with open('image_name.jpg', 'wb') as handler:
    handler.write(img_data)

  # download drink image

  drink_img = requests.get(PIP_TKN).content

  with open('pip.png', 'wb') as handler:
    handler.write(drink_img)

  # Back Image
  filename = 'image_name.jpg'

  # Mid Image
  filename1 = f'pip.png'

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
  back_resized_img.save(f"static/results/pip_doodle1.png", format="png")
