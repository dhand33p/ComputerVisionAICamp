from flask import Flask, render_template, request
from io import BytesIO
import requests

app = Flask(__name__)


API_URL = "https://api-inference.huggingface.co/models/dhand33p/detectindfood"
headers = {"Authorization": "Bearer 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"}


@app.route("/", methods=['GET'])
def index():
  return render_template("index.html")

@app.route("/predict", methods=['POST'])
def predict():
  imagefile = request.files['image']
  img_bytes = imagefile.read()
  img_bytes = BytesIO(img_bytes)
  print(img_bytes, 'sss')
  result = query(img_bytes)
  return render_template("result.html", result = result)


def query(img):
    #with open(img, "rb") as f:
        #data = f.read()
  response = requests.post(API_URL, headers=headers, data=img)
  data = response.json()
  highest_score_dict = max(data, key=lambda x: x['score'])
  label = highest_score_dict['label']
  score = highest_score_dict['score']
  
  if label == 'ind':
      prediction = f"The predicted food type is Indian with a score of {round(score, 3)}"

  elif label == 'med':
      prediction = f"The predicted food type is Mediterrean with a score of {round(score, 3)}"
  else:
       prediction = "There is no predicted type, upload a different image of the food!"

  print(data)
  return prediction

  

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=81, debug=True)
