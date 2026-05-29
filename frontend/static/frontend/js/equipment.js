document.addEventListener('DOMContentLoaded', async () => {
    if (!checkAuth()) return;
    markActiveNav();

    if (isAdmin()) document.getElementById('btn-add').classList.remove('d-none');

    await loadStats();
    await loadEquipment();

    document.getElementById('search').addEventListener('input', debounce(loadEquipment, 300));
    document.getElementById('filter-status').addEventListener('change', loadEquipment);
    document.getElementById('filter-type').addEventListener('change', loadEquipment);

    document.getElementById('form-equipment').addEventListener('submit', async e => {
        e.preventDefault();
        const data = Object.fromEntries(new FormData(e.target));
        const res = await API.json('POST', '/equipment/', data);
        if (res) {
            toast('Equipment created');
            bootstrap.Modal.getInstance(document.getElementById('modal-add')).hide();
            e.target.reset();
            await loadStats();
            await loadEquipment();
        }
    });
});

async function loadStats() {
    const data = await API.json('GET', '/equipment/');
    if (!data) return;
    const counts = { in_use: 0, in_repair: 0, decommissioned: 0 };
    data.forEach(e => { if (counts[e.status] !== undefined) counts[e.status]++; });
    document.getElementById('stat-total').textContent = data.length;
    document.getElementById('stat-in-use').textContent = counts.in_use;
    document.getElementById('stat-repair').textContent = counts.in_repair;
    document.getElementById('stat-decomm').textContent = counts.decommissioned;
}

async function loadEquipment() {
    const params = new URLSearchParams();
    const s = document.getElementById('search').value.trim();
    const st = document.getElementById('filter-status').value;
    const ty = document.getElementById('filter-type').value;
    if (s) params.set('search', s);
    if (st) params.set('status', st);
    if (ty) params.set('type', ty);

    const tbody = document.getElementById('equipment-tbody');
    tbody.innerHTML = `<tr><td colspan="6" class="spinner-overlay"><div class="spinner-border spinner-border-sm text-secondary"></div></td></tr>`;

    const data = await API.json('GET', `/equipment/?${params}`);
    if (!data) return;

    if (!data.length) {
        tbody.innerHTML = `<tr><td colspan="6"><div class="empty-state"><i class="bi bi-inbox"></i>No equipment found</div></td></tr>`;
        return;
    }

    tbody.innerHTML = data.map(eq => `
        <tr class="clickable-row" onclick="location.href='/equipment/${eq.id}/'">
            <td><strong>${eq.name}</strong><br><small class="text-muted">${eq.model}</small></td>
            <td><code class="text-secondary">${eq.serial_number}</code></td>
            <td>${typeBadge(eq.type)}</td>
            <td>${statusBadge(eq.status)}</td>
            <td class="text-muted">${eq.purchase_date}</td>
            <td class="text-center">${eq.components ? eq.components.length : 0}</td>
        </tr>`).join('');
}
