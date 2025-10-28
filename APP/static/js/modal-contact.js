document.addEventListener('DOMContentLoaded', function() {
    // Funcionalidade do menu mobile
    const menuBtn = document.querySelector('.menu-btn');
    const menuDropdown = document.getElementById('menuDropdown');
    
    if (menuBtn && menuDropdown) {
        menuBtn.addEventListener('click', function() {
            menuDropdown.classList.toggle('show');
        });
        
        // Fechar o menu ao clicar fora
        document.addEventListener('click', function(e) {
            if (!menuDropdown.contains(e.target) && e.target !== menuBtn) {
                menuDropdown.classList.remove('show');
            }
        });
    }
    
    // Modal de contato
    const openContact = document.getElementById('open-contact');
    const closeContact = document.getElementById('close-contact');
    const contactModal = document.getElementById('contact-modal');
    const contactForm = document.getElementById('modal-contact-form');
    const contactFeedback = document.getElementById('contact-feedback');
    
    if (openContact && closeContact && contactModal) {
        openContact.addEventListener('click', function() {
            contactModal.style.display = 'flex';
            setTimeout(() => {
                contactModal.querySelector('.modal-content').style.opacity = '1';
                contactModal.querySelector('.modal-content').style.transform = 'translateY(0)';
            }, 10);
        });
        
        closeContact.addEventListener('click', function() {
            contactModal.querySelector('.modal-content').style.opacity = '0';
            contactModal.querySelector('.modal-content').style.transform = 'translateY(-20px)';
            setTimeout(() => {
                contactModal.style.display = 'none';
            }, 300);
        });
        
        // Fechar ao clicar fora
        contactModal.addEventListener('click', function(e) {
            if (e.target === contactModal) {
                closeContact.click();
            }
        });
        
        // Processar o formulário de contato
        if (contactForm) {
            contactForm.addEventListener('submit', function(e) {
                e.preventDefault();
                
                // Simulação de envio bem-sucedido
                contactFeedback.textContent = 'Mensagem enviada com sucesso! Entraremos em contato em breve.';
                contactFeedback.style.color = 'var(--success-color)';
                contactFeedback.style.display = 'block';
                
                // Limpar o formulário
                contactForm.reset();
                
                // Fechar o modal após 3 segundos
                setTimeout(() => {
                    closeContact.click();
                    contactFeedback.style.display = 'none';
                }, 3000);
            });
        }
    }
});