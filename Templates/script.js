const table = document.getElementById('csv-table');

fetch('cleaned_city_codes.csv')  // Replace with the path to your CSV file
    .then(response => response.text())
    .then(data => {
        const csvRows = data.split(/\r?\n|\r/);  // Split CSV data into rows

        // Create table header row
        const headerRow = document.createElement('tr');
        csvRows[0].split(',').forEach(header => {
            const headerCell = document.createElement('th');
            headerCell.textContent = header;
            headerRow.appendChild(headerCell);
        });
        table.appendChild(headerRow);

        // Create data rows from remaining CSV data
        for (let i = 1; i < csvRows.length; i++) {
            const rowData = csvRows[i].split(',');
            const dataRow = document.createElement('tr');
            rowData.forEach(cellData => {
                const dataCell = document.createElement('td');
                dataCell.textContent = cellData;
                dataRow.appendChild(dataCell);
            });
            table.appendChild(dataRow);
        }
    })
    .catch(error => console.error(error));
