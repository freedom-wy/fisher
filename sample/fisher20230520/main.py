from apps import create_app

app = create_app()
print(app.config.get("HELLOWORLD"))


@app.route("/hello")
def index():
    return "hello world"


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80, debug=app.config.get("DEBUG"))
