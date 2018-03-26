from flask import Flask, jsonify, request
import math
from main import get_info, add_heart_rate, create_user, print_user
import datetime
app = Flask(__name__)


@app.route("/api/heart_rate", methods=["POST"])
def heart_rate():
    # """
    # Returns sum of a and b to the caller
    # """

    r = request.get_json()  # parses the POST request body as JSON

    import logging
    logging.basicConfig(filename="server_log.txt",
                        format='%(asctime)s %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p')

    try:
        if not isinstance(r['user_email'], str):
            raise TypeError("TypeError: user_email is not a sting")
            return 400
    except KeyError:
        logging.debug('KeyError: incorrect user_email key')
        raise KeyError("KeyError: incorrect user_email key")
        return 400
    try:
        if not isinstance(r['user_age'], int):
            raise TypeError("TypeError: user_age is not a sting")
            return 400
    except KeyError:
        logging.debug('KeyError: incorrect user_age key')
        raise KeyError("KeyError: incorrect user_age key")
        return 400
    try:
        if isinstance(r['heart_rate'], int):
            a=1
        elif isinstance(r['heart_rate'], float):
            a=1
        else:
            raise TypeError("TypeError: heart_rate is not a sting")
            return 400
    except KeyError:
        logging.debug('KeyError: incorrect heart_rate key')
        raise KeyError("KeyError: incorrect heart_rate key")
        return 400

    try:
        add_heart_rate(r['user_email'], r['heart_rate'], datetime.datetime.now())
    except Exception:
        create_user(r['user_email'], r['user_age'], r['heart_rate'], datetime.datetime.now())

    message = {
        "message": "Post Completed",
    }
    return jsonify(message), 200
    
@app.route("/api/heart_rate2", methods=["POST"])
def heart_rate2():
    # """
    # Returns sum of a and b to the caller
    # """

    r = request.get_json()  # parses the POST request body as JSON
    message = {
        "message": r['user_email'],
    }
    return jsonify(message), 200


@app.route("/api/heart_rate/<user_email>", methods=["GET"])
def allHeartRate(user_email):
    """
    Returns the hello_name dictionary below to the caller as JSON
    """
    message = []
    message.append("Hello there ")
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
    r = request.get_json()  # parses the POST request body as JSON
    dist = math.sqrt((r["a"][0]-r["b"][0])*(r["a"][0]-r["b"][0]))
    dist_return = {
        "distance": dist,
        "a": r["a"],
        "b": r["b"]
    }
    return jsonify(dist_return), 200
