const API = {
    base: '/api',

    async request(method, path, data = null) {
        const token = localStorage.getItem('access');
        const headers = { 'Content-Type': 'application/json' };
        if (token) headers['Authorization'] = `Bearer ${token}`;

        const opts = { method, headers };
        if (data !== null) opts.body = JSON.stringify(data);

        let res = await fetch(this.base + path, opts);

        if (res.status === 401) {
            const ok = await this._refresh();
            if (!ok) return null;
            headers['Authorization'] = `Bearer ${localStorage.getItem('access')}`;
            res = await fetch(this.base + path, { ...opts, headers });
        }

        return res;
    },

    async _refresh() {
        const refresh = localStorage.getItem('refresh');
        if (!refresh) { this.logout(); return false; }
        const res = await fetch(this.base + '/auth/refresh/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ refresh }),
        });
        if (res.ok) {
            const d = await res.json();
            localStorage.setItem('access', d.access);
            return true;
        }
        this.logout();
        return false;
    },

    logout() {
        localStorage.clear();
        window.location.href = '/login/';
    },

    async json(method, path, data = null) {
        const res = await this.request(method, path, data);
        if (!res) return null;
        if (!res.ok) {
            let msg = `Error ${res.status}`;
            try { const e = await res.json(); msg = Object.values(e).flat().join(' '); } catch {}
            toast(msg, 'danger');
            return null;
        }
        if (res.status === 204) return {};
        return res.json();
    },
};

function toast(message, type = 'success') {
    const container = document.getElementById('toast-container');
    if (!container) return;
    const id = 'toast-' + Date.now();
    container.insertAdjacentHTML('beforeend', `
        <div id="${id}" class="toast align-items-center text-bg-${type} border-0" role="alert" aria-live="assertive">
            <div class="d-flex">
                <div class="toast-body">${message}</div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        </div>`);
    const el = document.getElementById(id);
    new bootstrap.Toast(el, { delay: 3500 }).show();
    el.addEventListener('hidden.bs.toast', () => el.remove());
}

function checkAuth() {
    if (!localStorage.getItem('access')) { window.location.href = '/login/'; return false; }
    const user = getUser();
    const el = document.getElementById('user-badge');
    if (el) el.textContent = `${user.username} · ${user.role}`;
    return true;
}

function getUser() { return JSON.parse(localStorage.getItem('user') || '{}'); }
function isAdmin() { return getUser().role === 'admin'; }
function isAdminOrManager() { return ['admin', 'lab_manager'].includes(getUser().role); }

function markActiveNav() {
    const path = window.location.pathname.replace(/\/$/, '') || '/';
    document.querySelectorAll('.sidebar .nav-link').forEach(a => {
        const href = (a.getAttribute('href') || '').replace(/\/$/, '') || '/';
        const active = href === '/' ? path === '/' || path === '' : path === href || path.startsWith(href + '/');
        a.classList.toggle('active', active);
    });
}

function statusBadge(s) {
    const label = { in_use: 'In Use', in_repair: 'In Repair', decommissioned: 'Decommissioned' }[s] || s;
    return `<span class="badge badge-${s}">${label}</span>`;
}

function typeBadge(t) { return `<span class="badge badge-type">${t}</span>`; }
function roleBadge(r) { return `<span class="badge badge-role">${r}</span>`; }

function debounce(fn, ms) {
    let t; return (...a) => { clearTimeout(t); t = setTimeout(() => fn(...a), ms); };
}

function logout() { API.logout(); }
