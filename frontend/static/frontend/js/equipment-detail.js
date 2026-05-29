const EQ_ID = window.EQUIPMENT_ID;

document.addEventListener('DOMContentLoaded', async () => {
    if (!checkAuth()) return;

    await loadEquipment();
    await loadComponents();
    await loadHistory();

    if (isAdmin()) {
        document.querySelectorAll('.admin-only').forEach(el => el.classList.remove('d-none'));
    }
    if (isAdminOrManager()) {
        document.querySelectorAll('.manager-only').forEach(el => el.classList.remove('d-none'));
    }

    document.getElementById('form-component').addEventListener('submit', async e => {
        e.preventDefault();
        const data = Object.fromEntries(new FormData(e.target));
        const res = await API.json('POST', `/equipment/${EQ_ID}/components/`, data);
        if (res) {
            toast('Component added');
            bootstrap.Modal.getInstance(document.getElementById('modal-component')).hide();
            e.target.reset();
            await loadComponents();
        }
    });

    document.getElementById('form-edit').addEventListener('submit', async e => {
        e.preventDefault();
        const data = Object.fromEntries(new FormData(e.target));
        const res = await API.json('PATCH', `/equipment/${EQ_ID}/`, data);
        if (res) {
            toast('Equipment updated');
            bootstrap.Modal.getInstance(document.getElementById('modal-edit')).hide();
            await loadEquipment();
        }
    });
});

async function loadEquipment() {
    const eq = await API.json('GET', `/equipment/${EQ_ID}/`);
    if (!eq) return;

    document.getElementById('eq-title').textContent = eq.name;
    document.getElementById('detail-name').textContent = eq.name;
    document.getElementById('detail-model').textContent = eq.model;
    document.getElementById('detail-serial').textContent = eq.serial_number;
    document.getElementById('detail-type').innerHTML = typeBadge(eq.type);
    document.getElementById('detail-status').innerHTML = statusBadge(eq.status);
    document.getElementById('detail-date').textContent = eq.purchase_date;
    document.getElementById('detail-purpose').textContent = eq.purpose || '—';

    const form = document.getElementById('form-edit');
    form.name.value = eq.name;
    form.model.value = eq.model;
    form.serial_number.value = eq.serial_number;
    form.type.value = eq.type;
    form.status.value = eq.status;
    form.purchase_date.value = eq.purchase_date;
    form.purpose.value = eq.purpose || '';
}

async function loadComponents() {
    const data = await API.json('GET', `/equipment/${EQ_ID}/components/`);
    if (!data) return;
    const container = document.getElementById('components-list');
    if (!data.length) {
        container.innerHTML = `<div class="empty-state"><i class="bi bi-box-seam"></i>No components</div>`;
        return;
    }
    container.innerHTML = `<table class="table table-sm mb-0">
        <thead><tr><th>Name</th><th>Type</th>${isAdmin() ? '<th></th>' : ''}</tr></thead>
        <tbody>${data.map(c => `
            <tr>
                <td>${c.name}</td>
                <td>${typeBadge(c.type)}</td>
                ${isAdmin() ? `<td><button class="btn btn-sm btn-outline-danger py-0" onclick="removeComponent(${c.id})">
                    <i class="bi bi-trash"></i></button></td>` : ''}
            </tr>`).join('')}
        </tbody></table>`;
}

async function removeComponent(id) {
    if (!confirm('Remove this component?')) return;
    const res = await API.json('DELETE', `/equipment/${EQ_ID}/components/${id}/`);
    if (res !== null) { toast('Component removed'); await loadComponents(); }
}

async function loadHistory() {
    const data = await API.json('GET', `/equipment/${EQ_ID}/history/`);
    if (!data) return;
    const container = document.getElementById('history-list');
    if (!data.length) {
        container.innerHTML = `<div class="empty-state"><i class="bi bi-clock-history"></i>No history</div>`;
        return;
    }
    container.innerHTML = data.map(h => `
        <div class="history-item">
            <div class="history-dot"></div>
            <div class="flex-1">
                <div>${h.action}</div>
                <div class="history-time">${new Date(h.timestamp).toLocaleString()}</div>
            </div>
        </div>`).join('');
}
