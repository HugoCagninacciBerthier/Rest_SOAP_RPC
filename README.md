"""
This module is a Flask app that serves the EgaPro data via a JSON API.
It reads the data from a CSV file and serves it as a JSON object.
"""

from csv import DictReader
from flask import Flask, jsonify

# Read the index-egalite-fh.csv file and store it in a dictionary
egapro_data = {}

with open("index-egalite-fh-utf8.csv", encoding="utf-8") as csv_file:
    reader = DictReader(csv_file, delimiter=";", quotechar='"')
    for row in reader:
        if egapro_data.get(row["SIREN"]) is None:
            egapro_data[row["SIREN"]] = row
        elif egapro_data[row["SIREN"]]["Année"] < row["Année"]:
            egapro_data[row["SIREN"]].update(row)

application = Flask(__name__)

# Define the SIREN route taking a SIREN as a parameter and returning the
# corresponding data from the egapro_data dictionary
@application.route("/siren/<siren>")
def siren(siren: str):  # Correction ici : siren doit être un str
    """
    Return the EgaPro data for a given SIREN number.
    A 404 is returned if the SIREN is not found.

    :param siren: SIREN number as a string
    :return: The corresponding data as JSON
    """
    response = egapro_data.get(siren)  # Les clés du dict sont des strings

    if response is None:
        response = {"error": "SIREN not found"}
        status = 404
    else:
        status = 200
    return jsonify(response), status

# A debug Flask launcher
if __name__ == "__main__":
    application.run(debug=True)
