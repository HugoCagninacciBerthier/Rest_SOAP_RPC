from csv import DictReader
from flask import Flask, jsonify

# Read the index-egalite-fh.csv file and store it in a dictionary
egapro_data = {}

with open("index-egalite-fh-utf8.csv", encoding="utf-8") as csv_file:
    reader = DictReader(csv_file, delimiter=";", quotechar='"')
    for row in reader:
        if egapro_data.get(row["SIREN"]) is None:
            egapro_data[row["SIREN"]] = row
        elif egapro_data[row["SIREN"]]["Année"] < row["Année"]: # Va chercher l'année la plus récente si plusieurs résultats
            egapro_data[row["SIREN"]].update(row)

application = Flask(__name__)

@application.route("/siren/<siren>")
def siren(siren: str):  # Le siren doit être un string
    """
    Retourne les données égapro pour le siren demandé.
    """
    response = egapro_data.get(siren)  # Va chercher le siren

    if response is None:
        response = {"error": "SIREN not found"}
        status = 404
    else:
        status = 200
    return jsonify(response), status

# Un debug pour flask
if __name__ == "__main__":
    application.run(debug=True)
