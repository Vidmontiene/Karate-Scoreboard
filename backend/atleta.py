class Atleta:

  # Construtor
  def __init__(self, cor : str):
    self.cor = cor
    self.pontos = 0
    self.senshu = False
    self.penalidades = 0

  # Aumenta pontos
  def pontuar(self, pontos : int = 1):
    self.pontos += pontos

  # Set senshu
  def set_senshu(self, valor : bool):
    self.senshu = valor

  # Remove ponto
  def remove_ponto(self, pontos : int = 1):
    if self.pontos - pontos < 0:
      self.pontos = 0
    else:
      self.pontos -= pontos

  # Penalidade
  def penalidade(self):
    self.penalidades += 1

  # toString
  def __str__(self):
    return f"{self.cor}: {self.pontos} pontos e {self.penalidades} faltas"

