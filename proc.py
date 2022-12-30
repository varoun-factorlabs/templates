import numpy as np
#import cv2 as cv
import sys
from  PIL  import Image
import os
import requests
import wget
import json

def compute(INPUT_FG: str, INPUT_BG: str, OUTPUT: str, FG_TKN: str, BG_TKN: str):

  url = f"https://api.opensea.io/api/v1/assets?token_ids={FG_TKN}&asset_contract_address=0x8a90cab2b38dba80c64b7734e58ee1db38b8992e&order_direction=desc&offset=0&limit=20"

  headers = {"X-API-KEY": "7573a098035e499aba7b7f745b6e7f6c"}

  response = requests.request("GET", url, headers=headers)

  metadata = json.loads(response.text)

  image_url = metadata["assets"][0]["image_url"]

  wget.download(image_url, INPUT_FG)

  url = f"https://api.opensea.io/api/v1/assets?token_ids={BG_TKN}&asset_contract_address=0x614917F589593189ac27aC8B81064CBe450C35e3&order_direction=desc&offset=0&limit=20"

  headers = {"X-API-KEY": "7573a098035e499aba7b7f745b6e7f6c"}

  response = requests.request("GET", url, headers=headers)

  metadata = json.loads(response.text)

  image_url = metadata["assets"][0]["image_url"]

  wget.download(image_url, INPUT_BG)

  img = cv.imread(INPUT_FG, cv.IMREAD_UNCHANGED)
  cv.imwrite(f'static/results/{INPUT_FG}', img)

  original = img.copy()

  l = int(max(5, 6))
  u = int(min(6, 6))

  ed = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
  edges = cv.GaussianBlur(img, (21, 51), 3)
  edges = cv.cvtColor(edges, cv.COLOR_BGR2GRAY)
  edges = cv.Canny(edges, l, u)

  _, thresh = cv.threshold(edges, 0, 255, cv.THRESH_BINARY  + cv.THRESH_OTSU)
  kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (5, 5))
  mask = cv.morphologyEx(thresh, cv.MORPH_CLOSE, kernel, iterations=4)

  data = mask.tolist()
  sys.setrecursionlimit(10**8)
  for i in  range(len(data)):
      for j in  range(len(data[i])):
          if data[i][j] !=  255:
              data[i][j] =  -1
          else:
              break
      for j in  range(len(data[i])-1, -1, -1):
          if data[i][j] !=  255:
              data[i][j] =  -1
          else:
              break
  image = np.array(data)
  image[image !=  -1] =  255
  image[image ==  -1] =  0

  mask = np.array(image, np.uint8)

  result = cv.bitwise_and(original, original, mask=mask)
  result[mask ==  0] =  255
  cv.imwrite('bg.png', result)


  img = Image.open('bg.png')
  img.convert("RGBA")
  datas = img.getdata()

  newData = []
  for item in datas:
      if item[0] ==  255  and item[1] ==  255  and item[2] ==  255:
          newData.append((255, 255, 255, 0))
      else:
          newData.append(item)

  img.putdata(newData)
  img.save("img.png", "PNG")


  # creating a image object (main image)
  im1 = Image.open(INPUT_BG)
  im1.save(f'static/results/{INPUT_BG}', "PNG")

  if im1.size[0] > im1.size[1]:

      im1 = im1.crop((0, 0, im1.size[1], im1.size[1]))

  elif  im1.size[0] > im1.size[1]:
      
      im1 = im1.crop((0, 0, im1.size[0], im1.size[0]))

  # creating a image object (image which is to be paste on main image)
  im2 = Image.open("bg.png")

  im2_a = im2.convert("RGBA")
  datas = im2_a.getdata()

  newData = []
  for item in datas:
      if item[0] == 255 and item[1] == 255 and item[2] == 255:
          newData.append((255, 255, 255, 0))
      else:
          newData.append(item)

  im2_a.putdata(newData)

  im2_a.save("no_bg.png", "PNG")

  #im3 = Image.open("no_bg.png")

  WIDTH = im1.size[0]
  HEIGHT = im1.size[0]
  # Image.open() can also open other image types
  img = Image.open("no_bg.png")
  # WIDTH and HEIGHT are integers
  resized_img = img.resize((WIDTH, HEIGHT))
  resized_img.save("resized_image.png")
  resized_im = Image.open("resized_image.png")
  
  # paste image giving dimensions
  im1.paste(resized_im, (0, 0), resized_im)
  #im1.paste(resized_im,resized_im)

  im1.save(f'static/results/{OUTPUT}')

  os.remove(INPUT_FG)
  os.remove(INPUT_BG)