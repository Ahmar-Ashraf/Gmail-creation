document.getElementById("automationForm").addEventListener("submit", function(event) {
    event.preventDefault();

    let numAccounts = parseInt(document.getElementById("numAccounts").value, 10);
    let statusMessage = document.getElementById("statusMessage");

    if (isNaN(numAccounts) || numAccounts < 1) {
        statusMessage.textContent = "❌ Please enter a valid number of accounts!";
        statusMessage.style.color = "red";
        return;
    }

    fetch("/create_accounts", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ num_accounts: numAccounts })  // ✅ Removed password field
    })
    .then(response => response.json())
    .then(data => {
        statusMessage.textContent = data.status === "success" ? "✅ Automation started!" : "❌ Error: " + data.message;
        statusMessage.style.color = data.status === "success" ? "green" : "red";
    })
    .catch(error => {
        statusMessage.textContent = "❌ Network error. Please try again.";
        statusMessage.style.color = "red";
        console.error("Error:", error);
    });
});