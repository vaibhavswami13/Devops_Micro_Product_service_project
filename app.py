from flask import Flask
import socket

app = Flask(__name__)

@app.route("/")
def home():
    return "DevOps product-service app running on eks pod, you did freat Vaibhav, 3  days work paid off"

@app.route("/health")
def health():
    return {
        "status": "healthy",
        "hostname": socket.gethostname()
    }

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
