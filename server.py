from flask import Flask, jsonify, request
import math
app = Flask(__name__)

@app.route("/api/heart_rate", methods=["POST"])
def sum():
  # """
  # Returns sum of a and b to the caller
  # """
  r = request.get_json() # parses the POST request body as JSON
  s = r["a"][0] + r["b"][0] # adds JSON dict parameter "a" and "b" together
  return jsonify(s), 200

@app.route("/api/heart_rate/<user_email>", methods=["GET"])
def allHeartRate(user_email):
  """
  Returns the hello_name dictionary below to the caller as JSON
  """
  message = []
  message.append("Hello there ")
  message.append(name)
  message = ''.join(message)
  hello_name = {
    "message": message,
  }
  return jsonify(hello_name), 200
  
@app.route("/api/heart_rate/average/<user_email>", methods=["GET"])
def averageHeartRate(user_email):
  """
  Returns the hello_name dictionary below to the caller as JSON
  """
  message = []
  message.append("Hello there ")
  message.append(name)
  message = ''.join(message)
  hello_name = {
    "message": message,
  }
  return jsonify(hello_name), 200
  
@app.route("/api/heart_rate/interval_average", methods=["POST"])
def distance():
  """
  Returns distance between a and b to the caller as JSON
  """
  r = request.get_json() # parses the POST request body as JSON
  dist = math.sqrt((r["a"][0]-r["b"][0])*(r["a"][0]-r["b"][0])+(r["a"][1]-r["b"][1])*(r["a"][1]-r["b"][1]))
  dist_return = {
    "distance": dist,
    "a": r["a"],
    "b": r["b"]
  }
  return jsonify(dist_return), 200
