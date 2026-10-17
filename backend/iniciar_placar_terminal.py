from .partida import Partida
from .atleta import Atleta
import questionary

# Transforma duração mm:ss em segundo
def transforma_duracao(tempo : str):
  min, seg = tempo.split(':')
  return int(seg) + (int(min) * 60)

# Main
def main():
  aka = Atleta("Aka")
  ao = Atleta("Ao")

  duracao = questionary.select(
    "Qual será a duração da partida?",
    choices=[
      "1:00",
      "1:30",
      "2:00",
      "3:00",
      "Personalizado"
    ]
  ).ask()

  if duracao == None:
    return
  elif duracao == "Personalizado":
    while True:
      try:
        tempo = int(input("\nQual será a duração em segundos? "))
      except:
        print("Opção inválida! Digite um número")
        continue
      break
  else: 
    tempo = transforma_duracao(duracao)

  print()

  opcoes_orientacao = ["Aka (esquerda) - Ao (direita)", "Ao (esquerda) - Aka (direita)"]

  orientacao = questionary.select(
    "Qual será a orentação da partida?",
    choices=opcoes_orientacao
  ).ask()

  if orientacao == None:
    return
  
  num_orientacao = opcoes_orientacao.index(orientacao)

  partida = Partida(aka, ao, tempo, num_orientacao)
  partida.iniciar()

if __name__ == '__main__':
  main()
