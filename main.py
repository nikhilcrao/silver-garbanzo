import finapp

app = finapp.create_app()
app.run(host='0.0.0.0', port=81, debug=False)
