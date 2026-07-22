// 1. Alertas somem depois de 4 segundos
setTimeout(function () {
  document.querySelectorAll(".alert-success").forEach(function (alerta) {
    alerta.style.display = "none";
  });
}, 4000);

// 2. Confirmação antes de excluir
document.querySelectorAll("form[action*='excluir']").forEach(function (form) {
  form.addEventListener("submit", function (evento) {
    if (!confirm("Tem certeza que deseja excluir?")) {
      evento.preventDefault();
    }
  });
});

// 3. Contador de caracteres na descrição
const descricao = document.querySelector("#id_descricao");
if (descricao) {
  const contador = document.createElement("small");
  contador.className = "text-muted";
  descricao.parentNode.appendChild(contador);

  function atualizar() {
    contador.textContent = descricao.value.length + " caracteres";
  }

  descricao.addEventListener("input", atualizar);
  atualizar();
}

// 4. Aceitar orçamento sem recarregar a página
function getCsrfToken() {
  const input = document.querySelector("[name=csrfmiddlewaretoken]");
  return input ? input.value : "";
}

document.querySelectorAll(".btn-aceitar").forEach(function (botao) {
  botao.addEventListener("click", function () {
    const url = botao.dataset.url;
    const container = botao.parentNode;

    fetch(url, {
      method: "POST",
      headers: {
        "X-CSRFToken": getCsrfToken(),
      },
    })
      .then(function (resposta) {
        return resposta.json();
      })
      .then(function (dados) {
        if (dados.ok) {
          const badge = document.createElement("span");
          badge.className = "badge bg-success";
          badge.textContent = "Aceito";
          container.appendChild(badge);

          document.querySelectorAll(".btn-aceitar").forEach(function (b) {
            b.remove();
          });
        } else {
          alert("Erro: " + dados.erro);
        }
      })
      .catch(function (erro) {
        console.error("Detalhe do erro:", erro);
        alert("Algo deu errado. Veja o console.");
      });
  });
});