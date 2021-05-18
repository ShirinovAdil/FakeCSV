from schemas.models import ColumnModel, ColumnTypeChoices

from datetime import timedelta, datetime
import random
import json


def random_date(start, end):
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = random.randrange(int_delta)
    return str(start + timedelta(seconds=random_second))


def generate_int_data(column):
    """
    Random integer between two numbers
    """
    return str(random.randint(column.quantity_range_lower, column.quantity_range_upper))


def generate_date_data():
    """
    Random date in the range
    """
    return random_date(
        datetime.strptime("1/1/2020 4:50 AM", "%m/%d/%Y %I:%M %p"),
        datetime.strptime("1/1/2021 4:50 AM", "%m/%d/%Y %I:%M %p"),
    )


def generate_job_data():
    """
    Random job from the json file
    """
    with open("schemas/utils/occupations.json") as f:
        data = json.load(f)
    job_titles = data.get("occupations")
    return random.choices(job_titles)[0]


def generate_email_data():
    """
    Random mail from the json file
    """
    with open("schemas/utils/emails.json") as f:
        data = json.load(f)
    email_providers = data.get("emails")
    return random.choices(email_providers)[0]


def get_country_code():
    """Random country code"""
    with open("schemas/utils/codes.json") as f:
        data = json.load(f)
    country_code = data.get("codes")
    return random.choices(country_code)[0]["dial_code"]


def generate_phone_data():
    """
    Random phone number
    """
    return get_country_code() + "".join(
        str(random.randint(0, 9)) for x in range(random.randint(5, 9))
    )


def generate_csv_data(column_id):
    """
    Function detecting the passed column type and returning proper data
    """
    column = ColumnModel.objects.get(id=column_id)

    if column.type == ColumnTypeChoices.INT:
        return generate_int_data(column)
    elif column.type == ColumnTypeChoices.DATE:
        return generate_date_data()
    elif column.type == ColumnTypeChoices.JOB:
        return generate_job_data()
    elif column.type == ColumnTypeChoices.EMAIL:
        return generate_email_data()
    elif column.type == ColumnTypeChoices.PHONE:
        return generate_phone_data()
    else:
        return "Unsupported data type"
