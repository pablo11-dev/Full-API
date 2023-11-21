import csv
from flask import Flask, request    
import os
import random
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
arquivo_csv = "tarefas.csv"


def gerar_csv():
  if not os.path.exists(arquivo_csv):
    with open(arquivo_csv, mode="w", newline="") as file:
      writer = csv.writer(file)
      writer.writerow(["ID", "Tarefa", "Status"])


def escrever_csv(tarefaList):
  with open(arquivo_csv, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["ID", "Tarefa", "Status"])
    for tarefa in tarefaList:
      writer.writerow([tarefa["ID"], tarefa["Tarefa"], tarefa["Status"]])


def ler_csv():
  with open(arquivo_csv, mode="r", newline="") as file:
    reader = csv.reader(file)
    next(reader)
    tarefaList = []
    for row in reader:
      if len(row) >= 3:
        tarefaList.append({
            "ID": int(row[0]),
            "Tarefa": row[1],
            "Status": row[2]
        })
  return tarefaList


gerar_csv()

tarefaList = ler_csv()


@app.route("/", methods=["GET"])
def index():
  tarefas = ler_csv()
  tarefas_visiveis = [
      tarefa for tarefa in tarefas if tarefa["Status"] != "Deletada"
  ]
  return tarefas_visiveis


@app.route("/task", methods=["POST"])
def add_task():
  item = request.json
  if "Tarefa" not in item:
    return {
        "error":
        "A chave 'Tarefa' é necessária para adicionar uma nova tarefa."
    }, 400
  item["ID"] = random.randint(1000, 9999)
  item["Status"] = "Ativo"
  tarefaList.append(item)
  escrever_csv(tarefaList)
  return item


@app.route("/task/<int:task_id>", methods=["PUT"])
def update_task(task_id):
  item = request.json
  for tarefa in tarefaList:
    if tarefa["ID"] == task_id:
      if "Tarefa" in item:
        tarefa["Tarefa"] = item["Tarefa"]
  escrever_csv(tarefaList)
  return tarefaList


@app.route("/delete_task/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
  for tarefa in tarefaList:
    if tarefa["ID"] == task_id:
      tarefa["Status"] = "Deletada"
  escrever_csv(tarefaList)
  return tarefaList


if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)