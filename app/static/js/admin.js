const token = localStorage.getItem("token");

if (!token) {
    window.location.href = "/";
}

function logout() {
    localStorage.removeItem("token");
    window.location.href = "/";
}

async function loadDashboard() {
    const res = await fetch("/metrics", {
        headers: {
            "Authorization": "Bearer " + token
        }
    });

    if (res.status === 403) {
        alert("No autorizado");
        return;
    }

    const data = await res.json();

    document.getElementById("metrics").innerHTML = `
        <div class="card">
            <h3>Pedidos Activos</h3>
            <p>${data.active_orders}</p>
        </div>
        <div class="card">
            <h3>Ingresos Hoy</h3>
            <p>$${data.today_income}</p>
        </div>
        <div class="card">
            <h3>Mensajeros Activos</h3>
            <p>${data.active_drivers}</p>
        </div>
    `;

    loadOrders();
}

async function loadOrders() {
    const res = await fetch("/orders", {
        headers: {
            "Authorization": "Bearer " + token
        }
    });

    const orders = await res.json();

    let html = `
        <table>
            <tr>
                <th>ID</th>
                <th>Estado</th>
                <th>Total</th>
            </tr>
    `;

    orders.forEach(order => {
        html += `
            <tr>
                <td>${order.id}</td>
                <td>${order.status}</td>
                <td>$${order.total}</td>
            </tr>
        `;
    });

    html += "</table>";

    document.getElementById("table-container").innerHTML = html;
}

async function loadUsers() {
    const res = await fetch("/users", {
        headers: {
            "Authorization": "Bearer " + token
        }
    });

    const users = await res.json();

    let html = `
        <table>
            <tr>
                <th>Email</th>
                <th>Rol</th>
            </tr>
    `;

    users.forEach(user => {
        html += `
            <tr>
                <td>${user.email}</td>
                <td>${user.role}</td>
            </tr>
        `;
    });

    html += "</table>";

    document.getElementById("table-container").innerHTML = html;
}

loadDashboard();