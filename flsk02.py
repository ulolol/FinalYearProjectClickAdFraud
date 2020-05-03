from flask import Flask, request, render_template
import ttt00
app = Flask(__name__)

@app.route('/')
def my_form():
    return render_template('myf.html')

@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form['text']
    text = str(text)
    res = ttt00.ipaddr(text)
    return res


    #processed_text = text.upper()
    #return processed_text

if __name__ == '__main__': 
  
    # run() method of Flask class runs the application  
    # on the local development server. 
    app.run() 
