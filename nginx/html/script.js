// script.js
// Toda comunicação com a API passa por /api (o NGINX redireciona para o FastAPI)

const API = '/api';

// ═══════════════════════════════════════════════
//                   PERFIS
// ═══════════════════════════════════════════════

// Busca todos os perfis e preenche a tabela
async function carregarPerfis() {
  const resp = await fetch(`${API}/perfis/`);
  const perfis = await resp.json();

  const tbody = document.querySelector('#tabela-perfis tbody');
  tbody.innerHTML = '';

  if (perfis.length === 0) {
    tbody.innerHTML = '<tr><td colspan="4">Nenhum perfil cadastrado.</td></tr>';
    return;
  }

  perfis.forEach(p => {
    tbody.innerHTML += `
      <tr>
        <td>${p.id}</td>
        <td>${p.nome}</td>
        <td>${p.descricao || '—'}</td>
        <td>
          <button class="btn-editar" onclick="editarPerfil(${p.id}, '${p.nome}', '${p.descricao || ''}')">Editar</button>
          <button class="btn-deletar" onclick="deletarPerfil(${p.id})">Excluir</button>
        </td>
      </tr>
    `;
  });

  // Atualiza o <select> dentro do modal de usuário com os perfis disponíveis
  atualizarSelectPerfis(perfis);
}

// Preenche o <select> de perfis no modal de usuário
function atualizarSelectPerfis(perfis) {
  const select = document.getElementById('usuario-perfil');
  select.innerHTML = '<option value="">— Sem perfil —</option>';
  perfis.forEach(p => {
    select.innerHTML += `<option value="${p.id}">${p.nome}</option>`;
  });
}

// Salva ou atualiza um perfil
async function salvarPerfil() {
  const id   = document.getElementById('perfil-id').value;
  const nome = document.getElementById('perfil-nome').value.trim();
  const desc = document.getElementById('perfil-descricao').value.trim();

  if (!nome) {
    alert('O nome do perfil é obrigatório.');
    return;
  }

  const corpo = { nome, descricao: desc || null };

  if (id) {
    // PUT — atualiza perfil existente
    await fetch(`${API}/perfis/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(corpo),
    });
  } else {
    // POST — cria novo perfil
    await fetch(`${API}/perfis/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(corpo),
    });
  }

  fecharModal('modal-perfil');
  carregarPerfis();
}

// Preenche o modal com os dados do perfil para edição
function editarPerfil(id, nome, descricao) {
  abrirModal('modal-perfil');
  document.getElementById('titulo-modal-perfil').textContent = 'Editar Perfil';
  document.getElementById('perfil-id').value        = id;
  document.getElementById('perfil-nome').value      = nome;
  document.getElementById('perfil-descricao').value = descricao;
}

// Deleta um perfil após confirmação
async function deletarPerfil(id) {
  if (!confirm('Excluir este perfil?')) return;
  await fetch(`${API}/perfis/${id}`, { method: 'DELETE' });
  carregarPerfis();
}


// ═══════════════════════════════════════════════
//                  USUÁRIOS
// ═══════════════════════════════════════════════

// Busca todos os usuários e preenche a tabela
async function carregarUsuarios() {
  const resp     = await fetch(`${API}/usuarios/`);
  const usuarios = await resp.json();

  const tbody = document.querySelector('#tabela-usuarios tbody');
  tbody.innerHTML = '';

  if (usuarios.length === 0) {
    tbody.innerHTML = '<tr><td colspan="5">Nenhum usuário cadastrado.</td></tr>';
    return;
  }

  usuarios.forEach(u => {
    tbody.innerHTML += `
      <tr>
        <td>${u.id}</td>
        <td>${u.nome}</td>
        <td>${u.email}</td>
        <td>${u.perfil_nome || '—'}</td>
        <td>
          <button class="btn-editar" onclick="editarUsuario(${u.id}, '${u.nome}', '${u.email}', ${u.perfil_id || null})">Editar</button>
          <button class="btn-deletar" onclick="deletarUsuario(${u.id})">Excluir</button>
        </td>
      </tr>
    `;
  });
}

// Salva ou atualiza um usuário
async function salvarUsuario() {
  const id       = document.getElementById('usuario-id').value;
  const nome     = document.getElementById('usuario-nome').value.trim();
  const email    = document.getElementById('usuario-email').value.trim();
  const senha    = document.getElementById('usuario-senha').value;
  const perfilId = document.getElementById('usuario-perfil').value;

  if (!nome || !email) {
    alert('Nome e e-mail são obrigatórios.');
    return;
  }

  if (!id && !senha) {
    alert('A senha é obrigatória para novos usuários.');
    return;
  }

  const corpo = {
    nome,
    email,
    perfil_id: perfilId ? parseInt(perfilId) : null,
  };

  if (senha) corpo.senha = senha;

  if (id) {
    // PUT — atualiza usuário existente
    await fetch(`${API}/usuarios/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(corpo),
    });
  } else {
    // POST — cria novo usuário (senha obrigatória)
    await fetch(`${API}/usuarios/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ ...corpo, senha }),
    });
  }

  fecharModal('modal-usuario');
  carregarUsuarios();
}

// Preenche o modal com os dados do usuário para edição
function editarUsuario(id, nome, email, perfilId) {
  abrirModal('modal-usuario');
  document.getElementById('titulo-modal-usuario').textContent = 'Editar Usuário';
  document.getElementById('usuario-id').value     = id;
  document.getElementById('usuario-nome').value   = nome;
  document.getElementById('usuario-email').value  = email;
  document.getElementById('usuario-senha').value  = '';
  document.getElementById('usuario-perfil').value = perfilId || '';
}

// Deleta um usuário após confirmação
async function deletarUsuario(id) {
  if (!confirm('Excluir este usuário?')) return;
  await fetch(`${API}/usuarios/${id}`, { method: 'DELETE' });
  carregarUsuarios();
}


// ═══════════════════════════════════════════════
//               CONTROLE DE MODAIS
// ═══════════════════════════════════════════════

function abrirModal(id) {
  // Limpa os campos ao abrir para criação
  if (id === 'modal-perfil') {
    document.getElementById('titulo-modal-perfil').textContent = 'Novo Perfil';
    document.getElementById('perfil-id').value        = '';
    document.getElementById('perfil-nome').value      = '';
    document.getElementById('perfil-descricao').value = '';
  }
  if (id === 'modal-usuario') {
    document.getElementById('titulo-modal-usuario').textContent = 'Novo Usuário';
    document.getElementById('usuario-id').value     = '';
    document.getElementById('usuario-nome').value   = '';
    document.getElementById('usuario-email').value  = '';
    document.getElementById('usuario-senha').value  = '';
    document.getElementById('usuario-perfil').value = '';
  }
  document.getElementById(id).style.display = 'flex';
}

function fecharModal(id) {
  document.getElementById(id).style.display = 'none';
}

// Fecha o modal ao clicar fora da caixa
document.querySelectorAll('.modal-fundo').forEach(fundo => {
  fundo.addEventListener('click', function(e) {
    if (e.target === this) this.style.display = 'none';
  });
});


// ═══════════════════════════════════════════════
//                INICIALIZAÇÃO
// ═══════════════════════════════════════════════

// Carrega os dados ao abrir a página
carregarPerfis();
carregarUsuarios();
