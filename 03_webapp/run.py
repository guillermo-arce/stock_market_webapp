# Run a test server.
from app import app
app.run(host='localhost',port=7000, debug=app.config['DEBUG'])