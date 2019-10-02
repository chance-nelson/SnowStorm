from api import create_app
from flask_cors import CORS


app = create_app()
CORS(app)
app.run(host='localhost', port=5000, threaded=True)
