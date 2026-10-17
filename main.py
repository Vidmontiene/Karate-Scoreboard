import webview
from backend.partida import Partida
from backend.atleta import Atleta

# Constantes
ESQ = 0
DIR = 1

class API:

  # Construtor
  def __init__(self, partida : Partida):
    self.partida = partida

  # Retorna o dicionário do placar
  def obter_placar(self):
    partida = self.partida

    info = {
      "duracao": partida.duracao,
      "orientacao": partida.orientacao
    }

    esq = {
      "pontos": partida.esq.pontos,
      "senshu": partida.esq.senshu,
      "penalidades": partida.esq.penalidades
    }

    dir = {
      "pontos": partida.dir.pontos,
      "senshu": partida.dir.senshu,
      "penalidades": partida.dir.penalidades
    }

    info["esq"] = esq
    info["dir"] = dir

    return info

  # Pontua
  def pontua(self, alvo : int):
    partida = self.partida
    esq = partida.esq
    dir = partida.dir

    if alvo == ESQ:
      partida.ganhar_ponto(esq, dir)
    else:
      partida.ganhar_ponto(dir, esq)

  # Remove Ponto
  def remove_ponto(self, alvo : int):
    partida = self.partida

    if alvo == ESQ:
      esq = partida.esq
      partida.remove_ponto(esq)
    else:
      dir = partida.dir
      partida.remove_ponto(dir)

  # Modifica senshu
  def modificar_senshu(self, alvo : int):
    partida = self.partida
    esq = partida.esq
    dir = partida.dir

    if alvo == ESQ:
      partida.modificar_senshu(esq, dir)
    else:
      partida.modificar_senshu(dir, esq)

  # Penaliza
  def penaliza(self, alvo : int):
    partida = self.partida
    esq = partida.esq
    dir = partida.dir

    if alvo == ESQ:
      partida.penalidade(esq, dir)
    else:
      partida.penalidade(dir, esq)

  # Remove penalidade
  def remove_penalidade(self, alvo : int):
    partida = self.partida

    if alvo == ESQ:
      esq = partida.esq
      partida.remove_penalidade(esq)
    else:
      dir = partida.dir
      partida.remove_penalidade(dir)

aka = Atleta("Aka")
ao = Atleta("Ao")
partida = Partida(aka, ao, 60, 0)
api = API(partida)

window = webview.create_window(
  "Karate Scoreboard",
  "frontend/index.html",
  js_api=api,
)

webview.start(debug=True)