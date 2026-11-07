from flask import Flask, render_template, request
from parser import parse_log_line
from detector import detect_brute_force

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_log():
    uploaded_file = request.files["log_file"]

    if uploaded_file.filename == "":
        return "No file selected", 400

    if not uploaded_file.filename.lower().endswith((".log", ".txt")):
        return "Invalid file type", 400

    events = []

    for line_number, line in enumerate(uploaded_file.stream, start=1):
        try:
            decoded_line = line.decode("utf-8")

            if not decoded_line.strip():
                continue
        
            event = parse_log_line(decoded_line)
            events.append(event)
        
        except (ValueError, UnicodeDecodeError) as error:
            return f"Invalid log entry on line {line_number}: {error}", 400

    if not events:
        return "The uploaded log file contains no events", 400
    
    alerts = detect_brute_force(events)

    return render_template("results.html", events=events, alerts=alerts)

if __name__ == "__main__":
    app.run(debug=True)