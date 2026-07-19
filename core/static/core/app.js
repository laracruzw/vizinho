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