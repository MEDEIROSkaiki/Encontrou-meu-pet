document.addEventListener('DOMContentLoaded', () => {
  const racaSelect = document.getElementById('raca');
  const especie = localStorage.getItem('especie'); // Ex: "gato", "cachorro", etc.
  const especieMap = { cachorro: 1, gato: 2, passaro: 3 };
  const idespecie = especieMap[especie];

  if (!idespecie) {
    console.warn('Espécie não definida no localStorage.');
    return;
  }

  fetch('/racas', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ idespecie: idespecie })
  })
  .then(res => res.json())
  .then(racas => {
    // Limpa o select e adiciona o placeholder
    racaSelect.innerHTML = '<option value="">Selecione</option>';

    racas.forEach(raca => {
      const option = document.createElement('option');
      option.value = raca.nome.toLowerCase();
      option.textContent = raca.nome;
      racaSelect.appendChild(option);
    });

    // Restaura a raça previamente salva (se houver)
    const racaSalva = localStorage.getItem('raca');
    if (racaSalva) {
      racaSelect.value = racaSalva;
    }
  })
  .catch(error => {
    console.error('Erro ao buscar raças:', error);
    alert('Erro ao carregar as raças. Tente novamente mais tarde.');
  });
});

