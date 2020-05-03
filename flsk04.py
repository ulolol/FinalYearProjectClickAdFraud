from flask import Flask, request, render_template
import map00
import subprocess
from werkzeug.utils import secure_filename
app = Flask(__name__)

f = None



@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


@app.route('/')
def my_form():
    return render_template('newmain.html')


@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      f.save(secure_filename(f.filename))
      return 'file uploaded successfully'


@app.route('/', methods=['GET','POST'])
def my_form_post():
    if request.method == 'POST':
      f = request.files['file']
      f.save(secure_filename(f.filename))
    #cmds = 'python3 finalmodel.py -i ' + f.filename
    subprocess.call(["python3", "finalmodel.py", "-i", f.filename])
    map00.main()
    return render_template('/newfront/main.html')


    #processed_text = text.upper()
    #return processed_text



@app.route("/legit")
def legitpage():
    return render_template('/legit/legit.html')


if __name__ == '__main__': 
  
    # run() method of Flask class runs the application  
    # on the local development server. 
    app.run() 
 
