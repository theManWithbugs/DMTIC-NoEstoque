let dados_unidade;
let dados_departamentos;

async function items_info(btn_items) {
    try {
        const response = await fetch(`/home/async_items/?btn=${btn_items}`);
        if (!response.ok) {
            throw new Error("Network response was not ok in items fetch");
        }
        const items = await response.json();

        console.log(items);

        const caixa = document.getElementById('caixa');
        caixa.style = 'border: solid 3px lightblue; padding: 10px; border-radius: 5px; background-color: white;';

        // Adding a title before the list
        const title = document.createElement('h4');
        title.textContent = 'Todos os items (items iguais agrupados)';
        title.style = 'margin-bottom: 10px; text-align: center; padding: 10px;';

        const lista = document.createElement('ul');

        Object.entries(items).forEach(([key, value]) => {
            const item = document.createElement('li');
            item.style = 'font-size: 16px; margin-top: 5px;';
            item.textContent = `${key}: ${value}`;
            caixa.classList.add('animate__animated', 'animate__fadeInLeft', 'animate__delay-1s');
            lista.appendChild(item);
        });

        Object.entries(items).forEach(([key, value]) => {
            const divisionMatch = key.match(/Divisão: ([^\]]+)/);
            const departamentoMatch = key.match(/Departamento: ([^\]]+)/);
            const division = divisionMatch ? divisionMatch[1]: "Divisão não encontrada";
        });

        caixa.innerHTML = "";
        caixa.appendChild(title);
        caixa.appendChild(lista);

    } catch (error) {
        console.log('There was an error fetching the items:', error);
    }
}

async function materiais_info(btn_mate) {
    try {
        const response = await fetch(`/home/async_mater/?btn=${btn_mate}`);
        if (!response.ok) {
            throw new Error("Network response was not ok in items fetch");
        }
        const data = await response.json();
        
        const caixa = document.getElementById('caixa_two')
        caixa.style = 'border: solid 3px lightblue; padding: 40px; border-radius: 5px; background-color: white;';
        const title = document.createElement('h4');
        title.textContent = 'Agrupados por divisão';
        title.style = 'margin-bottom: 10px; text-align: center; padding: 10px;';

        caixa.innerText = "";

        caixa.appendChild(title);
        data.forEach(divisaoObj => {
            const divis_nome = document.createElement('h5');
            caixa.appendChild(divis_nome);
            divis_nome.innerText = divisaoObj.divisao
            divisaoObj.itens.forEach(item => {
                const p = document.createElement('p');
                p.textContent = `Item: ${item.modelo} Localidade: ${item.saida_obj}`;
                caixa.appendChild(p);
            });
        });
        caixa.classList.add('animate__animated', 'animate__fadeInLeft', 'animate__delay-1s');

    } catch (error) {
        console.log('There was an error fetching materiais_info:', error);
    }
}

