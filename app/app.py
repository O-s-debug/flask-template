from flask import Flask
from routers import router
from flask_wtf import CSRFProtect

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Use .env in production

app.register_blueprint(router)
csrf = CSRFProtect(app)

if __name__ == '__main__':
    app.run(debug=True)
