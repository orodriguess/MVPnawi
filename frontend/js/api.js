// frontend/js/api.js
// Centraliza todas as chamadas ao backend da aplicação NAWI 🧠
// Foco em segurança, clareza e consistência entre endpoints.

const API_BASE = "http://127.0.0.1:5000";

/* --------------------------- PRODUTOS BASE --------------------------- */
export async function getProdutosBase() {
  try {
    const res = await fetch(`${API_BASE}/produtos_base/`);
    if (!res.ok) throw new Error(`Erro ao buscar produtos base: ${res.status}`);
    const data = await res.json();
    console.log("📦 Produtos carregados:", data);
    return data;
  } catch (error) {
    console.error("❌ Falha em getProdutosBase:", error);
    return [];
  }
}

/* ---------------------------- CÁLCULOS ---------------------------- */
export async function calcular(produto_id, parametros, numero_pessoas = 1) {
  try {
    const res = await fetch(`${API_BASE}/calculadora/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ produto_id, parametros, numero_pessoas })
    });
    if (!res.ok) throw new Error(`Erro ${res.status} ao calcular`);
    return await res.json();
  } catch (error) {
    console.error("❌ Erro ao calcular:", error);
    return { duracao_dias: null, detalhes: { error: error.message } };
  }
}

/* -------------------------- ITENS DO USUÁRIO -------------------------- */
export async function salvarItem(usuario_id, produto_id, parametros) {
  try {
    const res = await fetch(`${API_BASE}/itens_usuario/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ usuario_id, produto_id, parametros })
    });
    if (!res.ok) throw new Error(`Erro ${res.status} ao salvar item`);
    const data = await res.json();
    console.log("💾 Item salvo com sucesso:", data);
    return data;
  } catch (error) {
    console.error("❌ Falha em salvarItem:", error);
    throw error;
  }
}

export async function listarItensUsuario(usuario_id) {
  try {
    const res = await fetch(`${API_BASE}/itens_usuario?usuario_id=${usuario_id}`);
    if (!res.ok) throw new Error(`Erro ${res.status} ao listar itens`);
    const data = await res.json();
    console.log(`📋 Itens do usuário ${usuario_id}:`, data);
    return data;
  } catch (error) {
    console.error("❌ Falha em listarItensUsuario:", error);
    return [];
  }
}
