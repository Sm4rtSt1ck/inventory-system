document.addEventListener('DOMContentLoaded', async () => {
    if (!checkAuth()) return;
    markActiveNav();

    if (isAdmin()) document.getElementById('btn-add').classList.remove('d-none');

    await loadLabs();

    document.getElementById('form-lab').addEventListener('submit', async e => {
        e.preventDefault();
        const data = Object.fromEntries(new FormData(e.target));
        const res = await API.json('POST', '/laboratories/', data);
        if (res) {
            toast('Laboratory created');
            bootstrap.Modal.getInstance(document.getElementById('modal-add')).hide();
            e.target.reset();
            await loadLabs();
        }
    });
});

async function loadLabs() {
    const tbody = document.getElementById('tbody');
    const data = await API.json('GET', '/laboratories/');
    if (!data) return;

    if (!data.length) {
        tbody.innerHTML = `<tr><td colspan="4"><div class="empty-state"><i class="bi bi-building"></i>No laboratories</div></td></tr>`;
        return;
    }
    tbody.innerHTML = data.map(l => `
        <tr>
            <td><strong>${l.name}</strong></td>
            <td>${l.room}</td>
            <td>${l.building}</td>
            <td>${isAdmin()
                ? `<button class="btn btn-sm btn-outline-danger py-0" onclick="deleteLab(${l.id})"><i class="bi bi-trash"></i></button>`
                : ''}</td>
        </tr>`).join('');
}

async function deleteLab(id) {
    if (!confirm('Delete this laboratory?')) return;
    const res = await API.json('DELETE', `/laboratories/${id}/`);
    if (res !== null) { toast('Laboratory deleted'); await loadLabs(); }
}
