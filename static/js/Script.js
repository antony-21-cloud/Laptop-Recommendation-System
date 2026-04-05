function checkAccess() {
    fetch('/api/auth/status')
        .then(response => response.json())
        .then(user => {
            if (user.is_logged_in) {
                // Update the UI with the username
                const display = document.getElementById('user-display');
                if (display) display.innerText = user.username.toUpperCase();
                
                // Security Check: If a student tries to access the seller page, kick them out
                const path = window.location.pathname;
                if (path.includes('seller') && user.role !== 'seller') {
                    window.location.href = '/login'; 
                }
            } else {
                window.location.href = '/login';
            }
        })
        .catch(() => {
            // If the server is down or session expired
            window.location.href = '/login';
        });
}


function executeLogin() {
    const data = {
        username: document.getElementById('login-user').value,
        password: document.getElementById('login-pass').value
    };

    fetch('/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    })
    .then(res => res.json())
    .then(res => {
        if (res.success) {
            // Redirect based on the role the Chef sent back
            if (res.role === 'seller') window.location.href = '/seller_dashboard';
            else window.location.href = '/student_dashboard';
        } else {
            alert("ACCESS_DENIED: Invalid Credentials");
        }
    });
}

function loadAdminDashboard() {
    fetch('/api/admin/all_users')
        .then(res => res.json())
        .then(data => {
            const userTable = document.getElementById('admin-user-table');
            const userCount = document.getElementById('admin-user-count');
            const laptopCount = document.getElementById('admin-laptop-count');

            if (userCount) userCount.innerText = data.users.length;
            if (laptopCount) laptopCount.innerText = data.total_laptops;

            if (userTable) {
                userTable.innerHTML = '';
                data.users.forEach(user => {
                    userTable.innerHTML += `
                        <tr class="hover:bg-rose-900/10 transition-colors">
                            <td class="p-4 text-slate-500">#${user.id}</td>
                            <td class="p-4 font-bold text-slate-200">${user.username}</td>
                            <td class="p-4">
                                <span class="px-2 py-0.5 rounded border ${user.role === 'admin' ? 'border-rose-500 text-rose-500' : 'border-slate-700 text-slate-400'}">
                                    ${user.role.toUpperCase()}
                                </span>
                            </td>
                            <td class="p-4 text-right">
                                <button onclick="deleteUser(${user.id})" class="text-rose-600 hover:text-rose-400 font-bold">TERMINATE</button>
                            </td>
                        </tr>
                    `;
                });
            }
        });
}

// Ensure Admin view loads if we are on that page
if (window.location.pathname.includes('admin')) {
    document.addEventListener('DOMContentLoaded', loadAdminDashboard);
}


// Initialize security on page load
document.addEventListener('DOMContentLoaded', checkAccess);


function loadSellerLaptops() {
    fetch('/api/seller/laptops')
        .then(response => response.json())
        .then(data => {
            console.log("Data received from Chef:", data);
            const tableBody = document.getElementById('laptop-list-body');
            
            if (tableBody) {
                tableBody.innerHTML = ''; // Clear the table first
                data.forEach(laptop => {
                    tableBody.innerHTML += `
                        <tr>
                            <td>${laptop.name}</td>
                            <td>Ksh ${laptop.price}</td>
                            <td>${laptop.processor}</td>
                        </tr>
                    `;
                });
            }
        })
        .catch(error => console.error('Waiter dropped the tray:', error));
}

// Run this when the window finishes loading
window.onload = loadSellerLaptops;


function loadInventory() {
    fetch('/api/seller/laptops')
        .then(response => {
            if (!response.ok) throw new Error('Network response was not ok');
            return response.json();
        })
        .then(data => {
            const tableBody = document.getElementById('laptop-list-body');
            const unitCount = document.getElementById('unit-count');
            
            // Update the counter
            unitCount.innerText = data.length;

            // Clear and Rebuild Table
            tableBody.innerHTML = ''; 
            data.forEach(laptop => {
                tableBody.innerHTML += `
                    <tr class="hover:bg-slate-800/50 transition-colors">
                        <td class="p-4 font-bold text-cyan-200">${laptop.name}</td>
                        <td class="p-4 text-slate-400">${laptop.processor} / ${laptop.ram}GB</td>
                        <td class="p-4 text-emerald-400">${laptop.price.toLocaleString()}</td>
                        <td class="p-4 text-right">
                            <button class="text-xs text-rose-500 hover:underline">DELETE</button>
                        </td>
                    </tr>
                `;
            });
        })
        .catch(err => console.error("CRITICAL_FETCH_ERROR:", err));
}

// Auto-fire when page hits the browser
document.addEventListener('DOMContentLoaded', loadInventory);


// UI Controls
function openModal() { document.getElementById('add-modal').classList.remove('hidden'); }
function closeModal() { document.getElementById('add-modal').classList.add('hidden'); }

// The Logic
function submitNewLaptop() {
    const payload = {
        name: document.getElementById('new-name').value,
        processor: document.getElementById('new-processor').value,
        price: document.getElementById('new-price').value
    };

    fetch('/api/seller/add_laptop', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload) // Turn JS object into JSON string
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        closeModal();
        loadInventory(); // Refresh the table without reloading the page!
    })
    .catch(err => console.error("UPLOAD_FAILURE:", err));
}

function searchLaptops() {
    const processor = document.getElementById('filter-processor').value;
    const price = document.getElementById('filter-price').value;

    // Build the URL with query parameters
    const url = `/api/student/search?processor=${processor}&price=${price}`;

    fetch(url)
        .then(res => res.json())
        .then(data => {
            const grid = document.getElementById('results-grid');
            grid.innerHTML = ''; // Clear old results

            if (data.length === 0) {
                grid.innerHTML = '<p class="text-rose-500 text-sm italic">NO_HARDWARE_FOUND_MATCHING_CRITERIA</p>';
                return;
            }

            data.forEach(laptop => {
                grid.innerHTML += `
                    <div class="bg-slate-900 border border-slate-800 p-4 rounded-lg hover:border-emerald-500/50 transition-all shadow-xl">
                        <div class="flex justify-between items-start mb-4">
                            <h3 class="text-lg font-bold text-white">${laptop.name}</h3>
                            <span class="text-xs bg-emerald-950 text-emerald-400 px-2 py-1 rounded border border-emerald-800">${laptop.processor}</span>
                        </div>
                        <div class="space-y-2 text-xs text-slate-400 mb-6">
                            <p>RAM: ${laptop.ram || '8'}GB</p>
                            <p>STORAGE: ${laptop.storage || '512'}GB SSD</p>
                        </div>
                        <div class="flex justify-between items-center border-t border-slate-800 pt-4">
                            <p class="text-xl font-bold text-emerald-400">Ksh ${laptop.price.toLocaleString()}</p>
                            <button class="bg-slate-800 hover:bg-slate-700 text-xs text-white px-3 py-1 rounded">DETAILS</button>
                        </div>
                    </div>
                `;
            });
        });
}

// Initial load to show all hardware
if (document.getElementById('results-grid')) {
    document.addEventListener('DOMContentLoaded', searchLaptops);
}