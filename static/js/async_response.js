let dados_unidade;
let dados_departamentos;

function all_func() {
    items_info()
}

// async function teste_async(btn_teste) {
//     try {
//         const response = await fetch(`/home/async_view_teste/?btn=${btn_teste}`);
//         if (!response.ok) {
//             throw new Error('Network response was not ok');
//         }
//         dados_unidades = await response.json();

//     } catch (error) {
//         console.log('Ocorreu um erro ao realizar o fetch!')
//     }
// }

// function exibirDados() {
//     setTimeout(() => {
//         if (dados_unidades !== null && typeof dados_unidades === 'object' && Object.keys(dados_unidades).length > 0) {
//             console.log("Dados válidos:", dados_unidades);

//             const caixa = document.querySelector('#caixa_html');

//             // Remove existing paragraphs to avoid duplication
//             caixa.innerHTML = '';

//             // Iterate over the dictionary and create a paragraph for each key-value pair
//             for (const [key, value] of Object.entries(dados_unidades)) {
//                 const newElement = document.createElement('div');
//                 newElement.innerHTML = 
//                 `<table>
//                     <tbody>
//                         <tr>
//                             <td>${key}</td>
//                             <td>${value}</td>
//                         </tr>
//                     </tbody>
//                 </table>`;
//                 newElement.classList.add('caixa', 'animate__animated', 'animate__fadeInLeft');
//                 caixa.appendChild(newElement);
//             }
//         } else {
//             console.log("Dados inválidos ou não carregados ainda.");
//         }
//     }, 100);
// }

// async function teste_async_two(btn_teste_two) {
//     try {
//         const response = await fetch(`/home/async_view_two/?btn=${btn_teste_two}`);
//         if (!response.ok) {
//             throw new Error("Network response was not ok in the second fetch")
//         }
//         dados_departamentos = await response.json();
//         console.log(dados_departamentos);

//     } catch (error) {
//             console.log('Ocorreu um erro ao realizar segundo fetch!')
//     }
// }

// function exibirDadosTwo() {
//     setTimeout(() => {
//         if (dados_departamentos !== null && typeof dados_departamentos === 'object' && Object.keys(dados_departamentos).length > 0) {
            
//             const caixa_two = document.querySelector('caixa_html2');

//             caixa_two.innerHTML = '';

//             for (const [key, value] of Object.entries(dados_departamentos)) {
//                 const newElementTwo = document.createElement('div');
//                 newElementTwo.innerHTML = 
//                 `
//                 <table>
//                     <tbody>
//                         <tr>
//                             <td>${key}</td>
//                             <td>${value}</td>
//                         </tr>
//                     </tbody>
//                 </table>`;
//                 newElementTwo.classList.add('caixa', 'animate__animated', 'animate__fadeInLeft');
//                 caixa_two.appendChild(newElementTwo);
//             }

//         } else {
//             console.log("Dados inválidos ou não carregados ainda. 2");
//         }
//     }, 100)
// }

async function items_info(btn_items) {
    try {
        const response = await fetch(`/home/async_items/?btn=${btn_items}`);
        if (!response.ok) {
            throw new Error("Network response was not ok in items fetch");
        }
        const items = await response.json();

        console.log(items);

        const caixa = document.getElementById('caixa');
        caixa.style = 'border: solid 1px; padding: 10px; border-radius: 5px;';

        // Adding a title before the list
        const title = document.createElement('h4');
        title.textContent = 'Lista de items';
        title.style = 'margin-bottom: 10px;';

        const lista = document.createElement('ul');

        Object.entries(items).forEach(([key, value]) => {
            const item = document.createElement('li');
            item.style = 'font-size: 16px;';
            item.textContent = `${key}: ${value}`;
            caixa.classList.add('animate__animated', 'animate__fadeInLeft');
            lista.appendChild(item);
        });

        caixa.innerHTML = "";
        caixa.appendChild(title);
        caixa.appendChild(lista);

    } catch (error) {
        console.log('There was an error fetching the items:', error);
    }
}






