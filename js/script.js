// JavaScript para funcionalidades do site de Libras

// Navegação suave
document.addEventListener('DOMContentLoaded', function() {
    // Navegação suave para links internos
    const links = document.querySelectorAll('a[href^="#"]');
    
    links.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            const targetSection = document.querySelector(targetId);
            
            if (targetSection) {
                const headerHeight = document.querySelector('header').offsetHeight;
                const targetPosition = targetSection.offsetTop - headerHeight - 20;
                
                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });
    
    // Formulário de contato
    const contactForm = document.querySelector('#contact form');
    
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Validação básica
            const name = document.getElementById('name').value.trim();
            const email = document.getElementById('email').value.trim();
            const message = document.getElementById('message').value.trim();
            
            if (!name || !email || !message) {
                alert('Por favor, preencha todos os campos obrigatórios.');
                return;
            }
            
            // Validação de email
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(email)) {
                alert('Por favor, insira um email válido.');
                return;
            }
            
            // Simular envio do formulário
            alert('Mensagem enviada com sucesso! Entraremos em contato em breve.');
            contactForm.reset();
        });
    }
    
    // Animação de entrada para elementos
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);
    
    // Observar elementos para animação
    const animatedElements = document.querySelectorAll('.course-item, .feature');
    animatedElements.forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(el);
    });
    
    // Melhorar acessibilidade do teclado
    document.addEventListener('keydown', function(e) {
        // Esc para fechar modais ou voltar ao topo
        if (e.key === 'Escape') {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }
        
        // Enter e Space para ativar links e botões
        if ((e.key === 'Enter' || e.key === ' ') && e.target.tagName === 'A') {
            e.target.click();
        }
    });
    
    // Indicador de foco melhorado
    document.addEventListener('focusin', function(e) {
        if (e.target.matches('a, button, input, textarea, select')) {
            e.target.setAttribute('data-focus-visible', 'true');
        }
    });
    
    document.addEventListener('focusout', function(e) {
        e.target.removeAttribute('data-focus-visible');
    });
    
    // Detectar navegação por teclado vs mouse
    let isUsingKeyboard = false;
    
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Tab') {
            isUsingKeyboard = true;
            document.body.classList.add('keyboard-navigation');
        }
    });
    
    document.addEventListener('mousedown', function() {
        isUsingKeyboard = false;
        document.body.classList.remove('keyboard-navigation');
    });
    
    // Anúncio para leitores de tela
    function announceToScreenReader(message) {
        const announcement = document.createElement('div');
        announcement.setAttribute('aria-live', 'polite');
        announcement.setAttribute('aria-atomic', 'true');
        announcement.style.position = 'absolute';
        announcement.style.left = '-10000px';
        announcement.style.width = '1px';
        announcement.style.height = '1px';
        announcement.style.overflow = 'hidden';
        announcement.textContent = message;
        
        document.body.appendChild(announcement);
        
        setTimeout(() => {
            document.body.removeChild(announcement);
        }, 1000);
    }
    
    // Anunciar mudanças de seção
    const sections = document.querySelectorAll('section[id]');
    const sectionObserver = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const sectionTitle = entry.target.querySelector('h1, h2');
                if (sectionTitle) {
                    announceToScreenReader(`Seção: ${sectionTitle.textContent}`);
                }
            }
        });
    }, { threshold: 0.5 });
    
    sections.forEach(section => {
        sectionObserver.observe(section);
    });
});

// Função para alternar alto contraste (pode ser ativada por botão)
function toggleHighContrast() {
    document.body.classList.toggle('high-contrast');
    const isHighContrast = document.body.classList.contains('high-contrast');
    localStorage.setItem('highContrast', isHighContrast);
}

// Carregar preferência de alto contraste
if (localStorage.getItem('highContrast') === 'true') {
    document.body.classList.add('high-contrast');
}

// Função para aumentar/diminuir fonte
function adjustFontSize(action) {
    const root = document.documentElement;
    const currentSize = parseFloat(getComputedStyle(root).fontSize);
    
    let newSize;
    if (action === 'increase') {
        newSize = Math.min(currentSize * 1.1, 24);
    } else if (action === 'decrease') {
        newSize = Math.max(currentSize * 0.9, 12);
    } else {
        newSize = 16; // reset
    }
    
    root.style.fontSize = newSize + 'px';
    localStorage.setItem('fontSize', newSize);
}

// Carregar preferência de tamanho de fonte
const savedFontSize = localStorage.getItem('fontSize');
if (savedFontSize) {
    document.documentElement.style.fontSize = savedFontSize + 'px';
}

