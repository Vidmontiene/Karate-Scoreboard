from atleta import Atleta
import time
from pynput import keyboard
import questionary
from rich.table import Table
from rich.console import Console

console = Console()

# Constantes para orientação
AKA_ESQ = 0
AKA_DIR = 1

class Partida:

  # Construtor
  def __init__(self, aka : Atleta, ao : Atleta, duracao : int, orientacao : int):

    if orientacao == AKA_ESQ:
      self.esq= aka  
      self.dir = ao
    elif orientacao == AKA_DIR:
      self.esq= ao 
      self.dir = aka

    self.duracao = duracao
    self.hajime = False
    self.terminada = False  
    self.vencedor = None
    self.orientacao = orientacao

    self.listener = keyboard.Listener(on_press=self.on_press)
    self.listener.start()

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
    if self.esq.penalidades >= 5:
      self.vencedor = self.dir
    elif self.dir.penalidades >= 5:
      self.vencedor = self.esq
    elif self.esq.pontos > self.dir.pontos:
      self.vencedor = self.esq
    elif self.dir.pontos > self.esq.pontos:
      self.vencedor = self.dir
    elif self.esq.senshu:
      self.vencedor = self.esq
    elif self.dir.senshu:
      self.vencedor = self.dir
    else:
      self.vencedor = Atleta("Empate")

    self.terminada = True
    return self.vencedor

  # Colore de acordo com o nome do objeto
  def cor_atleta(self, atleta : Atleta):
    if atleta.cor == "Aka":
      return f"[bold red]Aka[/]"
    elif atleta.cor == "Ao":
      return f"[bold blue]Ao[/]"

  # Mostra os valores de aka e ao
  def valores(self):
    esq = self.esq
    dir = self.dir

    tabela = Table()
    tabela.add_column(self.cor_atleta(esq), width=20, justify="center")
    tabela.add_column(self.cor_atleta(dir), width=20, justify="center")

    tabela.add_row(
      str(esq.pontos), str(dir.pontos)
    )

    tabela.add_row(
      "|" if esq.senshu else "", "|" if dir.senshu else ""
    )

    tabela.add_row(
      f'{"x" * esq.penalidades}', f'{"x" * dir.penalidades}'
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
      print("Pressione espaço para dar yame")
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
    if self.orientacao == AKA_ESQ:
      akao = ["Aka", "Ao"]
    elif self.orientacao == AKA_DIR:
      akao = ["Ao", "Aka"]

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
      elif akao.index(opcao) == 0:
        self.ganhar_ponto(self.esq, self.dir)
      else:
        self.ganhar_ponto(self.dir, self.esq)

    elif opcao == "Penalizar":
      opcao = questionary.select(
        "Quem deve ser penalizado?",
        choices=akao
      ).ask()

      if opcao == None:
        self.placar_yame()
      elif akao.index(opcao) == 0:
        self.penalidade(self.esq, self.dir)
      else:
        self.penalidade(self.dir, self.esq)

    elif opcao == "Remover Ponto":
      opcao = questionary.select(
        "Quem vai perder o ponto?",
        choices=akao
      ).ask()

      if opcao == None:
        self.placar_yame()
      elif akao.index(opcao) == 0:
        self.remove_ponto(self.esq)
      else:
        self.remove_ponto(self.dir)

    elif opcao == "Senshu":
      opcao = questionary.select(
        "Quem vai ter seu senshu modificado?",
        choices=akao
      ).ask()

      if opcao == None:
        self.placar_yame()
      elif akao.index(opcao) == 0:
        self.modificar_senshu(self.esq, self.dir)
      else:
        self.modificar_senshu(self.dir, self.esq)

  # Inicia placar no terminal
  def iniciar(self):

    while self.duracao > 0 and self.terminada == False:
      self.placar_yame()
      if self.hajime:
        self.placar_hajime()

    self.placar_yame(pergunta=False) 
    vencedor = self.procura_vencedor()

    if vencedor.cor == "Empate":
      print("Empate!")
    else:
      console.print(f'O vencedor é {self.cor_atleta(vencedor)}')
      
    self.listener.stop()
