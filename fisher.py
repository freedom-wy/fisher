from app import create_app


app = create_app()

print(app.url_map)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)
