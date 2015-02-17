from flask import Flask
from flask import render_template, send_from_directory
import os

app = Flask(__name__, static_url_path='', static_folder='static')

@app.route('/')
def index():
	return send_from_directory(os.path.join(app.root_path, 'static'), 'index.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False)
