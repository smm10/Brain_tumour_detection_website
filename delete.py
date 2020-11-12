from flask import Flask, render_template, request, make_response
from flask import flash, redirect, url_for, jsonify

from my_helper_functions import make_prediction,validate_file,open_image

app = Flask(__name__)
app.config.from_pyfile('config.py')



@app.route('/', methods=['GET', 'POST'])
def index():
  if request.method == 'GET':
    return render_template('predict.html')
  if request.method == 'POST':
    data, path = validate_file(request)
    img = open_image(path)
    #data = request.files['file']
    #print(data)
    #print(filename)
    result = make_prediction(img)
    print(result)
    if(result*100>50):
      return render_template('prediction.html', img=path, result = "Tumourous", accuracy = result)
    else:
      return render_template('prediction.html', img=path, result = "Non tumorous", accuracy = 1 - result)


if __name__ == '__main__':
  app.run(debug=True)