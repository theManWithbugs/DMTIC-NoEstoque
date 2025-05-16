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

fetch('/new_filtro_json/')
    .then(response => response.json())
    .then(data => {
        unidades = data.unidades;
        departamentos = data.departamentos;
        divisoes = data.divisoes;

        lista_unidades = [];
        lista_departamentos = [];
        lista_divisoes = [];

        divisoes.forEach(divisao => {
            lista_divisoes.push({ id: divisao.id, nome: divisao.nome });
        });

        unidades.forEach(unidade => {
            lista_unidades.push({ id: unidade.id, nome: unidade.unidade});
        });

        departamentos.forEach(departamento => {
            lista_departamentos.push({ id: departamento.unidade, nome: departamento.nome });
        });

        const caixa_items = document.getElementById('caixa_items');
        caixa_items.style = 'background-color: white; padding: 20px; border-radius: 5px; width: 480px; margin-left: auto; margin-right: auto; text-align: center;';

        const span_item = document.getElementById('span');
            const title = document.createElement('h4');
            title.textContent = 'Criar saida de objeto';
        span_item.appendChild(title);

        const caixa_unidade = document.getElementById('caixa_unidade');
        const select_unidade = document.createElement('select');
        
        option_default = document.createElement('option');
            option_default.innerHTML = 'Selecione';
            select_unidade.appendChild(option_default);
        select_unidade.style = 'width: 190px;';

        lista_unidades.forEach(unidade => {
            const option_unidade = document.createElement('option');
            option_unidade.value = unidade.id;
            option_unidade.textContent = unidade.nome;
            select_unidade.appendChild(option_unidade);
        });
        caixa_unidade.appendChild(select_unidade);

        const caixa_dep = document.getElementById('caixa_dep');
            const select_dep = document.createElement('select');
                caixa_dep.appendChild(select_dep);
                const caixa_divis = document.getElementById('caixa_divis');
            const select_divis = document.createElement('select');
        caixa_divis.appendChild(select_divis);

        select_unidade.addEventListener('change', function () {
            unidade_selecionada = select_unidade.value;
            select_dep.style = 'width: 190px;';
            select_dep.innerHTML = '';

            option_default = document.createElement('option');
            option_default.innerHTML = 'Selecione';
            select_dep.appendChild(option_default);
            // Criação de opções já filtradas
            lista_departamentos.forEach(departamento => {
                if (unidade_selecionada == departamento.id) {
                    const option_dep = document.createElement('option');
                    option_dep.value = departamento.id;
                    option_dep.textContent = departamento.nome;
                    select_dep.appendChild(option_dep);
                    // Create div_selecionada variable with the selected division value
                }
            });
        });

        select_dep.addEventListener('change', function () {
            dep_selecionado = select_dep.value;
            select_divis.style = 'width: 190px;';
            select_divis.innerHTML = '';

            option_default = document.createElement('option');
            option_default.innerHTML = 'Selecione';
            select_divis.appendChild(option_default)

            lista_divisoes.forEach(divisao => {
                if (dep_selecionado == divisao.id) {
                    const option_divis = document.createElement('option');
                    option_divis.value = divisao.id
                    option_divis.textContent = divisao.nome;
                    select_divis.appendChild(option_divis);
                }
            });
        });

        select_dep.addEventListener('change', function () {
            let first_var = false;
            if (select_unidade.value.includes(select_dep.value)) {
                first_var = true;
            } else {
                first_var = false;
            }

            select_divis.addEventListener('change', function () {
                let second_var = false;
                if (select_dep.value.includes(select_divis.value)) {
                    second_var = true;
                } else {
                    second_var = false;
                }

                caixa_btn = document.getElementById('caixa_btn');
                // Check if the button already exists before creating
                if (first_var && second_var === true && !document.getElementById('btn_enviar')) {
                    btn_enviar = document.createElement('button');
                    btn_enviar.textContent = 'Enviar';
                    btn_enviar.style = 'padding: 3px; margin-top: 7px;';
                    btn_enviar.type = 'submit';
                    btn_enviar.setAttribute('id', 'input_process'); // Set an id to identify the button
                    btn_enviar.onclick = enviar_dados;
                    caixa_btn.appendChild(btn_enviar);

                    dados = { 
                        unidade: select_unidade.value, 
                        departamento: select_dep.value, 
                        divisao: select_divis.value,
                    };
                      
                    function enviar_dados() {
                        fetch('/salvar_saida/', {
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
                        .then(dados => {
                            console.log('Resposta ao backend', dados);
                        })
                        .catch(error => console.error('Erro:', error));
                    }
                }
            });
        });

    })
    .catch(error => console.error('Error ao receber os dados:', error));