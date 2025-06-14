// Elementos do DOM
const cepInput = document.getElementById("cep");
const enderecoInfoContainer = document.getElementById(
  "endereco-info-container"
);

const dddInput = document.getElementById("ddd");
const enderecoInput = document.getElementById("endereco");
const bairroInput = document.getElementById("bairro");
const cidadeInput = document.getElementById("cidade");
const estadoInput = document.getElementById("estado");

const naoSeiCepLink = document.getElementById("nao-sei-cep");
const modalNaoSeiCep = document.getElementById("modal-nao-sei-cep");
const closeModalButton = modalNaoSeiCep.querySelector(".close-button");
const ufSelect = document.getElementById("uf-select");
const municipioSelect = document.getElementById("municipio-select");
const logradouroInput = document.getElementById("logradouro-input");
const logradouroSuggestions = document.getElementById("logradouro-suggestions");
const buscarCepEnderecoButton = document.getElementById("buscar-cep-endereco");

let typingTimer; // Timer para o debounce da busca de logradouro
const doneTypingInterval = 500; // Tempo em ms para esperar antes de buscar

// --- Funções de manipulação do campo CEP ---

function formatarCEP(input) {
  let cep = input.value.replace(/\D/g, ""); // Remove tudo que não for dígito
  if (cep.length > 5) {
    cep = cep.substring(0, 5) + "-" + cep.substring(5); // Mantém o restante da digitação
  }
  input.value = cep;

  // Atualiza a borda enquanto o preenchimento não está completo
  if (cep.length > 0 && cep.length < 9) {
    cepInput.classList.add("cep-incomplete");
    cepInput.classList.remove("cep-success", "cep-error");
    enderecoInfoContainer.style.display = "none"; // Esconde enquanto incompleto
    limparCamposEndereco(); // Limpa os campos enquanto o CEP está incompleto
  } else if (cep.length === 0) {
    cepInput.classList.remove("cep-incomplete", "cep-success", "cep-error");
    enderecoInfoContainer.style.display = "none";
    limparCamposEndereco();
  }
}

async function buscarCEP(cep) {
  const cepLimpo = cep.replace(/\D/g, "");

  if (cepLimpo.length === 8) {
    cepInput.closest(".form-group").classList.add("processing");
    cepInput.classList.remove("cep-incomplete", "cep-error");
    cepInput.classList.add("processing"); // Adiciona indicador de processamento
    enderecoInfoContainer.style.display = "none"; // Esconde enquanto busca

    try {
      const response = await fetch(
        `https://viacep.com.br/ws/${cepLimpo}/json/`
      );
      const data = await response.json();
      cepInput.closest(".form-group").classList.remove("processing");

      cepInput.classList.remove("processing"); // Remove indicador

      if (data.erro) {
        limparCamposEndereco();
        cepInput.classList.add("cep-error"); // Borda vermelha
        cepInput.classList.remove("cep-success");
        alert("CEP não encontrado.");
      } else {
        preencherCamposEndereco(data);
        cepInput.classList.add("cep-success"); // Borda verde
        cepInput.classList.remove("cep-error");
        enderecoInfoContainer.style.display = "block"; // Mostra a div de informações
      }
    } catch (error) {
      console.error("Erro ao buscar CEP:", error);
      limparCamposEndereco();
      cepInput.classList.remove("processing");
      cepInput.classList.add("cep-error"); // Borda vermelha em caso de erro na requisição
      alert("Erro ao buscar CEP. Tente novamente.");
      enderecoInfoContainer.style.display = "none";
    }
  } else if (cepLimpo.length < 8) {
    // Limpa os campos e esconde a div se o CEP estiver incompleto ou inválido
    limparCamposEndereco();
    enderecoInfoContainer.style.display = "none";
    cepInput.classList.remove("cep-success", "cep-error", "processing");
    if (cepLimpo.length > 0) {
      cepInput.classList.add("cep-incomplete");
    }
  }
}

function preencherCamposEndereco(data) {
  enderecoInput.value = data.logradouro || "";
  bairroInput.value = data.bairro || "";
  cidadeInput.value = data.localidade || "";
  estadoInput.value = data.uf || "";
  dddInput.value = data.ddd || "";
  document.getElementById("complemento").value = data.complemento || ""; // Adicionado complemento
}

function limparCamposEndereco() {
  enderecoInput.value = "";
  bairroInput.value = "";
  cidadeInput.value = "";
  estadoInput.value = "";
  dddInput.value = "";
  document.getElementById("complemento").value = "";
  document.getElementById("numero").value = ""; // Limpa número também
}

// --- Funções do modal "Não sei meu CEP" ---

naoSeiCepLink.addEventListener("click", (e) => {
  e.preventDefault();
  modalNaoSeiCep.style.display = "flex"; // Usar flex para centralizar
  carregarEstados();
});

closeModalButton.addEventListener("click", () => {
  modalNaoSeiCep.style.display = "none";
  limparModalBuscaCep();
});

window.addEventListener("click", (e) => {
  // Fecha o modal se clicar fora do form-box (dentro do container do modal)
  // Verifica se o clique foi no elemento do modal e não em um de seus filhos, exceto o form-box
  const isClickInsideFormBox = modalNaoSeiCep
    .querySelector(".form-box")
    .contains(e.target);
  const isClickOnCloseButton = e.target === closeModalButton;

  if (
    e.target === modalNaoSeiCep ||
    (!isClickInsideFormBox &&
      !isClickOnCloseButton &&
      modalNaoSeiCep.contains(e.target))
  ) {
    modalNaoSeiCep.style.display = "none";
    limparModalBuscaCep();
  }
});

async function carregarEstados() {
  ufSelect.innerHTML = '<option value="">Selecione um estado</option>'; // Limpa opções anteriores
  municipioSelect.innerHTML =
    '<option value="">Selecione um município</option>';
  municipioSelect.disabled = true;
  logradouroInput.disabled = true;
  logradouroSuggestions.innerHTML = "";
  buscarCepEnderecoButton.disabled = true;

  try {
    const response = await fetch(
      "https://servicodados.ibge.gov.br/api/v1/localidades/estados"
    );
    const estados = await response.json();
    estados.sort((a, b) => a.nome.localeCompare(b.nome)); // Ordena por nome

    estados.forEach((estado) => {
      const option = document.createElement("option");
      option.value = estado.sigla;
      option.textContent = estado.nome;
      ufSelect.appendChild(option);
    });
  } catch (error) {
    console.error("Erro ao carregar estados:", error);
    alert("Erro ao carregar lista de estados. Tente novamente.");
  }
}

ufSelect.addEventListener("change", async () => {
  const uf = ufSelect.value;
  municipioSelect.innerHTML =
    '<option value="">Selecione um município</option>';
  municipioSelect.disabled = true;
  logradouroInput.disabled = true;
  logradouroSuggestions.innerHTML = "";
  buscarCepEnderecoButton.disabled = true;

  if (uf) {
    try {
      const response = await fetch(
        `https://servicodados.ibge.gov.br/api/v1/localidades/estados/${uf}/municipios`
      );
      const municipios = await response.json();
      municipios.sort((a, b) => a.nome.localeCompare(b.nome)); // Ordena por nome

      municipios.forEach((municipio) => {
        const option = document.createElement("option");
        option.value = municipio.nome;
        option.textContent = municipio.nome;
        municipioSelect.appendChild(option);
      });
      municipioSelect.disabled = false;
    } catch (error) {
      console.error("Erro ao carregar municípios:", error);
      alert("Erro ao carregar lista de municípios. Tente novamente.");
    }
  }
});

municipioSelect.addEventListener("change", () => {
  if (municipioSelect.value) {
    logradouroInput.disabled = false;
    buscarCepEnderecoButton.disabled = false;
  } else {
    logradouroInput.disabled = true;
    buscarCepEnderecoButton.disabled = true;
    logradouroSuggestions.innerHTML = "";
  }
});

logradouroInput.addEventListener("keyup", () => {
  clearTimeout(typingTimer);
  if (logradouroInput.value.length >= 3) {
    // Começa a sugerir após 3 caracteres
    typingTimer = setTimeout(buscarLogradouros, doneTypingInterval);
  } else {
    logradouroSuggestions.innerHTML = "";
  }
});

async function buscarLogradouros() {
  const uf = ufSelect.value;
  const municipio = municipioSelect.value;
  const logradouroDigitado = logradouroInput.value.trim();

  if (!uf || !municipio || logradouroDigitado.length < 3) {
    logradouroSuggestions.innerHTML = "";
    return;
  }

  try {
    // Codifica o nome do município e logradouro para a URL
    const municipioEncoded = encodeURIComponent(municipio);
    const logradouroEncoded = encodeURIComponent(logradouroDigitado);

    const response = await fetch(
      `https://viacep.com.br/ws/${uf}/${municipioEncoded}/${logradouroEncoded}/json/`
    );
    const data = await response.json();

    logradouroSuggestions.innerHTML = ""; // Limpa sugestões anteriores

    if (data.length > 0 && !data.erro) {
      data.slice(0, 10).forEach((item) => {
        // Limita a 10 sugestões
        const li = document.createElement("li");
        li.textContent = `${item.logradouro}, ${item.bairro} - ${item.cep}`;
        li.dataset.cep = item.cep; // Guarda o CEP para preenchimento
        li.addEventListener("click", () => {
          cepInput.value = item.cep;
          buscarCEP(item.cep); // Preenche o formulário principal
          modalNaoSeiCep.style.display = "none";
          limparModalBuscaCep();
          cepInput.focus(); // Coloca o foco no campo CEP principal
        });
        logradouroSuggestions.appendChild(li);
      });
    } else {
      const li = document.createElement("li");
      li.textContent = "Nenhum logradouro encontrado.";
      logradouroSuggestions.appendChild(li);
    }
  } catch (error) {
    console.error("Erro ao buscar logradouros:", error);
    logradouroSuggestions.innerHTML = "<li>Erro ao buscar logradouros.</li>";
  }
}

buscarCepEnderecoButton.addEventListener("click", async () => {
  // Esta função será para buscar o CEP exato se o usuário não selecionou da lista
  // Basicamente, pegaria o primeiro resultado da busca por logradouro
  const uf = ufSelect.value;
  const municipio = municipioSelect.value;
  const logradouroDigitado = logradouroInput.value.trim();

  if (!uf || !municipio || logradouroDigitado.length < 3) {
    alert(
      "Por favor, selecione o estado, município e digite pelo menos 3 caracteres do logradouro."
    );
    return;
  }

  try {
    const municipioEncoded = encodeURIComponent(municipio);
    const logradouroEncoded = encodeURIComponent(logradouroDigitado);
    const response = await fetch(
      `https://viacep.com.br/ws/${uf}/${municipioEncoded}/${logradouroEncoded}/json/`
    );
    const data = await await response.json();

    if (data.length > 0 && !data.erro) {
      // Preenche o campo CEP principal com o primeiro resultado encontrado
      cepInput.value = data[0].cep;
      buscarCEP(data[0].cep); // Preenche o formulário principal
      modalNaoSeiCep.style.display = "none";
      limparModalBuscaCep();
      cepInput.focus();
    } else {
      alert("CEP não encontrado para o endereço informado.");
    }
  } catch (error) {
    console.error("Erro ao buscar CEP por endereço:", error);
    alert("Erro ao buscar CEP por endereço. Tente novamente.");
  }
});

function limparModalBuscaCep() {
  ufSelect.innerHTML = '<option value="">Selecione um estado</option>';
  municipioSelect.innerHTML =
    '<option value="">Selecione um município</option>';
  municipioSelect.disabled = true;
  logradouroInput.value = "";
  logradouroInput.disabled = true;
  logradouroSuggestions.innerHTML = "";
  buscarCepEnderecoButton.disabled = true;
}

function emailValido(email) {
  const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return regex.test(email);
}


// --- Código existente para o botão de cadastro ---

document.querySelector(".cadastrar").addEventListener("click", () => {
  const nome = document.getElementById("nome").value.trim();
  const sobrenome = document.getElementById("sobrenome").value.trim();
  const email = document.getElementById("email").value.trim();
  const senha = document.getElementById("senha").value;
  const confirmar = document.getElementById("confirmar").value;

  const idUsuario = document.getElementById("idUsuario").value.trim();
  const ddd = document.getElementById("ddd").value.trim();
  const telefone = document.getElementById("telefone").value.trim();
  const endereco = document.getElementById("endereco").value.trim();
  const numero = document.getElementById("numero").value.trim();
  const complemento = document.getElementById("complemento").value.trim();
  const bairro = document.getElementById("bairro").value.trim();
  const cidade = document.getElementById("cidade").value.trim();
  const estado = document.getElementById("estado").value.trim();
  const cep = document.getElementById("cep").value.trim();

  if (!nome || !sobrenome || !email || !senha || !confirmar) {
    alert("Preencha todos os campos obrigatórios.");
    return;
  }

  if (!emailValido(email)) {
  alert("Por favor, insira um email válido.");
  return;
}

  if ((!ddd || ddd.length != 2) && (telefone)) {
  alert("O DDD e o telefone precisam ser válidos.");
  return;
}

  if (!estado || !cidade || !bairro) {
  alert("Por favor, insira um CEP válido.");
  return;
}

  if (senha !== confirmar) {
    alert("As senhas não coincidem.");
    return;
  }

  const dados = {
    idUsuario: idUsuario,
    nome: nome,
    sobrenome: sobrenome,
    email: email,
    ddd: ddd,
    telefone: telefone,
    endereco: endereco,
    complemento: complemento, // Adicionado
    numero: numero, // Adicionado
    bairro: bairro,
    cidade: cidade,
    estado: estado,
    cep: cep,
    senha: senha,
    confirmar: confirmar,
  };

  fetch("/cadastrar", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(dados),
  })
    .then((res) => res.json())
    .then((data) => {
      alert(data.mensagem);
    })
    .catch((err) => {
      alert("Erro na requisição");
    });
});
