from flask import Flask, jsonify, request
import math
from main import get_info, add_heart_rate, create_user, print_user
import datetime
import numpy
app = Flask(__name__)


@app.route("/api/heart_rate", methods=["POST"])
def heart_rate():
    """
    Adds heart rate to dictionary related to user email
    Creates new user if user does not exist
    :param email: str email of the new user
    :param age: number age of the new user
    :param heart_rate: number initial heart_rate of this new user
    """

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
            a = 1
        elif isinstance(r['heart_rate'], float):
            a = 1
        else:
            raise TypeError("TypeError: heart_rate is not a sting")
            return 400
    except KeyError:
        logging.debug('KeyError: incorrect heart_rate key')
        raise KeyError("KeyError: incorrect heart_rate key")
        return 400

    try:
        add_heart_rate(r['user_email'], r['heart_rate'],
                       datetime.datetime.now())
    except Exception:
        create_user(r['user_email'], r['user_age'],
                    r['heart_rate'], datetime.datetime.now())

    message = {
        "message": "Post Completed",
    }
    return jsonify(message), 200


@app.route("/api/heart_rate/<user_email>", methods=["GET"])
def allHeartRate(user_email):
    """
    Returns the heart rate and times for specified user as JSON
    :param email: str email of the new user
    """
    import logging
    logging.basicConfig(filename="server_log.txt",
                        format='%(asctime)s %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p')

    try:
        user_info = get_info(user_email)
    except Exception:
        logging.debug('Error: Ueser does not exist')
        # raise Exception("Error: User does not exist")
        message = {
            "Error": "User does not exist",
        }
        return jsonify(message), 400

    user_info_return = {
        "user_email": user_info.email,
        "heart_rate": user_info.heart_rate,
        "date_time": user_info.heart_rate_times,
    }
    return jsonify(user_info_return), 200


@app.route("/api/heart_rate/average/<user_email>", methods=["GET"])
def averageHeartRate(user_email):
    """
    Returns the average heart rate and times for specified user as JSON
    :param email: str email of the new user
    """
    import logging
    logging.basicConfig(filename="server_log.txt",
                        format='%(asctime)s %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p')

    try:
        user_info = get_info(user_email)
    except Exception:
        logging.debug('Error: Ueser does not exist')
        # raise Exception("Error: User does not exist")
        message = {
            "Error": "User does not exist",
        }
        return jsonify(message), 400

    ind = len(user_info.heart_rate_times) - 1
    heart_rate_avg = numpy.average(user_info.heart_rate)
    user_info_return = {
        "user_email": user_info.email,
        "average_heart_rate": heart_rate_avg,
        "date_time_span": [user_info.heart_rate_times[0],
                           user_info.heart_rate_times[ind]],
    }
    return jsonify(user_info_return), 200


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
