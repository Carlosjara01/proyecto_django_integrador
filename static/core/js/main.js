// Confirmación de eliminación
document.addEventListener("DOMContentLoaded", function() {
    const deleteForms = document.querySelectorAll(".delete-form");
    deleteForms.forEach(form => {
        form.addEventListener("submit", function(event) {
            const confirmed = confirm("¿Estás seguro que deseas eliminar este registro?");
            if (!confirmed) {
                event.preventDefault();
            }
        });
    });
});

// Filtro rápido en listas (tabla de productos o pedidos)
const searchInput = document.getElementById("search-input");
if (searchInput) {
    searchInput.addEventListener("keyup", function() {
        const filter = searchInput.value.toLowerCase();
        const rows = document.querySelectorAll("#search-table tbody tr");
        rows.forEach(row => {
            const text = row.textContent.toLowerCase();
            row.style.display = text.includes(filter) ? "" : "none";
        });
    });
}

// Alertas temporales desaparecen tras 3 segundos
document.querySelectorAll(".alert").forEach(alert => {
    setTimeout(() => {
        alert.style.display = "none";
    }, 3000);
});
