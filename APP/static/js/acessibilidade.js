// JavaScript específico para funcionalidades de acessibilidade

// Função para alternar leitor de tela (simulação)
function toggleScreenReader() {
    const isActive = document.body.classList.toggle('screen-reader-active');
    
    if (isActive) {
        announceToScreenReader('Modo leitor de tela ativado. Navegue usando Tab e Enter.');
        // Adicionar mais anúncios automáticos
        enableScreenReaderMode();
    } else {
        announceToScreenReader('Modo leitor de tela desativado.');
        disableScreenReaderMode();
    }
    
    localStorage.setItem('screenReaderMode', isActive);
}

// Ativar modo leitor de tela
function enableScreenReaderMode() {
    // Anunciar elementos quando recebem foco
    document.addEventListener('focusin', announceElement);
    
    // Anunciar mudanças de página
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.type === 'childList' && mutation.addedNodes.length > 0) {
                announceToScreenReader('Conteúdo da página foi atualizado.');
            }
        });
    });
    
    observer.observe(document.body, {
        childList: true,
        subtree: true
    });
}

// Desativar modo leitor de tela
function disableScreenReaderMode() {
    document.removeEventListener('focusin', announceElement);
}

// Anunciar elemento focado
function announceElement(event) {
    const element = event.target;
    let announcement = '';
    
    if (element.tagName === 'A') {
        announcement = `Link: ${element.textContent || element.getAttribute('aria-label')}`;
    } else if (element.tagName === 'BUTTON') {
        announcement = `Botão: ${element.textContent || element.getAttribute('aria-label')}`;
    } else if (element.tagName === 'INPUT') {
        const label = document.querySelector(`label[for="${element.id}"]`);
        const labelText = label ? label.textContent : element.getAttribute('aria-label') || element.placeholder;
        announcement = `Campo de entrada: ${labelText}`;
    } else if (element.tagName === 'TEXTAREA') {
        const label = document.querySelector(`label[for="${element.id}"]`);
        const labelText = label ? label.textContent : element.getAttribute('aria-label') || element.placeholder;
        announcement = `Área de texto: ${labelText}`;
    } else if (element.tagName === 'SELECT') {
        const label = document.querySelector(`label[for="${element.id}"]`);
        const labelText = label ? label.textContent : element.getAttribute('aria-label');
        announcement = `Lista de seleção: ${labelText}`;
    } else if (element.getAttribute('role') === 'button') {
        announcement = `Botão: ${element.textContent || element.getAttribute('aria-label')}`;
    }
    
    if (announcement) {
        announceToScreenReader(announcement);
    }
}

// Função melhorada para anúncios
function announceToScreenReader(message) {
    // Remove anúncios anteriores
    const existingAnnouncements = document.querySelectorAll('.sr-announcement');
    existingAnnouncements.forEach(el => el.remove());
    
    // Cria novo anúncio
    const announcement = document.createElement('div');
    announcement.className = 'sr-announcement';
    announcement.setAttribute('aria-live', 'polite');
    announcement.setAttribute('aria-atomic', 'true');
    announcement.style.position = 'absolute';
    announcement.style.left = '-10000px';
    announcement.style.width = '1px';
    announcement.style.height = '1px';
    announcement.style.overflow = 'hidden';
    announcement.textContent = message;
    
    document.body.appendChild(announcement);
    
    // Remove após 3 segundos
    setTimeout(() => {
        if (announcement.parentNode) {
            announcement.parentNode.removeChild(announcement);
        }
    }, 3000);
}

// Navegação por teclas de atalho
document.addEventListener('keydown', function(e) {
    // Alt + 1: Ir para o conteúdo principal
    if (e.altKey && e.key === '1') {
        e.preventDefault();
        const mainContent = document.getElementById('main-content') || document.querySelector('main');
        if (mainContent) {
            mainContent.focus();
            mainContent.scrollIntoView({ behavior: 'smooth' });
            announceToScreenReader('Navegando para o conteúdo principal.');
        }
    }
    
    // Alt + 2: Ir para o menu de navegação
    if (e.altKey && e.key === '2') {
        e.preventDefault();
        const nav = document.querySelector('nav');
        if (nav) {
            const firstLink = nav.querySelector('a');
            if (firstLink) {
                firstLink.focus();
                announceToScreenReader('Navegando para o menu principal.');
            }
        }
    }
    
    // Alt + 3: Ir para o formulário de contato
    if (e.altKey && e.key === '3') {
        e.preventDefault();
        const contactForm = document.querySelector('#contact form');
        if (contactForm) {
            const firstInput = contactForm.querySelector('input, textarea');
            if (firstInput) {
                firstInput.focus();
                contactForm.scrollIntoView({ behavior: 'smooth' });
                announceToScreenReader('Navegando para o formulário de contato.');
            }
        }
    }
    
    // Alt + 4: Ir para o rodapé
    if (e.altKey && e.key === '4') {
        e.preventDefault();
        const footer = document.querySelector('footer');
        if (footer) {
            footer.focus();
            footer.scrollIntoView({ behavior: 'smooth' });
            announceToScreenReader('Navegando para o rodapé.');
        }
    }
    
    // Ctrl + Alt + H: Mostrar atalhos de teclado
    if (e.ctrlKey && e.altKey && e.key === 'h') {
        e.preventDefault();
        showKeyboardShortcuts();
    }
});

// Mostrar atalhos de teclado
function showKeyboardShortcuts() {
    const shortcuts = `
    Atalhos de Teclado Disponíveis:
    
    Alt + 1: Ir para o conteúdo principal
    Alt + 2: Ir para o menu de navegação
    Alt + 3: Ir para o formulário de contato
    Alt + 4: Ir para o rodapé
    
    Tab: Navegar para o próximo elemento
    Shift + Tab: Navegar para o elemento anterior
    Enter/Space: Ativar links e botões
    Esc: Voltar ao topo da página
    
    Ctrl + Alt + H: Mostrar esta lista de atalhos
    `;
    
    alert(shortcuts);
    announceToScreenReader('Lista de atalhos de teclado exibida.');
}

// Detectar preferências do usuário
function detectUserPreferences() {
    // Verificar se o usuário prefere movimento reduzido
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
        document.body.classList.add('reduced-motion');
        announceToScreenReader('Modo de movimento reduzido detectado e ativado.');
    }
    
    // Verificar se o usuário prefere alto contraste
    if (window.matchMedia('(prefers-contrast: high)').matches) {
        document.body.classList.add('high-contrast');
        announceToScreenReader('Modo de alto contraste detectado e ativado.');
    }
    
    // Verificar se o usuário prefere esquema de cores escuro
    if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
        document.body.classList.add('dark-mode');
        announceToScreenReader('Modo escuro detectado.');
    }
}

// Monitorar mudanças nas preferências
function monitorPreferences() {
    // Monitorar mudanças na preferência de movimento
    window.matchMedia('(prefers-reduced-motion: reduce)').addEventListener('change', function(e) {
        if (e.matches) {
            document.body.classList.add('reduced-motion');
            announceToScreenReader('Modo de movimento reduzido ativado.');
        } else {
            document.body.classList.remove('reduced-motion');
            announceToScreenReader('Modo de movimento reduzido desativado.');
        }
    });
    
    // Monitorar mudanças na preferência de contraste
    window.matchMedia('(prefers-contrast: high)').addEventListener('change', function(e) {
        if (e.matches) {
            document.body.classList.add('high-contrast');
            announceToScreenReader('Modo de alto contraste ativado.');
        } else {
            document.body.classList.remove('high-contrast');
            announceToScreenReader('Modo de alto contraste desativado.');
        }
    });
}

// Validação de formulário acessível
function setupAccessibleFormValidation() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        const inputs = form.querySelectorAll('input, textarea, select');
        
        inputs.forEach(input => {
            // Validação em tempo real
            input.addEventListener('blur', function() {
                validateField(this);
            });
            
            // Limpar erro quando o usuário começar a digitar
            input.addEventListener('input', function() {
                clearFieldError(this);
            });
        });
        
        // Validação no envio
        form.addEventListener('submit', function(e) {
            let isValid = true;
            
            inputs.forEach(input => {
                if (!validateField(input)) {
                    isValid = false;
                }
            });
            
            if (!isValid) {
                e.preventDefault();
                const firstError = form.querySelector('.field-error');
                if (firstError) {
                    const field = firstError.previousElementSibling;
                    field.focus();
                    announceToScreenReader('Formulário contém erros. Por favor, corrija os campos destacados.');
                }
            }
        });
    });
}

// Validar campo individual
function validateField(field) {
    const value = field.value.trim();
    const isRequired = field.hasAttribute('required');
    let isValid = true;
    let errorMessage = '';
    
    // Limpar erro anterior
    clearFieldError(field);
    
    // Verificar se campo obrigatório está vazio
    if (isRequired && !value) {
        isValid = false;
        errorMessage = 'Este campo é obrigatório.';
    }
    
    // Validação específica por tipo
    if (value && field.type === 'email') {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(value)) {
            isValid = false;
            errorMessage = 'Por favor, insira um email válido.';
        }
    }
    
    // Mostrar erro se inválido
    if (!isValid) {
        showFieldError(field, errorMessage);
    }
    
    return isValid;
}

// Mostrar erro do campo
function showFieldError(field, message) {
    const errorElement = document.createElement('div');
    errorElement.className = 'field-error';
    errorElement.textContent = message;
    errorElement.setAttribute('role', 'alert');
    errorElement.style.color = '#d32f2f';
    errorElement.style.fontSize = '0.9rem';
    errorElement.style.marginTop = '5px';
    
    field.parentNode.appendChild(errorElement);
    field.setAttribute('aria-invalid', 'true');
    field.setAttribute('aria-describedby', field.id + '-error');
    errorElement.id = field.id + '-error';
    
    announceToScreenReader(`Erro no campo ${field.getAttribute('aria-label') || field.placeholder}: ${message}`);
}

// Limpar erro do campo
function clearFieldError(field) {
    const errorElement = field.parentNode.querySelector('.field-error');
    if (errorElement) {
        errorElement.remove();
    }
    field.removeAttribute('aria-invalid');
    field.removeAttribute('aria-describedby');
}

// Inicializar funcionalidades de acessibilidade
document.addEventListener('DOMContentLoaded', function() {
    // Carregar preferências salvas
    if (localStorage.getItem('screenReaderMode') === 'true') {
        document.body.classList.add('screen-reader-active');
        enableScreenReaderMode();
    }
    
    // Detectar e monitorar preferências do usuário
    detectUserPreferences();
    monitorPreferences();
    
    // Configurar validação acessível de formulários
    setupAccessibleFormValidation();
    
    // Anunciar que a página foi carregada
    setTimeout(() => {
        announceToScreenReader('Página carregada. Use Tab para navegar ou Alt + H para ver atalhos de teclado.');
    }, 1000);
});

// Função para criar um tour guiado acessível
function startAccessibilityTour() {
    const tourSteps = [
        {
            element: 'header nav',
            message: 'Este é o menu principal. Use Tab para navegar entre os links.'
        },
        {
            element: 'main',
            message: 'Esta é a área de conteúdo principal da página.'
        },
        {
            element: '.accessibility-toolbar',
            message: 'Esta é a barra de ferramentas de acessibilidade. Aqui você pode ajustar fonte e contraste.'
        },
        {
            element: 'footer',
            message: 'Este é o rodapé da página com informações adicionais.'
        }
    ];
    
    let currentStep = 0;
    
    function showStep(stepIndex) {
        if (stepIndex >= tourSteps.length) {
            announceToScreenReader('Tour de acessibilidade concluído.');
            return;
        }
        
        const step = tourSteps[stepIndex];
        const element = document.querySelector(step.element);
        
        if (element) {
            element.scrollIntoView({ behavior: 'smooth', block: 'center' });
            element.focus();
            announceToScreenReader(step.message);
            
            setTimeout(() => {
                showStep(stepIndex + 1);
            }, 3000);
        }
    }
    
    announceToScreenReader('Iniciando tour de acessibilidade. O tour irá destacar as principais áreas da página.');
    showStep(0);
}

// Exportar funções para uso global
window.toggleScreenReader = toggleScreenReader;
window.startAccessibilityTour = startAccessibilityTour;
window.announceToScreenReader = announceToScreenReader;
