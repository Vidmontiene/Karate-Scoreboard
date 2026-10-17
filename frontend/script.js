ESQ = 0;
DIR = 1;
let yame = true

// Fila de operações
let filaOper = Promise.resolve();

// Transforma duração em segundos em MM:SS
function transforma_duracao(tempo_segundos) {
  const minutos = Math.floor(tempo_segundos / 60);
  const segundos = tempo_segundos % 60;
  return `${String(minutos).padStart(2, "0")}:${String(segundos).padStart(2, "0")}`;
}

// Atualiza o placar com base no objeto Partida
async function atualizarPlacar() {

  // Pega as informações da partida
  const dados = await window.pywebview.api.obter_placar();

  let orientacao = dados.orientacao;
  
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

// Inicia/Para cronometro
function cronometro(){
  yame = !yame
  console.log(yame)
}

// Listeners
window.addEventListener("pywebviewready", () => { 
  atualizarPlacar(); // Quando inicia execução

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
});

document.addEventListener("keydown", (evento) => {
  if (evento.code === "Space") {
    cronometro(); // Inicia/Para cronometro
  }
});

