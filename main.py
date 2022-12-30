from flask import Flask, render_template, request
from werkzeug.serving import run_simple
import os
import proc_fins

RESULTS_FOLDER = os.path.join('static', 'results')

app = Flask('app')

app.config['UPLOAD_FOLDER'] = RESULTS_FOLDER


@app.route('/')
def index():
  return render_template("index.html")


@app.route('/compute')
def student():
  return render_template('compute.html')


@app.route('/result', methods=['POST', 'GET'])
def result():
  if request.method == 'POST':
    #result = request.form
    Doodle = request.form.get("Doodle")
    drink = request.form.get("drink")
    proc_fins.compute("AAA.png", "BBB.png", "final_new.png",
                      str(Doodle).zfill(4), drink)
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'final_new.png')
    AAA = os.path.join(app.config['UPLOAD_FOLDER'], 'AAA.png')
    BBB = os.path.join(app.config['UPLOAD_FOLDER'], 'BBB.png')
    return render_template("result.html",
                           user_image=full_filename,
                           AAA_image=AAA,
                           BBB_image=BBB,
                           dood_num=str(Doodle).zfill(4))


run_simple("0.0.0.0", 5407, app, use_reloader=False)
#app.run(host='0.0.0.0', port=8080)
