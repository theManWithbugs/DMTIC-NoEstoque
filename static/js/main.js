unidade_el = document.getElementById('add_unidade');
function reg_unidade() {
    unidade_el.style = `display: block; background-color: white; border-radius: 5px; 
    align-items: center; justify-content: center; display: flex; padding: 20px;`;
    unidade_el.classList.add('animate__animated', 'animate__bounceInLeft');

    departamento_el.style = 'display: none';
    divisao_el.style = 'display: none';
}

departamento_el = document.getElementById('add_departamento');
function reg_departmento() {
    departamento_el.style = `display: block; background-color: white; border-radius: 5px; 
    align-items: center; justify-content: center; display: flex; padding: 20px;`;
    departamento_el.classList.add('animate__animated', 'animate__bounceInLeft');

    unidade_el.style = 'display: none';
    divisao_el.style = 'display: none';
}

divisao_el = document.getElementById('add_divisao');

function reg_divisao() {
    divisao_el.style = `display: block; background-color: white; border-radius: 5px; 
    align-items: center; justify-content: center; display: flex; padding: 20px;`;
    divisao_el.classList.add('animate__animated', 'animate__bounceInLeft');

    unidade_el.style = 'display: none;';
    departamento_el.style = 'display: none;';
}

document.addEventListener('DOMContentLoaded', function() {
    const switchInput = document.getElementById('switch');
    const navbar = document.getElementById('navbar');
    const title = document.getElementById('title_nav');
    const footer = document.getElementById('footer_ele');
    const footer_text = document.getElementById('footer_text');

    function tema_claro() {
        navbar.classList.remove('bg-dark');
        navbar.classList.add('bg-white');

            title.classList.remove('text-white');
            title.classList.add('text-dark');

            footer.classList.remove('bg-dark');
            footer.classList.add('bg-white');

        footer_text.classList.remove('text-white');
        footer_text.classList.add('text-dark');
    }

    function tema_escuro() {
        navbar.classList.remove('bg-white');
        navbar.classList.add('bg-dark');

            title.classList.remove('text-dark')
            title.classList.add('text-white')

            footer.classList.remove('bg-white');
            footer.classList.add('bg-dark');

        footer_text.classList.remove('text-dark');
        footer_text.classList.add('text-white');
    }
    
    // Atualiza o tema e salva a preferência
    switchInput.addEventListener('change', function() {
        if (this.checked) {
            tema_claro();
            salvarTema('claro');
        } else {
            tema_escuro();
            salvarTema('escuro');
        }
    });

    function salvarTema(tema) {
        localStorage.setItem('tema', tema);
    }

    function aplicarTemaSalvo() {
        const temaSalvo = localStorage.getItem('tema');
        if (temaSalvo === 'claro') {
            switchInput.checked = true;
            tema_claro();
        } else if (temaSalvo === 'escuro') {
            switchInput.checked = false;
            tema_escuro();
        }
    }

    aplicarTemaSalvo();
});

