import numpy as np
import cv2
import cv2.aruco as aruco
from PIL import Image
import os
import requests
import wget
import json

#opencv-contrib-python              4.5.4.60
#opencv-python                      4.5.5.62

#pip install opencv-contrib-python==4.5.4.60
#pip install opencv-python==4.5.5.62


def findArucoMarkers(img, markerSize=4, totalMarkers=250, draw=True):
  imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  key = getattr(aruco, f'DICT_{markerSize}X{markerSize}_{totalMarkers}')
  arucoDict = aruco.Dictionary_get(key)
  arucoParam = aruco.DetectorParameters_create()
  bboxs, ids, rejected = aruco.detectMarkers(imgGray,
                                             arucoDict,
                                             parameters=arucoParam)

  if draw:
    aruco.drawDetectedMarkers(img, bboxs)

  return [bboxs, ids]


def augmentAruco(bbox, id, img, imgAug, drawId=True):

  tl = bbox[0][0][0], bbox[0][0][1]
  tr = bbox[0][1][0], bbox[0][1][1]
  br = bbox[0][2][0], bbox[0][2][1]
  bl = bbox[0][3][0], bbox[0][3][1]

  h, w, c = imgAug.shape

  pts1 = np.array([tl, tr, br, bl])
  pts2 = np.float32([[0, 0], [w, 0], [w, h], [0, h]])

  matrix, _ = cv2.findHomography(pts2, pts1)
  imgOut = cv2.warpPerspective(imgAug, matrix, (img.shape[1], img.shape[0]))
  cv2.fillConvexPoly(img, pts1.astype(int), (0, 0, 0))

  return imgOut


def computeRoom(INPUT_FG: str, INPUT_BG: str, OUTPUT: str, DOOD_TKN: str,
                FG_TKN: str):

  #https://i.ibb.co/nkCsx4G/room.png

  room_URL = f'https://i.ibb.co/nkCsx4G/room.png'

  img_data = requests.get(room_URL).content

  with open('room_image.png', 'wb') as handler:
    handler.write(img_data)

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

  img = cv2.imread("room.png")
  imgAug = cv2.imread("image_name.jpg")

  arucoFound = findArucoMarkers(img)

  if len(arucoFound[0]) != 0:
    for bbox, id in zip(arucoFound[0], arucoFound[1]):
      #print(bbox)
      imgNew = augmentAruco(bbox, id, img, imgAug)

      cv2.imwrite("newtest1.png", imgNew)

  # Back Image
  filename = f'newtest1.png'

  # Mid Image
  filename1 = f'room_empty.png'

  # Open Back Image
  backImage = Image.open(filename)

  # Open Mid Image
  midImage = Image.open(filename1)

  # Convert image to RGBA
  backImage = backImage.convert("RGBA")

  # Convert image to RGBA
  midImage = midImage.convert("RGBA")

  WIDTH = 800
  HEIGHT = 800

  resized_img = midImage.resize((WIDTH, HEIGHT))
  resized_img.save("resized_image.png")

  back_resized_img = backImage.resize((WIDTH, HEIGHT))
  back_resized_img.save("back_resized_img.png")

  # Paste the frontImage at (width, height)
  back_resized_img.paste(resized_img, (0, 0), resized_img)

  # Save this image
  back_resized_img.save(f"room_merged.png", format="png")
