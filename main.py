from flask import Flask, render_template, request
#from werkzeug.serving import run_simple
import os
import proc_fins

RESULTS_FOLDER = os.path.join('static', 'results')

app = Flask('app')

app.config['UPLOAD_FOLDER'] = RESULTS_FOLDER


@app.route('/')
def index():
  remix = False
  return render_template("gallery.html", remix=remix)


# @app.route('/compute')
# def student():
#   return render_template('compute.html')

# @app.route('/gallery')
# def student():
#   remix = False
#   return render_template('gallery.html', remix=remix)


@app.route('/result', methods=['POST', 'GET'])
def result():
  remix = True
  if request.method == 'POST':
    #result = request.form
    Doodle = request.form.get("Doodle")
    # if isinstance(Doodle, int) == False:
    #   raise ValueError("Number missing!")
    drink = request.form.get("drink")
    proc_fins.compute("AAA.png", "BBB.png", "final_new.png",
                      str(Doodle), drink)
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'final_new.png')
    AAA = os.path.join(app.config['UPLOAD_FOLDER'], 'AAA.png')
    BBB = os.path.join(app.config['UPLOAD_FOLDER'], 'BBB.png')
    return render_template("gallery.html", remix=remix, dood_num=Doodle)
    # return render_template("result.html",
    #                        user_image=full_filename,
    #                        AAA_image=AAA,
    #                        BBB_image=BBB,
    #                        dood_num=str(Doodle).zfill(4))



app.run(host='0.0.0.0', port=8080)
