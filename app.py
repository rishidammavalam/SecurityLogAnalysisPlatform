from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_log():
    uploaded_file = request.files["log_file"]

    return f"Uploaded file: {uploaded_file.filename}"

if __name__ == "__main__":
    app.run(debug=True)