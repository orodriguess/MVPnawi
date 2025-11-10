const API_URL = "http://127.0.0.1:5000/itens/";
const usuarioNome = localStorage.getItem("usuarioNome");

document.getElementById("tituloUsuario").textContent =
    usuarioNome ? `Olá, ${usuarioNome}! Cadastre seus itens de consumo:` : "Cadastre seus itens:";

// ---------- LISTAR ----------
async function listarItens() {
    const resp = await fetch(API_URL);
    const itens = await resp.json();

    const lista = document.getElementById("listaItens");
    lista.innerHTML = "";

    itens.forEach(i => {
        const card = document.createElement("div");
        card.className = "col-md-4 mb-3";
        card.innerHTML = `
            <div class="card card-usuario p-3">
                <h5>${i.nome}</h5>
                <p>${i.quantidade_total} ${i.unidade}</p>
                <p>Consumo diário: ${i.consumo_diario} ${i.unidade}/dia</p>
                <p><strong>Dura aproximadamente ${i.duracao_estimada ?? '---'} dias</strong></p>
                <button class="btn btn-sm btn-delete text-white" onclick="deletarItem(${i.id})">Excluir</button>
            </div>
        `;
        lista.appendChild(card);
    });
}

// ---------- CADASTRAR ----------
document.getElementById("btnAdicionar").addEventListener("click", async () => {
    const nome = document.getElementById("nomeItem").value.trim();
    const quantidade_total = parseFloat(document.getElementById("quantidade").value);
    const unidade = document.getElementById("unidade").value.trim();
    const consumo_diario = parseFloat(document.getElementById("consumo").value);

    if (!nome || !quantidade_total || !consumo_diario) {
        alert("Preencha todos os campos obrigatórios!");
        return;
    }

    const resp = await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ nome, quantidade_total, unidade, consumo_diario })
    });

    if (resp.ok) {
        listarItens();
        document.getElementById("nomeItem").value = "";
        document.getElementById("quantidade").value = "";
        document.getElementById("unidade").value = "";
        document.getElementById("consumo").value = "";
    } else {
        alert("Erro ao adicionar item.");
    }
});

// ---------- DELETAR ----------
async function deletarItem(id) {
    if (!confirm("Deseja excluir este item?")) return;
    const resp = await fetch(`${API_URL}${id}`, { method: "DELETE" });
    if (resp.ok) listarItens();
}

// ---------- INICIALIZA ----------
listarItens();



// ---------- PRODUTOS BASE ----------
const API_PRODUTOS_BASE = "http://127.0.0.1:5000/produtos_base/";

async function carregarProdutosBase() {
    const resp = await fetch(API_PRODUTOS_BASE);
    const produtos = await resp.json();

    const select = document.getElementById("produtoSelect");
    produtos.forEach(p => {
        const opt = document.createElement("option");
        opt.value = p.tipo_calculo;
        opt.textContent = p.nome;
        select.appendChild(opt);
    });
}

document.getElementById("produtoSelect").addEventListener("change", (e) => {
    const tipo = e.target.value;
    const formContainer = document.getElementById("formCampos");
    formContainer.innerHTML = "";

    if (tipo === "papel_higienico") {
        formContainer.innerHTML = `
            <input type="number" id="rolos" class="form-control mb-2" placeholder="Quantidade de rolos">
            <input type="number" id="metros" class="form-control mb-2" placeholder="Metros por rolo">
        `;
    } else if (tipo === "pasta_dente" || tipo === "sabonete") {
        formContainer.innerHTML = `
            <input type="number" id="unidades" class="form-control mb-2" placeholder="Quantidade de unidades">
            <input type="number" id="gramas" class="form-control mb-2" placeholder="Gramas por unidade">
        `;
    } else {
        formContainer.innerHTML = `
            <input type="number" id="quantidade" class="form-control mb-2" placeholder="Quantidade total">
            <input type="number" id="consumo" class="form-control mb-2" placeholder="Consumo diário">
        `;
    }
});