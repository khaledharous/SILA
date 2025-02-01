function showTable(title, data) {
    // Set the title of the popup
    document.getElementById('table-title').textContent = title;

    // Clear any existing rows in the table body
    const tableBody = document.getElementById('details-table').querySelector('tbody');
    tableBody.innerHTML = '';

    // Populate the table with the provided data
    data.forEach(([item, score]) => {
        const row = document.createElement('tr');

        const itemCell = document.createElement('td');
        itemCell.textContent = item;
        row.appendChild(itemCell);

        const scoreCell = document.createElement('td');
        scoreCell.textContent = score;
        row.appendChild(scoreCell);

        tableBody.appendChild(row);
    });

    // Show the overlay and popup table
    document.getElementById('overlay').style.display = 'block';
    document.getElementById('popup-table').style.display = 'block';
}

function closeTable() {
    // Hide the overlay and popup table
    document.getElementById('overlay').style.display = 'none';
    document.getElementById('popup-table').style.display = 'none';
}