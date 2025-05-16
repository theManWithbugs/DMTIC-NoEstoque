function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

fetch('/new_filtro/')
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        let unidades = [];
        let departamentos = [];
        let divisoes = [];

        let unidadeSelecionadaValor = null; 
        let departamentoSelecionadoValor = null; 
        let divisaoSelecionadaValor = null; 

        data.unidades.forEach(unidade => {
            unidades.push({ id: unidade.id, nome: unidade.unidade });
        });

        data.departamentos.forEach(departamento => {
            departamentos.push({ id: departamento.id, nome: departamento.nome, unidade: departamento.unidade });
        });

        data.divisoes.forEach(divisao => {
            divisoes.push({ id: divisao.id, nome: divisao.nome, departamento: divisao.departamento });
        });

        const selectUnidade = document.getElementById('select');
        unidades.forEach(unidade => {
            const option = document.createElement('option');
            option.value = unidade.id;
            option.textContent = unidade.nome;
            selectUnidade.appendChild(option);
        });

        selectUnidade.addEventListener('change', function () {
            unidadeSelecionadaValor = selectUnidade.value;

            const selectDepartamento = document.getElementById('select_depar');
            selectDepartamento.innerHTML = '<option value="">Selecione</option>'; 

            departamentos.forEach(departamento => {
                if (departamento.unidade == unidadeSelecionadaValor) {
                    const option = document.createElement('option');
                    option.value = departamento.id;
                    option.textContent = departamento.nome;
                    selectDepartamento.appendChild(option);
                }
            });
        });

        const selectDepartamento = document.getElementById('select_depar');
        selectDepartamento.addEventListener('change', function () {
            departamentoSelecionadoValor = selectDepartamento.value;

            const selectDivisao = document.getElementById('select_divi');
            selectDivisao.innerHTML = '<option value="">Selecione</option>'; 

            divisoes.forEach(divisao => {
                if (divisao.departamento == departamentoSelecionadoValor) {
                    const option = document.createElement('option');
                    option.value = divisao.id;
                    option.textContent = divisao.nome;
                    selectDivisao.appendChild(option);
                }
            });
        });
        const selectDivisao = document.getElementById('select_divi');
        selectDivisao.addEventListener('change', function () {
            divisaoSelecionadaValor = selectDivisao.value;
        });

        // Adiciona evento ao botão para enviar os dados
        const enviarButton = document.getElementById('enviar');
        enviarButton.addEventListener('click', function () {
            //Pega os valores atuais dos selects, mesmo que o usuário não tenha alterado
            // unidadeSelecionadaValor = selectUnidade.value || "";
            // departamentoSelecionadoValor = selectDepartamento.value || "";
            // divisaoSelecionadaValor = selectDivisao.value || "";

            const dados = {
                unidadeSelecionadaValor,
                departamentoSelecionadoValor,
                divisaoSelecionadaValor,
            };

            fetch('/filtrojs/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken,
                },
                body: JSON.stringify(dados)
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Erro ao enviar os dados');
                }
                return response.json();
            })
            .then(data => {
                console.log('Resposta ao backend', data);
            })
            .catch(error => console.error('Erro:', error));
        });
    })
    .catch(error => console.error('Erro ao receber os dados:', error));