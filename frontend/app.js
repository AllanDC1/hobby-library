const API = window.location.origin + "/api";

let currentUser = null;
let editingHobbyId = null;

// ========== AUTH ==========

async function loginOrRegister() {
    const username = document.getElementById("input-username").value.trim();
    const email = document.getElementById("input-email").value.trim();
    const errorEl = document.getElementById("auth-error");

    if (!username || !email) {
        errorEl.textContent = "Preencha todos os campos.";
        errorEl.classList.remove("hidden");
        return;
    }

    try {
        const res = await fetch(`${API}/users`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username, email })
        });

        if (!res.ok) throw new Error("Erro ao registrar/entrar");

        currentUser = await res.json();
        showUserPanel();
        loadHobbies();
    } catch (err) {
        errorEl.textContent = err.message;
        errorEl.classList.remove("hidden");
    }
}

function logout() {
    currentUser = null;
    document.getElementById("auth-section").classList.remove("hidden");
    document.getElementById("user-section").classList.add("hidden");
}

function showUserPanel() {
    document.getElementById("auth-section").classList.add("hidden");
    document.getElementById("user-section").classList.remove("hidden");
    document.getElementById("user-info").textContent =
        `${currentUser.username} (${currentUser.email})`;
}

// ========== HOBBIES ==========

async function loadHobbies() {
    const listEl = document.getElementById("hobbies-list");
    const sourceEl = document.getElementById("hobbies-source");

    try {
        const res = await fetch(`${API}/users/${currentUser.id}/hobbies`);
        const data = await res.json();

        sourceEl.textContent = data.source === "cache" ? "⚡ cache" : "🗄️ database";
        sourceEl.className = `badge ${data.source}`;

        const hobbies = data.hobbies;
        if (!hobbies.length) {
            listEl.innerHTML = '<p class="empty-state">Nenhum hobby cadastrado ainda.</p>';
            return;
        }

        listEl.innerHTML = hobbies.map(h => renderHobbyCard(h)).join("");
    } catch (err) {
        listEl.innerHTML = '<p class="error">Erro ao carregar hobbies.</p>';
    }
}

function renderHobbyCard(hobby) {
    const excluded = ["_id", "user_id", "name", "category", "created_at", "updated_at"];
    const customFields = Object.entries(hobby)
        .filter(([k]) => !excluded.includes(k))
        .map(([k, v]) =>
            `<div class="field-item">
                <span class="field-key">${escapeHtml(k)}:</span>
                <span>${escapeHtml(String(v))}</span>
            </div>`
        ).join("");

    const category = hobby.category
        ? `<span class="hobby-category">${escapeHtml(hobby.category)}</span>`
        : "";

    return `
        <div class="hobby-card">
            <div class="hobby-header">
                <span class="hobby-name">${escapeHtml(hobby.name)}</span>
                ${category}
            </div>
            ${customFields ? `<div class="hobby-fields">${customFields}</div>` : ""}
            <div class="hobby-actions">
                <button class="btn-secondary" onclick="openEditModal('${hobby._id}')">Editar</button>
                <button class="btn-danger" onclick="deleteHobby('${hobby._id}')">Excluir</button>
            </div>
        </div>
    `;
}

// ========== ADD HOBBY ==========

function addField() {
    const container = document.getElementById("fields-container");
    const row = document.createElement("div");
    row.className = "field-row";
    row.innerHTML = `
        <input type="text" placeholder="Nome do campo" class="field-key-input">
        <input type="text" placeholder="Valor" class="field-value-input">
        <span class="btn-remove" onclick="this.parentElement.remove()">✕</span>
    `;
    container.appendChild(row);
}

async function addHobby() {
    const name = document.getElementById("hobby-name").value.trim();
    const category = document.getElementById("hobby-category").value.trim();

    if (!name) return;

    const fields = {};
    document.querySelectorAll("#fields-container .field-row").forEach(row => {
        const key = row.querySelector(".field-key-input").value.trim();
        const val = row.querySelector(".field-value-input").value.trim();
        if (key) fields[key] = val;
    });

    try {
        const res = await fetch(`${API}/users/${currentUser.id}/hobbies`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ name, category: category || null, fields })
        });

        if (!res.ok) throw new Error("Erro ao adicionar hobby");

        // Limpa o formulário
        document.getElementById("hobby-name").value = "";
        document.getElementById("hobby-category").value = "";
        document.getElementById("fields-container").innerHTML = "";

        loadHobbies();
    } catch (err) {
        alert(err.message);
    }
}

// ========== EDIT HOBBY ==========

async function openEditModal(hobbyId) {
    editingHobbyId = hobbyId;

    const res = await fetch(`${API}/users/${currentUser.id}/hobbies/${hobbyId}`);
    const hobby = await res.json();

    document.getElementById("edit-hobby-name").value = hobby.name || "";
    document.getElementById("edit-hobby-category").value = hobby.category || "";

    const container = document.getElementById("edit-fields-container");
    container.innerHTML = "";

    const excluded = ["_id", "user_id", "name", "category", "created_at", "updated_at"];
    Object.entries(hobby)
        .filter(([k]) => !excluded.includes(k))
        .forEach(([k, v]) => {
            const row = document.createElement("div");
            row.className = "field-row";
            row.innerHTML = `
                <input type="text" value="${escapeHtml(k)}" class="field-key-input">
                <input type="text" value="${escapeHtml(String(v))}" class="field-value-input">
                <span class="btn-remove" onclick="this.parentElement.remove()">✕</span>
            `;
            container.appendChild(row);
        });

    document.getElementById("edit-modal").classList.remove("hidden");
}

function addEditField() {
    const container = document.getElementById("edit-fields-container");
    const row = document.createElement("div");
    row.className = "field-row";
    row.innerHTML = `
        <input type="text" placeholder="Nome do campo" class="field-key-input">
        <input type="text" placeholder="Valor" class="field-value-input">
        <span class="btn-remove" onclick="this.parentElement.remove()">✕</span>
    `;
    container.appendChild(row);
}

async function saveEdit() {
    const name = document.getElementById("edit-hobby-name").value.trim();
    const category = document.getElementById("edit-hobby-category").value.trim();

    const fields = {};
    document.querySelectorAll("#edit-fields-container .field-row").forEach(row => {
        const key = row.querySelector(".field-key-input").value.trim();
        const val = row.querySelector(".field-value-input").value.trim();
        if (key) fields[key] = val;
    });

    try {
        const res = await fetch(`${API}/users/${currentUser.id}/hobbies/${editingHobbyId}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ name, category: category || null, fields })
        });

        if (!res.ok) throw new Error("Erro ao editar hobby");

        closeEditModal();
        loadHobbies();
    } catch (err) {
        alert(err.message);
    }
}

function closeEditModal() {
    editingHobbyId = null;
    document.getElementById("edit-modal").classList.add("hidden");
}

// ========== DELETE ==========

async function deleteHobby(hobbyId) {
    if (!confirm("Tem certeza que deseja excluir este hobby?")) return;

    try {
        const res = await fetch(`${API}/users/${currentUser.id}/hobbies/${hobbyId}`, {
            method: "DELETE"
        });

        if (!res.ok) throw new Error("Erro ao excluir");

        loadHobbies();
    } catch (err) {
        alert(err.message);
    }
}

// ========== UTILS ==========

function escapeHtml(text) {
    const div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
}
