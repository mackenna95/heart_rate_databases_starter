from pymodm import connect
import models
import datetime
connect("mongodb://localhost:27017/heart_rate_app")  # open up connection to db


def get_info(email):
    """
    Gets heart_rate measurements from the user specified by email.
    :param email: str email of the user
    :returns user: class instance indicating existing user data
    """
    # Get the first user where _id=email
    user = models.User.objects.raw({"_id": email}).first()
    return user


def check_tachycardia(heart_rate_avg, age):
    """
    Checks if heart rate is Tachycardic
    :param heart_rate_avg: average heart rate
    :param age: user age
    :returns tachycardia: Bool indicating tachycardia
    """
    if age <= 2/365:
        if heart_rate_avg > 159:
            tachycardia = True
        else:
            tachycardia = False
    elif age <= 6/365:
        if heart_rate_avg > 166:
            tachycardia = True
        else:
            tachycardia = False
    elif age <= 3/52:
        if heart_rate_avg > 182:
            tachycardia = True
        else:
            tachycardia = False
    elif age <= 2/12:
        if heart_rate_avg > 179:
            tachycardia = True
        else:
            tachycardia = False
    elif age <= 5/12:
        if heart_rate_avg > 186:
            tachycardia = True
        else:
            tachycardia = False
    elif age <= 11/12:
        if heart_rate_avg > 169:
            tachycardia = True
        else:
            tachycardia = False
    elif age <= 2:
        if heart_rate_avg > 151:
            tachycardia = True
        else:
            tachycardia = False
    elif age <= 4:
        if heart_rate_avg > 137:
            tachycardia = True
        else:
            tachycardia = False
    elif age <= 7:
        if heart_rate_avg > 133:
            tachycardia = True
        else:
            tachycardia = False
    elif age <= 11:
        if heart_rate_avg > 130:
            tachycardia = True
        else:
            tachycardia = False
    elif age <= 15:
        if heart_rate_avg > 119:
            tachycardia = True
        else:
            tachycardia = False
    else:
        if heart_rate_avg > 100:
            tachycardia = True
        else:
            tachycardia = False

    return tachycardia


def add_heart_rate(email, heart_rate, time):
    """
    Appends a heart_rate measurement at a specified time to the user specified
    by email. It is assumed that the user specified by email exists already.
    :param email: str email of the user
    :param heart_rate: number heart_rate measurement of the user
    :param time: the datetime of the heart_rate measurement
    """
    # Get the first user where _id=email
    user = models.User.objects.raw({"_id": email}).first()
    # Append the heart_rate to the user's list of heart rates
    user.heart_rate.append(heart_rate)
    # append the current time to the user's list of heart rate times
    user.heart_rate_times.append(time)
    user.save()  # save the user to the database


def create_user(email, age, heart_rate, time):
    """
    Creates a user with the specified email and age. If the user already
    exists in the DB this WILL overwrite that user. It also adds the
    specified heart_rate to the user
    :param email: str email of the new user
    :param age: number age of the new user
    :param heart_rate: number initial heart_rate of this new user
    :param time: datetime of the initial heart rate measurement
    """
    u = models.User(email, age, [], [])  # create a new User instance
    u.heart_rate.append(heart_rate)  # add initial heart rate
    u.heart_rate_times.append(time)  # add initial heart rate time
    u.save()  # save the user to the database


def print_user(email):
    """
    Prints the user with the specified email
    :param email: str email of the user of interest
    :return:
    """
    # Get the first user where _id=email
    user = models.User.objects.raw({"_id": email}).first()
    print(user.email)
    print(user.heart_rate)
    print(user.heart_rate_times)
    return user

if __name__ == "__main__":
    # we should only do this once, otherwise will overwrite existing user
    create_user(email="suyash@suyashkumar.com", age=24, heart_rate=60,
                time=datetime.datetime.now())
    add_heart_rate("suyash@suyashkumar.com", 60, datetime.datetime.now())
    print_user("suyash@suyashkumar.com")
