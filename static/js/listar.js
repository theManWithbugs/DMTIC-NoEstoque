
function exibir() {
    caixa = document.getElementById('box_words');
    button = document.getElementById('btn_exibir');

    caixa.style.display = 'block';
    caixa.style.background = 'white';
    caixa.style.padding = '6px';
    caixa.style.borderRadius = '5px';
}

function ocultar() {
    caixa = document.getElementById('box_words');
    button = document.getElementById('btn_exibir');

    caixa.style.display = 'none';
}