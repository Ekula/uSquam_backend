from flask import Flask
from usquam.resources.register import api_bp

app = Flask(__name__)
app.register_blueprint(api_bp)

if __name__=="__main__":
    app.run(debug=True)