import { getProdutosBase, calcular, salvarItem, listarItensUsuario } from "./api.js";

const usuarioId = localStorage.getItem("usuario_id");
const usuarioNome = localStorage.getItem("usuario_nome");

if(!usuarioId) window.location.href = "index.html";

document.getElementById("userInfo").textContent = `Usuário: ${usuarioNome}`;
const produtoSelect = document.getElementById("produto");
const parametrosDiv = document.getElementById("parametros");
const resultadoDiv = document.getElementById("resultadoCalculo");
const tabelaBody = document.querySelector("#tabelaProdutos tbody");

let produtosBase = [];

init();

async function init(){
  produtosBase = await getProdutosBase();
  renderProdutos();
  await carregarItens();
}

async function renderProdutos(){
  produtoSelect.innerHTML = "<option value=''>Selecione...</option>";
  produtosBase.forEach(p=>{
    const opt = document.createElement("option");
    opt.value = p.id;
    opt.textContent = p.nome;
    produtoSelect.appendChild(opt);
  });
}

produtoSelect.addEventListener("change", ()=>{
  const produto = produtosBase.find(p=>p.id == produtoSelect.value);
  renderParametros(produto);
});

produtoSelect.addEventListener("click", ()=>{
  if(produtoSelect.value === ""){
    parametrosDiv.innerHTML = "";
  }
});

function renderParametros(produto){
  parametrosDiv.innerHTML = "";
  if(!produto) return;
  
  // Gera campos conforme tipo_calculo
  const tipo = (produto.tipo_calculo || "generico").toLowerCase();

  let campos = [];
  if(["multiplicativo","papel_higienico"].includes(tipo)){
    campos = [
      {id:"unidades", label:"Nº de unidades (ex: rolos)"},
      {id:"conteudo_por_unidade", label:`Conteúdo por unidade (${produto.unidade_principal})`},
      {id:"consumo_diario", label:`Consumo diário (${produto.unidade_principal})`}
    ];
  }else{
    campos = [
      {id:"quantidade_total", label:`Quantidade total (${produto.unidade_principal})`},
      {id:"consumo_diario", label:`Consumo diário (${produto.unidade_principal})`}
    ];
  }

  campos.forEach(c=>{
    const lbl = document.createElement("label");
    lbl.textContent = c.label;
    const inp = document.createElement("input");
    inp.type = "number";
    inp.id = c.id;
    parametrosDiv.appendChild(lbl);
    parametrosDiv.appendChild(inp);
  });
}

document.getElementById("btnCalcular").addEventListener("click", async ()=>{
  const produtoId = produtoSelect.value;
  if(!produtoId) return alert("Selecione um produto.");

  const produto = produtosBase.find(p=>p.id == produtoId);
  const inputs = parametrosDiv.querySelectorAll("input");
  const params = {};
  inputs.forEach(i => params[i.id] = parseFloat(i.value || 0));

  const result = await calcular(produtoId, params, 1);
  resultadoDiv.textContent = result.duracao_dias 
    ? `Vai durar cerca de ${result.duracao_dias} dias.`
    : "Não foi possível calcular.";
});

document.getElementById("btnSalvar").addEventListener("click", async ()=>{
  const produtoId = produtoSelect.value;
  if(!produtoId) return alert("Selecione um produto.");

  const inputs = parametrosDiv.querySelectorAll("input");
  const params = {};
  inputs.forEach(i => params[i.id] = parseFloat(i.value || 0));

  await salvarItem(usuarioId, produtoId, params);
  await carregarItens();
  alert("Produto salvo com sucesso!");
});

async function carregarItens(){
  const itens = await listarItensUsuario(usuarioId);
  tabelaBody.innerHTML = "";
  itens.forEach(i=>{
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${i.produto_nome || "-"}</td>
      <td>${i.parametros?.quantidade_total || i.parametros?.unidades || "-"}</td>
      <td>${i.duracao_dias ? `${i.duracao_dias} dias` : "-"}</td>
    `;
    tabelaBody.appendChild(tr);
  });
}

document.addEventListener("DOMContentLoaded", renderProdutos);