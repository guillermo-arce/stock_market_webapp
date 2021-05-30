# Run a test server.
from app import app
app.run(host='0.0.0.0',port=7000, debug=app.config['DEBUG'])