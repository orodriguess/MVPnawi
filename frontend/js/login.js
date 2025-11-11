// client/js/login.js
const API_BASE = "http://127.0.0.1:5000";

document.getElementById("btnEntrar").addEventListener("click", entrar);
document.getElementById("email").addEventListener("keydown", (e)=>{
  if(e.key === "Enter") entrar();
});

function showError(msg){
  const el = document.getElementById("error");
  el.textContent = msg || "";
}

async function entrar(){
  const email = document.getElementById("email").value.trim();
  showError("");

  if(!email){
    showError("Por favor, informe um e-mail.");
    return;
  }
  // validação simples de formato
  const simpleEmailRe = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if(!simpleEmailRe.test(email)){
    showError("Formato de e-mail inválido.");
    return;
  }

  try{
    // 1) tenta obter usuário pelo email (assumi rota /usuarios?email=)
    const q = `${API_BASE}/usuarios?email=${encodeURIComponent(email)}`;
    const res = await fetch(q);
    let user = null;

    if(res.ok){
      const data = await res.json();
      if(Array.isArray(data) && data.length) user = data[0];
      else if(data && data.id) user = data;
    }

    // 2) se não existe, cria
    if(!user){
      const create = await fetch(`${API_BASE}/usuarios/`, {
        method: "POST",
        headers: {"Content-Type":"application/json"},
        body: JSON.stringify({ nome: email.split("@")[0], email })
      });
      if(!create.ok){
        const txt = await create.text();
        throw new Error(`Erro ao criar usuário: ${txt}`);
      }
      user = await create.json();
    }

    // 3) salva e navega
    localStorage.setItem("usuario_id", String(user.id));
    localStorage.setItem("usuario_nome", user.nome || "");
    window.location.href = "dashboard.html";

  }catch(err){
    console.error(err);
    showError("Erro ao conectar com o servidor. Verifique se a API está rodando.");
  }
}
