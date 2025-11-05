(function() {
    'use strict';
    const TOKEN_KEY = 'eco_libras_token';
    const form = document.getElementById('admin-login-form');
    if (!form) return;

    // Default behaviour: regular form POST (server will set cookie + redirect)
    // If you want AJAX, add data-ajax="1" to the submit button.
    form.addEventListener('submit', function(e) {
        const submitter = e.submitter || document.activeElement;
        if (!submitter || !submitter.dataset || submitter.dataset.ajax !== '1') {
            // allow normal form submit
            return;
        }

        e.preventDefault();
        const data = { username: form.username.value, password: form.password.value };

        fetch(form.action, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
            body: JSON.stringify(data)
        })
        .then(r => r.json())
        .then(json => {
            if (json.success && json.access_token) {
                try { localStorage.setItem(TOKEN_KEY, json.access_token); } catch (_) {}
                window.location.href = json.redirect_url || '/admin/';
            } else {
                const msg = document.getElementById('login-message');
                if (msg) msg.textContent = json.message || 'Login failed';
            }
        })
        .catch(err => {
            const msg = document.getElementById('login-message');
            if (msg) msg.textContent = 'Network error';
            console.error(err);
        });
    });
})();