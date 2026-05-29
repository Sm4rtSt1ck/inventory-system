document.addEventListener('DOMContentLoaded', async () => {
    if (!checkAuth()) return;
    markActiveNav();

    if (isAdmin()) document.getElementById('btn-add').classList.remove('d-none');

    await loadPersons();

    document.getElementById('form-person').addEventListener('submit', async e => {
        e.preventDefault();
        const data = Object.fromEntries(new FormData(e.target));
        const res = await API.json('POST', '/persons/', data);
        if (res) {
            toast('Person created');
            bootstrap.Modal.getInstance(document.getElementById('modal-add')).hide();
            e.target.reset();
            await loadPersons();
        }
    });
});

async function loadPersons() {
    const tbody = document.getElementById('tbody');
    const data = await API.json('GET', '/persons/');
    if (!data) return;

    if (!data.length) {
        tbody.innerHTML = `<tr><td colspan="4"><div class="empty-state"><i class="bi bi-people"></i>No persons</div></td></tr>`;
        return;
    }
    tbody.innerHTML = data.map(p => `
        <tr>
            <td><strong>${p.full_name}</strong></td>
            <td>${roleBadge(p.role)}</td>
            <td><a href="mailto:${p.email}" class="text-decoration-none text-muted">${p.email}</a></td>
            <td>${isAdmin()
                ? `<button class="btn btn-sm btn-outline-danger py-0" onclick="deletePerson(${p.id})"><i class="bi bi-trash"></i></button>`
                : ''}</td>
        </tr>`).join('');
}

async function deletePerson(id) {
    if (!confirm('Delete this person?')) return;
    const res = await API.json('DELETE', `/persons/${id}/`);
    if (res !== null) { toast('Person deleted'); await loadPersons(); }
}
