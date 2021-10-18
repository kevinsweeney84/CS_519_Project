import os

from dotenv import load_dotenv
load_dotenv()


def getenv(variable):
    """
    Method retrieves the desired variable from the .env file
    :param variable:
    :return:
    """

    return os.getenv(variable)
