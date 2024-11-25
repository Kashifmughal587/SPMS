// document.addEventListener('DOMContentLoaded', () => {
//     const modeToggle = document.getElementById('modeToggle');
//     const sidebarToggle = document.getElementById('sidebarToggle');
//     const sidebar = document.getElementById('sidebar');

//     // Toggle Dark/Light Mode
//     modeToggle.addEventListener('click', () => {
//         document.body.classList.toggle('dark-mode');
//         document.body.classList.toggle('light-mode');

//         // Update mode button
//         if (document.body.classList.contains('dark-mode')) {
//             modeToggle.innerHTML = '<i class="bi bi-sun"></i> Light Mode';
//         } else {
//             modeToggle.innerHTML = '<i class="bi bi-moon"></i> Dark Mode';
//         }
//     });

//     // Sidebar Toggle
//     sidebarToggle.addEventListener('click', () => {
//         sidebar.classList.toggle('d-none');
//     });
// });

function togglePermanentAddress() {
    const isChecked = document.getElementById('same_as_present').checked;

    // Get permanent address inputs
    const permanentInputs = document.querySelectorAll('#permanent_address, #permanent_city, #permanent_state, #permanent_country');

    if (isChecked) {
        // Disable and clear inputs
        permanentInputs.forEach(input => {
            input.disabled = true;
            input.value = ''; // Optional: Clear the input values
        });
    } else {
        // Enable inputs
        permanentInputs.forEach(input => {
            input.disabled = false;
        });
    }
}
