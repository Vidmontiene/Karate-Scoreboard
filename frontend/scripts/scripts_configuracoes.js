const botaoPersonalizado = document.getElementById("botao_personalizado");

// Encerra execução
async function encerrar() {
  await window.pywebview.api.encerrar();
}

// Volta para tela inical
function voltar() {
  window.location.href = "duracao.html";
}

// Seleciona duração e muda para a próxima página
async function selecionar_duracao(tempo){
  await window.pywebview.api.set_duracao(tempo);
  window.location.href = "orientacao.html";
}

// Seleciona orientacao e muda para a próxima página
async function selecionar_orientacao(orientacao){
  await window.pywebview.api.set_orientacao(orientacao);
  await window.pywebview.api.iniciar_placar();
  window.location.href = "placar.html";
}

botaoPersonalizado.addEventListener("click", () => {
  // Evita criar outro input se já estiver editando
  if (botaoPersonalizado.querySelector("input")) return;

  botaoPersonalizado.innerHTML = `
    <input
      id="input_personalizado"
      type="text"
      placeholder="MM:SS"
      maxlength="5"
      pattern="^[0-5][0-9]\:[0-5][0-9]\"
    >
  `;

  const input = document.getElementById("input_personalizado");
  input.focus();

  // Formata automaticamente para MM:SS
  let digitos = "";

  input.addEventListener("keydown", (e) => {
    if (e.key >= "0" && e.key <= "9") {
      e.preventDefault();

      digitos = (digitos + e.key).slice(-4);

      const valor = digitos.padStart(4, "0");
      input.value = valor.slice(0, 2) + ":" + valor.slice(2);
    } else if (e.key === "Backspace") {
      e.preventDefault();

      digitos = digitos.slice(0, -1);

      const valor = digitos.padStart(4, "0");
      input.value = valor.slice(0, 2) + ":" + valor.slice(2);
    }
  });

  // Quando apertar Enter
  input.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
      const formatoValido = /^\d{2}:\d{2}$/.test(input.value);

      if (!formatoValido) {
        alert("Digite o tempo no formato MM:SS.");
        input.focus();
        return;
      }

      const [minutos, segundos] = input.value.split(":").map(Number);

      if (segundos > 59 || (minutos === 0 && segundos === 0)) {
        alert("Digite um tempo válido.");
        input.focus();
        return;
      }

      const duracao = minutos * 60 + segundos;
      selecionar_duracao(duracao)
    }
  });

  // Se perder o foco, volta ao botão se estiver vazio
  input.addEventListener("blur", () => {
    if (input.value === "") {
      botaoPersonalizado.innerHTML =
        '<p class="txt_botao">Personalizado</p>';
    }
  });
});