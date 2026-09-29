from atleta import Atleta
import time
from pynput import keyboard
import questionary
from tabulate import tabulate
from rich.table import Table
from rich.console import Console

console = Console()

class Partida:

  # Construtor
  def __init__(self, aka : Atleta, ao : Atleta, duracao : int, orientacao : str):
    self.aka = aka  
    self.ao = ao
    self.duracao = duracao
    self.hajime = False
    self.terminada = False  
    self.vencedor = None
    self.orientacao = orientacao

    self.listener = keyboard.Listener(on_press=self.on_press)
    self.listener.start()

    self.iniciar_placar_terminal()

  # Pontuar - Dá senshu e acaba se a diferença for de 8 pontos
  def ganhar_ponto(self, alvo : Atleta, outro : Atleta, pontos : int = 1):

    # Senshu
    if alvo.pontos == 0 and outro.pontos == 0 and alvo.senshu == False and outro.senshu == False:
      self.modificar_senshu(alvo, outro)
    
    alvo.pontuar(pontos)

    # Diferença de 8 pontos
    if alvo.pontos - outro.pontos >= 8:
      self.terminada = True
      self.vencedor = alvo

  # Remover pontos
  def remove_ponto(self, alvo : Atleta, pontos : int = 1):
    alvo.remove_ponto(pontos)

  # Penalidade
  def penalidade(self, alvo : Atleta, outro : Atleta):
    alvo.penalidade()

    # Máximo de 5
    if alvo.penalidades >= 5:
      self.vencedor = outro
      self.terminada = True

  # Modifica o valor do senshu. Garante que somente um atleta o possui
  def modificar_senshu(self, alvo : Atleta, outro : Atleta):
    if alvo.senshu:
      alvo.set_senshu(False)
      return
    elif outro.senshu:
      outro.set_senshu(False)
    alvo.set_senshu(True)

  # Analisa quem ganhou
  def procura_vencedor(self):
    if self.aka.penalidades >= 5:
      self.vencedor = self.ao
    elif self.ao.penalidades >= 5:
      self.vencedor = self.aka
    elif self.aka.pontos > self.ao.pontos:
      self.vencedor = self.aka
    elif self.ao.pontos > self.aka.pontos:
      self.vencedor = self.ao
    elif self.aka.senshu:
      self.vencedor = self.aka
    elif self.ao.senshu:
      self.vencedor = self.ao
    else:
      self.vencedor = Atleta("Empate")

    self.terminada = True
    return self.vencedor
    
  # Mostra os valores de aka e ao
  def valores(self):
    aka = self.aka
    ao = self.ao

    tabela = Table()
    tabela.add_column(f"[bold red]Aka[/]", width=20, justify="center")
    tabela.add_column(f"[bold blue]Ao[/]", width=20, justify="center")

    tabela.add_row(
      str(aka.pontos), str(ao.pontos)
    )

    tabela.add_row(
      "|" if aka.senshu else "", "|" if ao.senshu else ""
    )

    tabela.add_row(
      f'{"x" * aka.penalidades}', f'{"x" * ao.penalidades}'
    )

    return tabela

  # Detecta espaço
  def on_press(self, key):
    if key == keyboard.Key.space:
      self.hajime = not self.hajime
    elif key == keyboard.Key.esc:
      self.terminada = True

  # Atualiza placar enquanto está em hajime
  def placar_hajime(self):
    while self.duracao > 0 and self.terminada == False and self.hajime:
      print("\033[H\033[J", end="")

      mins, segs = divmod(self.duracao, 60)
      tempo_formatado = f'{mins:02d}:{segs:02d}'
      
      console.print(
        f"[bold]{tempo_formatado}[/]",
        justify="center",
        width=40
      )
      console.print(self.valores())
      self.duracao -= 1
      time.sleep(1)

  # Placar quando está em yame
  def placar_yame(self, pergunta=True):
    print("\033[H\033[J", end="")
    
    mins, segs = divmod(self.duracao, 60)
    tempo_formatado = f'{mins:02d}:{segs:02d}'

    console.print(
      f"[bold]{tempo_formatado}[/]",
      justify="center",
      width=40
    )

    console.print(self.valores())

    if pergunta:
      self.perguntar()

  # Perguntas em yame
  def perguntar(self):
    akao = ["Aka", "Ao"]
    opcao = questionary.select(
      "O que deseja fazer?",
      choices=[
        "Continuar",
        "Pontuar",
        "Penalizar",
        "Remover Ponto",
        "Senshu",
        "Encerrar"
      ]
    ).ask()

    if opcao == "Encerrar" or opcao == None:
      self.terminada = True

    elif opcao == "Continuar":
      self.hajime = True

    elif opcao == "Pontuar":
      opcao = questionary.select(
        "Quem deve pontuar?",
        choices=akao
      ).ask()
      if opcao == None:
        self.placar_yame()
      elif opcao == "Aka":
        self.ganhar_ponto(self.aka, self.ao)
      else:
        self.ganhar_ponto(self.ao, self.aka)

    elif opcao == "Penalizar":
      opcao = questionary.select(
        "Quem deve ser penalizado?",
        choices=akao
      ).ask()

      if opcao == None:
        self.placar_yame()
      elif opcao == "Aka":
        self.penalidade(self.aka, self.ao)
      else:
        self.penalidade(self.ao, self.aka)

    elif opcao == "Remover Ponto":
      opcao = questionary.select(
        "Quem vai perder o ponto?",
        choices=akao
      ).ask()

      if opcao == None:
        self.placar_yame()
      elif opcao == "Aka":
        self.remove_ponto(self.aka)
      else:
        self.remove_ponto(self.ao)

    elif opcao == "Senshu":
      opcao = questionary.select(
        "Quem vai ter seu senshu modificado?",
        choices=akao
      ).ask()

      if opcao == None:
        self.placar_yame()
      elif opcao == "Aka":
        self.modificar_senshu(self.aka, self.ao)
      else:
        self.modificar_senshu(self.ao, self.aka)

  # Inicia placar
  def iniciar_placar_terminal(self):

    while self.duracao > 0 and self.terminada == False:
      self.placar_yame()
      if self.hajime:
        self.placar_hajime()

    self.placar_yame(pergunta=False) 
    vencedor = self.procura_vencedor()
    print(f'O vencedor é {vencedor.cor}')
    self.listener.stop()
