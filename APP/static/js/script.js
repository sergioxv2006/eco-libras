

// ========== Funções utilitárias e acessibilidade ========== //
function announceToScreenReader(message) {
    // Anuncia mensagens para leitores de tela
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
    setTimeout(() => document.body.removeChild(announcement), 1000);
}

function smoothScrollInit() {
    // Scroll suave para âncoras
    const links = document.querySelectorAll('a[href^="#"]');
    links.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const targetSection = document.querySelector(targetId);
            if (targetSection) {
                const headerHeight = document.querySelector('header').offsetHeight;
                const targetPosition = targetSection.offsetTop - headerHeight - 20;
                window.scrollTo({ top: targetPosition, behavior: 'smooth' });
            }
        });
    });
}

function contactFormInit() {
    // Validação e feedback do formulário de contato
    const contactForm = document.getElementById('modal-contact-form');
    if (!contactForm) return;
    const feedback = document.getElementById('contact-feedback');
    contactForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const name = document.getElementById('name').value.trim();
        const email = document.getElementById('email').value.trim();
        const message = document.getElementById('message').value.trim();
        feedback.textContent = '';
        feedback.style.color = '';
        if (!name || !email || !message) {
            feedback.textContent = 'Por favor, preencha todos os campos obrigatórios.';
            feedback.style.color = 'red';
            return;
        }
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(email)) {
            feedback.textContent = 'Por favor, insira um email válido.';
            feedback.style.color = 'red';
            return;
        }
        feedback.textContent = 'Mensagem enviada com sucesso! Entraremos em contato em breve.';
        feedback.style.color = 'green';
        contactForm.reset();
        setTimeout(() => { feedback.textContent = ''; }, 3000);
    });
}

function animateOnScrollInit() {
    // Anima elementos ao entrar na viewport
    const observerOptions = { threshold: 0.1, rootMargin: '0px 0px -50px 0px' };
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);
    const animatedElements = document.querySelectorAll('.course-item, .feature');
    animatedElements.forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(el);
    });
}

function sectionAnnounceInit() {
    // Anuncia mudança de seção para leitores de tela
    const sections = document.querySelectorAll('section[id]');
    const sectionObserver = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const sectionTitle = entry.target.querySelector('h1, h2');
                if (sectionTitle) announceToScreenReader(`Seção: ${sectionTitle.textContent}`);
            }
        });
    }, { threshold: 0.5 });
    sections.forEach(section => sectionObserver.observe(section));
}

function modalContactInit() {
    // Inicializa modal de contato com acessibilidade
    const openBtn = document.getElementById('open-contact');
    const closeBtn = document.getElementById('close-contact');
    const modal = document.getElementById('contact-modal');
    if (!openBtn || !closeBtn || !modal) return;
    openBtn.addEventListener('click', function(e) {
        e.preventDefault();
        modal.classList.add('show');
    });
    closeBtn.addEventListener('click', function() {
        modal.classList.remove('show');
    });
    modal.addEventListener('click', function(e) {
        if (e.target === this) this.classList.remove('show');
    });
    window.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') modal.classList.remove('show');
    });
}

function accessibilityKeyboardInit() {
    // Melhora navegação por teclado e feedback visual
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') window.scrollTo({ top: 0, behavior: 'smooth' });
        if ((e.key === 'Enter' || e.key === ' ') && e.target.tagName === 'A') e.target.click();
        if (e.key === 'Tab') {
            document.body.classList.add('keyboard-navigation');
        }
    });
    document.addEventListener('mousedown', function() {
        document.body.classList.remove('keyboard-navigation');
    });
}

function focusIndicatorInit() {
    // Indica foco visível para elementos interativos
    document.addEventListener('focusin', function(e) {
        if (e.target.matches('a, button, input, textarea, select')) {
            e.target.setAttribute('data-focus-visible', 'true');
        }
    });
    document.addEventListener('focusout', function(e) {
        e.target.removeAttribute('data-focus-visible');
    });
}

// ========== Inicialização ========== //

// ========== Inicialização ========== //
document.addEventListener('DOMContentLoaded', function() {
    smoothScrollInit();
    contactFormInit();
    animateOnScrollInit();
    sectionAnnounceInit();
    modalContactInit();
    accessibilityKeyboardInit();
    focusIndicatorInit();
    // Preferências de acessibilidade
    if (localStorage.getItem('highContrast') === 'true') {
        document.body.classList.add('high-contrast');
    }
    const savedFontSize = localStorage.getItem('fontSize');
    if (savedFontSize) {
        document.documentElement.style.fontSize = savedFontSize + 'px';
    }
});

    // Função para alternar alto contraste (pode ser ativada por botão)
    function toggleHighContrast() {
        document.body.classList.toggle('high-contrast');
        const isHighContrast = document.body.classList.contains('high-contrast');
        localStorage.setItem('highContrast', isHighContrast);
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
        document.body.appendChild(announcement);

        
