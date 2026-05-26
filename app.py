import csv
import io
import os
from datetime import datetime

from flask import Flask, jsonify, render_template, send_file

app = Flask(__name__)

DADOS = [
    {"id": "QW12E", "categoria": "New Panamax", "entrada": "0", "saida": "0", "dock": "A1", "data": "2024-09-15"},
    {"id": "RT56Y", "categoria": "Ultra Large Container Ship", "entrada": "0", "saida": "0", "dock": "A2", "data": "2024-07-22"},
    {"id": "YU78H", "categoria": "Post-Panamax", "entrada": "0", "saida": "0", "dock": "A3", "data": "2024-06-30"},
    {"id": "DF34G", "categoria": "Container Ship", "entrada": "0", "saida": "0", "dock": "A4", "data": "2024-05-10"},
    {"id": "GH89J", "categoria": "Feeder Ship", "entrada": "0", "saida": "0", "dock": "A1", "data": "2024-04-20"},
    {"id": "JK12M", "categoria": "General Cargo Ship", "entrada": "0", "saida": "0", "dock": "A2", "data": "2024-03-05"},
    {"id": "LP34N", "categoria": "Bulk Carrier", "entrada": "0", "saida": "0", "dock": "A3", "data": "2024-02-14"},
    {"id": "ZX56O", "categoria": "Roll-on/Roll-off", "entrada": "0", "saida": "0", "dock": "A4", "data": "2024-01-01"},
]


@app.route("/")
def index():
    return render_template("index.html", video={"title": "CAM-01", "url": "vxqQyW4b9jA"}, planilha=DADOS)


@app.route("/api", methods=["GET"])
def get_api_welcome():
    return render_template("api.html")


@app.route("/api/guia")
def guia():
    return render_template("guia.html")


@app.route("/webhook")
def webhook():
    return render_template("webhook.html")


@app.route("/download_csv")
def download_csv():
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=["id", "categoria", "entrada", "saida", "dock", "data"])
    writer.writeheader()
    writer.writerows(DADOS)

    csv_bytes = output.getvalue().encode("utf-8")
    output.close()

    data_primeira = datetime.strptime(DADOS[0]["data"], "%Y-%m-%d").strftime("%Y%m%d")
    nome_arquivo = f"suape_vision_{data_primeira}.csv"

    return send_file(
        io.BytesIO(csv_bytes),
        mimetype="text/csv",
        as_attachment=True,
        download_name=nome_arquivo,
    )


@app.route("/api/dados", methods=["GET"])
@app.route("/api/dados/id/<id>", methods=["GET"])
@app.route("/api/dados/data/<data>", methods=["GET"])
@app.route("/api/dados/id/<id>/data/<data>", methods=["GET"])
def get_dados(id=None, data=None):
    filtrados = DADOS
    if id:
        filtrados = [item for item in filtrados if item["id"] == id]
    if data:
        filtrados = [item for item in filtrados if item["data"] == data]

    if not filtrados:
        return jsonify({"erro": "Nenhum registro encontrado."}), 404
    return jsonify(filtrados)


if __name__ == "__main__":
    app.run(debug=os.getenv("FLASK_DEBUG", "false").lower() == "true")
