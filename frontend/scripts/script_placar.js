// Constantes
const ESQ = 0;
const DIR = 1;
const AKA_ESQ = 0
const AKA_DIR = 1

// Variáveis
let yame = true
let intervalo = null;
let tempoRestante = null;
let intervaloVencedor = null;

// Fila de operações
let filaOper = Promise.resolve();

// Transforma duração em segundos em MM:SS
function transforma_duracao(tempo_segundos) {
  const minutos = Math.floor(tempo_segundos / 60);
  const segundos = tempo_segundos % 60;
  return `${String(minutos).padStart(2, "0")}:${String(segundos).padStart(2, "0")}`;
}

// Define a orientacao
async function orienta(){
  const dados = await window.pywebview.api.obter_placar();
  const orientacao = dados.orientacao

  const esquerda = document.querySelector("#lado_esquerdo > .ponto");
  const direita = document.querySelector("#lado_direito > .ponto");

  if (orientacao === AKA_ESQ){
    esquerda.style.backgroundColor = "red";
    esquerda.style.borderColor = "red";
    direita.style.backgroundColor = "blue";
    direita.style.borderColor = "blue";
  }
  else{
    esquerda.style.backgroundColor = "blue";
    esquerda.style.borderColor = "blue";
    direita.style.backgroundColor = "red";
    direita.style.borderColor = "red";
  }
}

// Atualiza o placar com base no objeto Partida
async function atualizarPlacar() {

  // Pega as informações da partida
  const dados = await window.pywebview.api.obter_placar();

  // Lado esquerdo
  document.getElementById("ponto_esq").textContent =
    dados.esq.pontos;

  document.getElementById("senshu_esq").textContent =
    dados.esq.senshu ? "S" : "";

  document.getElementById("penalidade_esq").textContent =
    `${"x".repeat(dados.esq.penalidades)}`;
  //

  // Lado esquerdo
  document.getElementById("ponto_dir").textContent =
    dados.dir.pontos;

  document.getElementById("senshu_dir").textContent =
    dados.dir.senshu ? "S" : "";

  document.getElementById("penalidade_dir").textContent =
    `${"x".repeat(dados.dir.penalidades)}`;
  //

  // Cronômetro
  document.getElementById("cronometro").textContent =
    transforma_duracao(dados.duracao);

  // Pisca vencedor
  if (dados.terminada){
    await destaca_vencedor();
  }
}

// Pontuar
function pontua(alvo) {
  filaOper = filaOper.then(
    async () => {
      await window.pywebview.api.pontua(alvo);
      await atualizarPlacar();
    })
    .catch(erro => {
      console.error("Erro ao modificar pontuação:", erro);
    });
  return filaOper;
}

// Senshu
function senshu(alvo) {
  filaOper = filaOper
    .then(async () => {
      await window.pywebview.api.modificar_senshu(alvo);
      await atualizarPlacar();
    })
    .catch(erro => {
      console.error("Erro ao modificar senshu:", erro);
    });
  return filaOper;
}

// Penaliza
function penaliza(alvo) {
  filaOper = filaOper
    .then(async () => {
      await window.pywebview.api.penaliza(alvo);
      await atualizarPlacar();
    })
    .catch(erro => {
      console.error("Erro ao penalizar:", erro);
    });
  return filaOper;
}

// Remove ponto
function remove_ponto(alvo) {
  filaOper = filaOper
    .then(async () => {
      await window.pywebview.api.remove_ponto(alvo);
      await atualizarPlacar();
    })
    .catch(erro => {
      console.error("Erro ao remover ponto:", erro);
    });
  return filaOper;
}

// Remove ppenalidade
function remove_penalidade(alvo) {
  filaOper = filaOper
    .then(async () => {
      await window.pywebview.api.remove_penalidade(alvo);
      await atualizarPlacar();
    })
    .catch(erro => {
      console.error("Erro ao remover penalidade:", erro);
    });
  return filaOper;
}

// Atualiza apenas o cronômetro na tela
function atualizarCronometro() {
  document.getElementById("cronometro").textContent =
    transforma_duracao(tempoRestante);
}

// Inicia/Para cronometro
async function cronometro() {

  // Se está rodando, pausa
  if (yame) {
    clearInterval(intervalo);
    intervalo = null;
    yame = false;

    if (tempoRestante != null) {
      filaOper = filaOper.then(() =>
        window.pywebview.api.modifica_duracao(tempoRestante)
      );

      await filaOper;
    }

    return;
  }

  // Busca a duração na primeira execução
  if (tempoRestante === null) {
    const dados = await window.pywebview.api.obter_placar();
    tempoRestante = dados.duracao;
  }

  // Não inicia se o tempo acabou
  if (tempoRestante <= 0) return;

  // Inicia
  yame = true;

  intervalo = setInterval(() => {
    tempoRestante--;
    atualizarCronometro();

    // Enfileira a atualização da duração no Python
    filaOper = filaOper
      .then(() => window.pywebview.api.modifica_duracao(tempoRestante))
      .catch(erro => {
        console.error("Erro ao atualizar duração:", erro);
      });

    if (tempoRestante <= 0) {
      clearInterval(intervalo);
      intervalo = null;
      yame = false;

      // Aguarda as operações pendentes antes de atualizar o placar
      filaOper = filaOper.then(() => atualizarPlacar());
    }
  }, 1000);
}

// Pisca o lado vencedor
async function destaca_vencedor() {
  if (intervaloVencedor !== null) return;

  const info = await window.pywebview.api.obter_vencedor();
  let elemento = null

  if (
    (info.orientacao == AKA_ESQ && info.vencedor === "Aka") 
    || 
    (info.orientacao == AKA_DIR && info.vencedor === "Ao")
  ){
    elemento = document.getElementById("lado_esquerdo");
  }
  else if (
    (info.orientacao == AKA_ESQ && info.vencedor === "Ao") 
    || 
    (info.orientacao == AKA_DIR && info.vencedor === "Aka")
  ){
    elemento = document.getElementById("lado_direito");
  }
  else {
    elemento = document.getElementById("tempo");
    console.log("Empate")
  }

  // Pisca vencedor
  intervaloVencedor = setInterval(() => {
    elemento.style.visibility =
      elemento.style.visibility === "hidden" ? "visible" : "hidden";
  }, 500);
}

// Listeners
window.addEventListener("pywebviewready", () => { 
  orienta() // Coloca as cores no lugar certo
  atualizarPlacar(); // Inicia placar
  
  document.getElementById("botao_ponto_esq")
    .addEventListener("click", () => pontua(ESQ)); // Pontua esquerdo
  document.getElementById("botao_ponto_dir")
    .addEventListener("click", () => pontua(DIR)); // Pontua direito

  document.getElementById("botao_senshu_esq")
    .addEventListener("click", () => senshu(ESQ)); // Senshu esquerdo
  document.getElementById("botao_senshu_dir")
    .addEventListener("click", () => senshu(DIR)); // Senshu direito

  document.getElementById("botao_penalidade_esq")
    .addEventListener("click", () => penaliza(ESQ)); // Penaliza esquerdo
  document.getElementById("botao_penalidade_dir")
    .addEventListener("click", () => penaliza(DIR)); // Penaliza direito

  document.getElementById("botao_ponto_esq").addEventListener("contextmenu", (evento) => {
    evento.preventDefault(); // Impede o menu de contexto
    remove_ponto(ESQ);       // Remove ponto esquerdo
  });
  document.getElementById("botao_ponto_dir").addEventListener("contextmenu", (evento) => {
    evento.preventDefault(); // Impede o menu de contexto
    remove_ponto(DIR);       // Remove ponto direito
  });

  document.getElementById("botao_senshu_esq").addEventListener("contextmenu", (evento) => {
    evento.preventDefault(); // Impede o menu de contexto
    senshu(ESQ);            // Senshu esquerdo
  });
  document.getElementById("botao_senshu_dir").addEventListener("contextmenu", (evento) => {
    evento.preventDefault(); // Impede o menu de contexto
    senshu(DIR);             // Senshu direito
  });

  document.getElementById("botao_penalidade_esq").addEventListener("contextmenu", (evento) => {
    evento.preventDefault(); // Impede o menu de contexto
    remove_penalidade(ESQ);  // Remove penalidade esquerdo
  });
  document.getElementById("botao_penalidade_dir").addEventListener("contextmenu", (evento) => {
    evento.preventDefault(); // Impede o menu de contexto
    remove_penalidade(DIR);  // Remove penalidade direito
  });

  document.getElementById("tempo")
    .addEventListener("click", () => cronometro()); // Inicia/Pausa cronometro
});

// Detecta pressionar de teclas
document.addEventListener("keydown", (evento) => {

  // Espaço
  if (evento.code === "Space") {
    evento.preventDefault();

    if (!evento.repeat) {
      cronometro();   // Inicia/Pausa cronometro
    }
  }

  // Esc
  else if (evento.code === "Escape"){
    window.location.href = "duracao.html";
  }
});

// Tira o foco dos botões ao apertar 
document.querySelectorAll("button").forEach((botao) => {
  botao.addEventListener("click", () => {
    botao.blur();
  });
});
