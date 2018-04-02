from flask import Flask, jsonify, request
import math
from main import get_info, add_heart_rate, create_user, print_user
from main import check_tachycardia
from flask_cors import CORS
import datetime
import numpy
from dateutil.parser import parse
app = Flask(__name__)
CORS(app)


@app.route("/api/heart_rate", methods=["POST"])
def heart_rate():
    """
    Adds heart rate to dictionary related to user email
    Creates new user if user does not exist
    :param email: str email of the new user
    :param age: number age of the new user
    :param heart_rate: number initial heart_rate of this new user
    :returns message: json indicating either
    job complete, KeyError, TypeError
    """

    r = request.get_json()  # parses the POST request body as JSON

    import logging
    logging.basicConfig(filename="server_log.txt",
                        format='%(asctime)s %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p')

    try:
        if not isinstance(r['user_email'], str):
            logging.debug('TypeError: user_email is not a string')
            message = {
                "TypeError": "User_email is not a string",
            }
            return jsonify(message), 400
    except KeyError:
        logging.debug('KeyError: incorrect user_email key')
        message = {
            "KeyError": "Incorrect user_email key",
        }
        return jsonify(message), 400
    try:
        if not isinstance(r['user_age'], int):
            logging.debug('TypeError: user_age is not an int')
            message = {
                "TypeError": "User_age is not an int",
            }
            return jsonify(message), 400
    except KeyError:
        logging.debug('KeyError: incorrect user_age key')
        message = {
            "KeyError": "Incorrect user_age key",
        }
        return jsonify(message), 400
    try:
        if isinstance(r['heart_rate'], int):
            a = 1
        elif isinstance(r['heart_rate'], float):
            a = 1
        else:
            logging.debug('TypeError: Heart_rate is not an int/float')
            message = {
                "TypeError": "Heart_rate is not an int or float",
            }
            return jsonify(message), 400
    except KeyError:
        logging.debug('KeyError: incorrect heart_rate key')
        message = {
            "KeyError": "Incorrect heart_rate key",
        }
        return jsonify(message), 400

    try:
        add_heart_rate(r['user_email'], r['heart_rate'],
                       datetime.datetime.now())
    except Exception:
        logging.debug('ExceptionError: new user will be created')
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
    :returns user_info_return: json with
    user_email, heart_rate, date_time
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
    :returns user_info_return: json with
    user_email, average_heart_rate, date_time_span
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
def intervalAverage():
    """
    Returns the average heart rate over a specified time for
    specified user as JSON
    :param email: str email of the new user
    :returns user_info_return: json with
    user_email, heart_rate_average_times, average_heart_rate,
    Tachycardia
    """
    import logging
    logging.basicConfig(filename="server_log.txt",
                        format='%(asctime)s %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p')

    r = request.get_json()  # parses the POST request body as JSON

    try:
        user_time = parse(r['heart_rate_average_since'])
    except ValueError:
        logging.debug('Incorrect data format, YYYY-MM-DD HH.MM.SS.')
        message = {
            "ValueError": "Incorrect data format, YYYY-MM-DD HH.MM.SS.",
        }
        return jsonify(message), 400
    except KeyError:
        logging.debug('KeyError: incorrect heart_rate_average_since key')
        message = {
            "KeyError": "Incorrect heart_rate_average_since key",
        }
        return jsonify(message), 400

    try:
        user_info = get_info(r['user_email'])
    except Exception:
        logging.debug('Error: Ueser does not exist')
        # raise Exception("Error: User does not exist")
        message = {
            "Error": "User does not exist",
        }
        return jsonify(message), 400

    enum = user_info.heart_rate_times
    inds = [i for i, x in enumerate(enum) if x >= user_time]
    heart_rate_avg = numpy.average([user_info.heart_rate[i] for i in inds])
    average_heart_rate_times = [user_info.heart_rate_times[i] for i in inds]

    tachycardia = check_tachycardia(heart_rate_avg, user_info.age)

    user_info_return = {
        "user_email": user_info.email,
        "heart_rate_average_times": average_heart_rate_times,
        "average_heart_rate": heart_rate_avg,
        "Tachycardia": tachycardia,
    }
    return jsonify(user_info_return), 200
