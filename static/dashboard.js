function loadAccounts() {
    fetch("/get_accounts")
        .then(response => response.json())
        .then(data => {
            const tableBody = document.querySelector("#accountsTable tbody");
            tableBody.innerHTML = "";
            if (data.length === 0) {
                tableBody.innerHTML = "<tr><td colspan='3'>No accounts created yet.</td></tr>";
                return;
            }
            data.forEach(account => {
                const row = document.createElement("tr");
                row.innerHTML = `<td>${account.Email}</td><td>${account.Proxy || "N/A"}</td><td>${account.Time}</td>`;
                tableBody.appendChild(row);
            });
        })
        .catch(error => console.error("Error loading accounts:", error))
        .finally(() => setTimeout(loadAccounts, 5000)); // Ensures next request starts after the previous one finishes
}

loadAccounts();  // Initial load