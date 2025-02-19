# backend/run.py

from app import create_app
from flask_cors import CORS
<<<<<<< HEAD
=======

>>>>>>> 4d38979407c86dd5c5488f5b512c547176bade78
app = create_app()
CORS(app)

if __name__ == "__main__":
    app.run(debug=True)
