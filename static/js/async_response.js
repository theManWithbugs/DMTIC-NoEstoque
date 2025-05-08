console.log("I'm working!");

async function teste_async (btn_teste) {
    try {
        const response = await fetch(`/home/async_view_teste/?btn=${btn_teste}`);
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const dados = await response.json();

        const caixa = document.querySelector('#caixa');

        // dados.forEach(element => {
        //     const newElement = document.createElement('p');
        //     newElement.innerHTML = element;
        //     caixa.appendChild(newElement);
        // });

        const newElement = document.createElement('p');
        newElement.innerHTML = dados;
        caixa.appendChild(newElement);

        // if (newElement != null) {
        //     console.log('Definido!');
        // } else {
        //     console.log('Não Definido!');
        // }

    } catch (error) {
        console.log('Ocorreu um erro ao realizar o fetch!')
    }

}