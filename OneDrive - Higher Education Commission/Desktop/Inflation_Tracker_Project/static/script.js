document.addEventListener('DOMContentLoaded', () => {
    fetchStats();
    fetchItems();

    const searchInput = document.getElementById('searchInput');
    searchInput.addEventListener('input', (e) => filterItems(e.target.value));
});

let allItems = [];

async function fetchStats() {
    try {
        const response = await fetch('/api/stats');
        const data = await response.json();

        renderStatList('topIncreases', data.increases, true);
        renderStatList('topDecreases', data.decreases, false);
    } catch (error) {
        console.error('Error fetching stats:', error);
    }
}

async function fetchItems() {
    try {
        const response = await fetch('/api/items');
        allItems = await response.json();
        renderTable(allItems);
    } catch (error) {
        console.error('Error fetching items:', error);
        document.getElementById('tableBody').innerHTML = '<tr><td colspan="6" class="loading">Error loading data</td></tr>';
    }
}

function renderStatList(elementId, items, isIncrease) {
    const container = document.getElementById(elementId);
    container.innerHTML = items.map(item => `
        <li class="stat-item">
            <span>${item.item_name}</span>
            <span class="stat-val ${isIncrease ? 'increase' : 'decrease'}">
                ${item.change_nov_25_oct_25 > 0 ? '+' : ''}${item.change_nov_25_oct_25.toFixed(2)}%
            </span>
        </li>
    `).join('');
}

function renderTable(items) {
    const tbody = document.getElementById('tableBody');
    tbody.innerHTML = items.map(item => `
        <tr>
            <td>${item.item_name}</td>
            <td>${item.unit}</td>
            <td class="price-cell">${formatPrice(item.avg_price_nov_25)}</td>
            <td class="price-cell">${formatPrice(item.avg_price_oct_25)}</td>
            <td class="price-cell ${getChangeClass(item.change_nov_25_oct_25)}">
                ${formatChange(item.change_nov_25_oct_25)}
            </td>
            <td class="price-cell ${getChangeClass(item.change_nov_25_nov_24)}">
                ${formatChange(item.change_nov_25_nov_24)}
            </td>
        </tr>
    `).join('');
}

function filterItems(query) {
    const lowerQuery = query.toLowerCase();
    const filtered = allItems.filter(item =>
        item.item_name.toLowerCase().includes(lowerQuery)
    );
    renderTable(filtered);
}

function formatPrice(price) {
    return price ? `Rs. ${price.toFixed(2)}` : '-';
}

function formatChange(change) {
    if (change === null || change === undefined) return '-';
    const sign = change > 0 ? '+' : '';
    return `${sign}${change.toFixed(2)}%`;
}

function getChangeClass(change) {
    if (change > 0) return 'increase';
    if (change < 0) return 'decrease';
    return '';
}
