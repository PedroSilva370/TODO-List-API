const titulo = document.getElementById("titulo");
const descricao = document.getElementById("descricao");
const botao = document.getElementById("adicionar");
const lista = document.getElementById("lista");

botao.addEventListener("click", async function() {

    const dados = {
        title: titulo.value,
        description: descricao.value
    };

    const resposta = await fetch("http://127.0.0.1:8000/tasks", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(dados)
    });

    const tarefa = await resposta.json();

    const novaTarefa = document.createElement("li");

    novaTarefa.textContent =
        tarefa.title + " - " + tarefa.description;

    lista.appendChild(novaTarefa);

    titulo.value = "";
    descricao.value = "";
});