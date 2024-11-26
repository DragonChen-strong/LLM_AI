from model import app
from model.config import config

if __name__ == "__main__":
    app.run(debug=config.FLASK_ENV == "development", host="0.0.0.0", port=config.API_PORT)
