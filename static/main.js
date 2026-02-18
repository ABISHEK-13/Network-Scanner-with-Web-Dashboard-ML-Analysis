const darkModeToggle = document.getElementById("darkModeToggle");

if (localStorage.getItem('darkMode') === 'true') {
    document.body.classList.add('dark-mode');
}
darkModeToggle.addEventListener('click', () => {
    const isDarkMode = document.body.classList.toggle('dark-mode');
    localStorage.setItem('darkMode', isDarkMode);
});

function loadHistory() {
    fetch('/history')
        .then(res => res.json())
        .then(data => {
            const historyContainer = document.getElementById('historyContainer');
            historyContainer.innerHTML = '';
            data.forEach(scan => {
                const entryDiv = document.createElement('div');
                entryDiv.classList.add('history-entry');
                entryDiv.innerHTML = `
                    <strong>Scan ID: ${scan.id}</strong>
                    <button onclick="viewScan(${scan.id})">View</button>
                    <button onclick="downloadScan(${scan.id})">Download</button>
                `;
                historyContainer.appendChild(entryDiv);
            });
        });
}

function viewScan(scanId) {
    fetch(`/history/${scanId}`)
        .then(res => res.json())
        .then(scan => {
            const scanDetails = document.getElementById('scanDetails');
            scanDetails.innerHTML = `
                <h2>Scan Details (ID: ${scan.id})</h2>
                <pre>${JSON.stringify(scan, null, 2)}</pre>
            `;
        });
}

function downloadScan(scanId) {
    fetch(`/history/${scanId}/export`)
        .then(res => res.blob())
        .then(blob => {
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `scan_${scanId}.pdf`;
            a.click();
            URL.revokeObjectURL(url);
        });
}

document.addEventListener('DOMContentLoaded', loadHistory);
