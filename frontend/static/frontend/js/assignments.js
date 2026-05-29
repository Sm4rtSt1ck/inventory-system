let showActive = true;

document.addEventListener('DOMContentLoaded', async () => {
    if (!checkAuth()) return;
    markActiveNav();

    if (isAdminOrManager()) {
        document.getElementById('btn-add').classList.remove('d-none');
        await populateSelects();
    }

    document.getElementById('toggle-active').addEventListener('click', () => { showActive = true; updateToggle(); loadAssignments(); });
    document.getElementById('toggle-all').addEventListener('click', () => { showActive = false; updateToggle(); loadAssignments(); });

    document.getElementById('form-assignment').addEventListener('submit', async e => {
        e.preventDefault();
        const data = Object.fromEntries(new FormData(e.target));
        const res = await API.json('POST', '/assignments/', data);
        if (res) {
            toast('Assignment created');
            bootstrap.Modal.getInstance(document.getElementById('modal-add')).hide();
            e.target.reset();
            loadAssignments();
        }
    });

    loadAssignments();
});

function updateToggle() {
    document.getElementById('toggle-active').classList.toggle('btn-primary', showActive);
    document.getElementById('toggle-active').classList.toggle('btn-outline-secondary', !showActive);
    document.getElementById('toggle-all').classList.toggle('btn-primary', !showActive);
    document.getElementById('toggle-all').classList.toggle('btn-outline-secondary', showActive);
}

async function loadAssignments() {
    const url = showActive ? '/assignments/?active=true' : '/assignments/';
    const tbody = document.getElementById('tbody');
    tbody.innerHTML = `<tr><td colspan="7" class="spinner-overlay"><div class="spinner-border spinner-border-sm text-secondary"></div></td></tr>`;

    const data = await API.json('GET', url);
    if (!data) return;

    if (!data.length) {
        tbody.innerHTML = `<tr><td colspan="7"><div class="empty-state"><i class="bi bi-clipboard-x"></i>No assignments found</div></td></tr>`;
        return;
    }

    tbody.innerHTML = data.map(a => `
        <tr>
            <td><a href="/equipment/${a.equipment}/" class="text-decoration-none fw-medium">Equipment #${a.equipment}</a></td>
            <td>${a.laboratory ? `${a.laboratory.name}<br><small class="text-muted">${a.laboratory.building}, room ${a.laboratory.room}</small>` : a.laboratory}</td>
            <td>${a.person ? a.person.full_name : a.person}</td>
            <td>${a.person ? roleBadge(a.person.role) : ''}</td>
            <td class="text-muted">${a.date_from}</td>
            <td class="text-muted">${a.date_to || '—'}</td>
            <td>${a.is_active
                ? `<span class="badge badge-active">Active</span>`
                : `<span class="badge badge-closed">Closed</span>`}
            ${a.is_active && isAdminOrManager()
                ? `<button class="btn btn-sm btn-outline-secondary ms-1 py-0" onclick="closeAssignment(${a.id})">Close</button>`
                : ''}
            </td>
        </tr>`).join('');
}

async function closeAssignment(id) {
    const today = new Date().toISOString().split('T')[0];
    const res = await API.json('PATCH', `/assignments/${id}/`, { date_to: today });
    if (res !== null) { toast('Assignment closed'); loadAssignments(); }
}

async function populateSelects() {
    const [equip, labs, persons] = await Promise.all([
        API.json('GET', '/equipment/'),
        API.json('GET', '/laboratories/'),
        API.json('GET', '/persons/'),
    ]);

    const sel = (id, items, fn) => {
        const el = document.getElementById(id);
        if (!el || !items) return;
        items.forEach(i => { const o = new Option(...fn(i)); el.add(o); });
    };

    sel('sel-equipment', equip, e => [`${e.name} (${e.serial_number})`, e.id]);
    sel('sel-lab', labs, l => [`${l.name} — ${l.building} ${l.room}`, l.id]);
    sel('sel-person', persons, p => [`${p.full_name} (${p.role})`, p.id]);
}
