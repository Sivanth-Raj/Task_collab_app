document.addEventListener("DOMContentLoaded", function () {
    // Highlight overdue tasks in red dynamically
    highlightOverdueTasks();

    // Setup filter and sort dropdown event listeners
    setupFilters();

    // Setup task search input
    setupSearch();

    // Form validation or improvements can be added here
});

document.querySelectorAll("select[name='task_status']").forEach(select => {
    select.addEventListener("change", async function () {
        console.log("here")
        const taskId = this.dataset.taskId; // assuming data attribute with task id
        const newStatus = this.value;
        console.log(newStatus, taskId)
        const response = await fetch(`/update-task/${taskId}`, {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded"
            },
            body: new URLSearchParams({ task_status: newStatus })
        });
        if (!response.ok) {
            alert("Failed to update task status");
        }
    });
});



function highlightOverdueTasks() {
    const rows = document.querySelectorAll("table tbody tr");
    const now = new Date();

    rows.forEach(row => {
        const deadlineCell = row.querySelector("td:nth-child(3)");
        const statusSelect = row.querySelector("select[name='status']");
        if (!deadlineCell || !statusSelect) return;

        const deadline = new Date(deadlineCell.textContent || deadlineCell.innerText);
        const status = statusSelect.value;

        if (deadline < now && status !== "Completed") {
            row.classList.add("table-danger");
        } else {
            row.classList.remove("table-danger");
        }
    });
}

function setupFilters() {
    // Assuming you have dropdowns for filters/sorts (add to your HTML)
    // Example: filter by priority or status
    const priorityFilter = document.getElementById("priorityFilter");
    const statusFilter = document.getElementById("statusFilter");

    if (priorityFilter) {
        priorityFilter.addEventListener("change", filterTasks);
    }
    if (statusFilter) {
        statusFilter.addEventListener("change", filterTasks);
    }
}

function filterTasks() {
    const priorityFilter = document.getElementById("priorityFilter")?.value || "";
    const statusFilter = document.getElementById("statusFilter")?.value || "";

    const rows = document.querySelectorAll("table tbody tr");

    rows.forEach(row => {
        let show = true;

        if (priorityFilter) {
            const priority = row.querySelector("td:nth-child(4)").textContent.trim();
            if (priority !== priorityFilter) show = false;
        }
        if (statusFilter) {
            const statusSelect = row.querySelector("select[name='status']");
            const status = statusSelect ? statusSelect.value : "";
            if (status !== statusFilter) show = false;
        }

        row.style.display = show ? "" : "none";
    });
}

function setupSearch() {
    const searchInput = document.getElementById("taskSearch");
    if (!searchInput) return;

    searchInput.addEventListener("input", function () {
        const filter = searchInput.value.toLowerCase();
        const rows = document.querySelectorAll("table tbody tr");

        rows.forEach(row => {
            const title = row.querySelector("td:first-child").textContent.toLowerCase();
            const desc = row.querySelector("td:nth-child(2)").textContent.toLowerCase();
            if (title.includes(filter) || desc.includes(filter)) {
                row.style.display = "";
            } else {
                row.style.display = "none";
            }
        });
    });
}
document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('addTaskForm');
    if (form) {
        form.addEventListener('submit', async function (event) {
            event.preventDefault();
            const formData = new FormData(form);
            const response = await fetch(form.action, {
                method: 'POST',
                body: formData,
                headers: { 'X-Requested-With': 'XMLHttpRequest' }
            });
            if (response.ok) {
                const newTaskRowHtml = await response.text();

                // Insert new row into task table tbody
                const tbody = document.querySelector("table tbody");
                tbody.insertAdjacentHTML("beforeend", newTaskRowHtml);

                // Reset form fields
                form.reset();
            } else {
                alert("Failed to add task");
            }

        });
    }
});

