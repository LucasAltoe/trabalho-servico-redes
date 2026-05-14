const API = '/api';

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

  atualizarSelectPerfis(perfis);
}

function atualizarSelectPerfis(perfis) {
  const select = document.getElementById('usuario-perfil');
  select.innerHTML = '<option value="">— Sem perfil —</option>';
  perfis.forEach(p => {
    select.innerHTML += `<option value="${p.id}">${p.nome}</option>`;
  });
}

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
    await fetch(`${API}/perfis/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(corpo),
    });
  } else {
    await fetch(`${API}/perfis/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(corpo),
    });
  }

  fecharModal('modal-perfil');
  carregarPerfis();
}

function editarPerfil(id, nome, descricao) {
  abrirModal('modal-perfil');
  document.getElementById('titulo-modal-perfil').textContent = 'Editar Perfil';
  document.getElementById('perfil-id').value        = id;
  document.getElementById('perfil-nome').value      = nome;
  document.getElementById('perfil-descricao').value = descricao;
}

async function deletarPerfil(id) {
  if (!confirm('Excluir este perfil?')) return;
  await fetch(`${API}/perfis/${id}`, { method: 'DELETE' });
  carregarPerfis();
}

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
    await fetch(`${API}/usuarios/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(corpo),
    });
  } else {
    await fetch(`${API}/usuarios/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ ...corpo, senha }),
    });
  }

  fecharModal('modal-usuario');
  carregarUsuarios();
}

function editarUsuario(id, nome, email, perfilId) {
  abrirModal('modal-usuario');
  document.getElementById('titulo-modal-usuario').textContent = 'Editar Usuário';
  document.getElementById('usuario-id').value     = id;
  document.getElementById('usuario-nome').value   = nome;
  document.getElementById('usuario-email').value  = email;
  document.getElementById('usuario-senha').value  = '';
  document.getElementById('usuario-perfil').value = perfilId || '';
}

async function deletarUsuario(id) {
  if (!confirm('Excluir este usuário?')) return;
  await fetch(`${API}/usuarios/${id}`, { method: 'DELETE' });
  carregarUsuarios();
}

function abrirModal(id) {
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

document.querySelectorAll('.modal-fundo').forEach(fundo => {
  fundo.addEventListener('click', function(e) {
    if (e.target === this) this.style.display = 'none';
  });
});

carregarPerfis();
carregarUsuarios();
