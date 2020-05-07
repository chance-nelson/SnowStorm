from api import create_app


app = create_app()
app.run(host='localhost', port=5000, threaded=True)
