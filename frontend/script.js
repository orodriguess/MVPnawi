const API_URL = "http://127.0.0.1:5000/usuarios/";

document.getElementById("btnCadastrar").addEventListener("click", async () => {
    const nome = document.getElementById("nome").value.trim();
    const email = document.getElementById("email").value.trim();

    if (!nome || !email) {
        alert("Por favor, preencha seu nome e e-mail!");
        return;
    }

    const resp = await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ nome, email })
    });

    if (resp.ok) {
        const usuario = await resp.json();
        localStorage.setItem("usuarioNome", usuario.nome);
        localStorage.setItem("usuarioEmail", usuario.email);
        alert(`Bem-vindo, ${usuario.nome}!`);
        window.location.href = "produtos.html"; // redireciona
    } else {
        alert("Erro ao cadastrar usuário.");
    }
});
