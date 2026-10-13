
const API_URL = "https://todo-list-api-qbo7.onrender.com";

const usuario = document.getElementById("usuario");
const senha = document.getElementById("senha");
const entrar = document.getElementById("entrar");
const cadastrar = document.getElementById("cadastrar");
const sair = document.getElementById("sair");
const mensagem = document.getElementById("mensagem");

const areaAutenticacao = document.getElementById("area-autenticacao");
const areaTarefas = document.getElementById("area-tarefas");

const titulo = document.getElementById("titulo");
const descricao = document.getElementById("descricao");
const adicionar = document.getElementById("adicionar");
const lista = document.getElementById("lista");

function mostrarMensagem(texto) {
    mensagem.textContent = texto;
}

function obterToken() {
    return localStorage.getItem("access_token");
}

function obterCabecalhos(json = false) {
    const headers = {
        Authorization: `Bearer ${obterToken()}`
    };

    if (json) {
        headers["Content-Type"] = "application/json";
    }

    return headers;
}

async function requisicao(url, opcoes = {}) {
    const resposta = await fetch(`${API_URL}${url}`, opcoes);

    if (!resposta.ok) {
        const erro = await resposta.json().catch(() => ({}));
        throw new Error(erro.detail || `Erro HTTP ${resposta.status}`);
    }

    if (resposta.status === 204) {
        return null;
    }

    return resposta.json();
}

function configurarAutenticacao(token) {
    localStorage.setItem("access_token", token);
    areaAutenticacao.hidden = true;
    areaTarefas.hidden = false;
    mostrarMensagem("");
    carregarTarefas();
}

entrar.addEventListener("click", async function () {
    try {
        const resultado = await requisicao("/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                username: usuario.value,
                password: senha.value
            })
        });

        configurarAutenticacao(resultado.access_token);
    } catch (erro) {
        mostrarMensagem(`Não foi possível entrar: ${erro.message}`);
    }
});

cadastrar.addEventListener("click", async function () {
    try {
        await requisicao("/users", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                username: usuario.value,
                password: senha.value
            })
        });

        mostrarMensagem("Conta criada! Agora clique em Entrar.");
    } catch (erro) {
        mostrarMensagem(`Não foi possível cadastrar: ${erro.message}`);
    }
});

function cancelarEdicao() {
    delete titulo.dataset.taskId;
    titulo.value = "";
    descricao.value = "";
    adicionar.textContent = "Adicionar tarefa";
}

function prepararEdicao(tarefa) {
    titulo.value = tarefa.title;
    descricao.value = tarefa.description;
    titulo.dataset.taskId = String(tarefa.id);
    adicionar.textContent = "Salvar edição";
    titulo.focus();
}

async function carregarTarefas() {
    try {
        const resultado = await requisicao("/tasks", {
            headers: obterCabecalhos()
        });

        lista.replaceChildren();

        for (const tarefa of resultado.tasks) {
            const item = document.createElement("li");

            const texto = document.createElement("span");
            texto.textContent = `${tarefa.title} - ${tarefa.description}`;

            if (tarefa.completed) {
                texto.style.textDecoration = "line-through";
            }

            const editar = document.createElement("button");
            editar.textContent = "Editar";

            editar.addEventListener("click", function () {
                prepararEdicao(tarefa);
            });

            const concluir = document.createElement("button");
            concluir.textContent = tarefa.completed ? "Reabrir" : "Concluir";

            concluir.addEventListener("click", async function () {
                try {
                    await requisicao(`/tasks/${tarefa.id}`, {
                        method: "PATCH",
                        headers: obterCabecalhos(true),
                        body: JSON.stringify({
                            completed: !tarefa.completed
                        })
                    });

                    mostrarMensagem("");
                    await carregarTarefas();
                } catch (erro) {
                    mostrarMensagem(`Erro ao atualizar tarefa: ${erro.message}`);
                }
            });

            const excluir = document.createElement("button");
            excluir.textContent = "Excluir";

            excluir.addEventListener("click", async function () {
                const confirmar = confirm(
                    `Deseja excluir a tarefa "${tarefa.title}"?`
                );

                if (!confirmar) {
                    return;
                }

                try {
                    await requisicao(`/tasks/${tarefa.id}`, {
                        method: "DELETE",
                        headers: obterCabecalhos()
                    });

                    if (titulo.dataset.taskId === String(tarefa.id)) {
                        cancelarEdicao();
                    }

                    mostrarMensagem("Tarefa excluída com sucesso.");
                    await carregarTarefas();
                } catch (erro) {
                    mostrarMensagem(`Erro ao excluir tarefa: ${erro.message}`);
                }
            });

            item.appendChild(texto);
            item.appendChild(document.createTextNode(" "));
            item.appendChild(editar);
            item.appendChild(document.createTextNode(" "));
            item.appendChild(concluir);
            item.appendChild(document.createTextNode(" "));
            item.appendChild(excluir);

            lista.appendChild(item);
        }
    } catch (erro) {
        mostrarMensagem(`Erro ao carregar tarefas: ${erro.message}`);

        if (
            erro.message.toLowerCase().includes("token") ||
            erro.message.includes("401")
        ) {
            encerrarSessao();
        }
    }
}

adicionar.addEventListener("click", async function () {
    const tituloTarefa = titulo.value.trim();
    const descricaoTarefa = descricao.value.trim();
    const taskId = titulo.dataset.taskId;

    if (!tituloTarefa) {
        alert("Digite o título da tarefa.");
        titulo.focus();
        return;
    }

    try {
        if (taskId) {
            await requisicao(`/tasks/${taskId}`, {
                method: "PATCH",
                headers: obterCabecalhos(true),
                body: JSON.stringify({
                    title: tituloTarefa,
                    description: descricaoTarefa
                })
            });

            mostrarMensagem("Tarefa editada com sucesso.");
        } else {
            await requisicao("/tasks", {
                method: "POST",
                headers: obterCabecalhos(true),
                body: JSON.stringify({
                    title: tituloTarefa,
                    description: descricaoTarefa,
                    completed: false,
                    priority: "media"
                })
            });

            mostrarMensagem("Tarefa criada com sucesso.");
        }

        cancelarEdicao();
        await carregarTarefas();
    } catch (erro) {
        mostrarMensagem(`Erro ao salvar tarefa: ${erro.message}`);
    }
});

function encerrarSessao() {
    localStorage.removeItem("access_token");
    cancelarEdicao();

    areaAutenticacao.hidden = false;
    areaTarefas.hidden = true;

    lista.replaceChildren();
    senha.value = "";

    mostrarMensagem("");
}

sair.addEventListener("click", encerrarSessao);

if (obterToken()) {
    areaAutenticacao.hidden = true;
    areaTarefas.hidden = false;
    carregarTarefas();
} else {
    areaAutenticacao.hidden = false;
    areaTarefas.hidden = true;
}
