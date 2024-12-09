// Theme Selector Logic
document.addEventListener("DOMContentLoaded", () => {
    const themeSelector = document.getElementById("theme");
    const savedTheme = localStorage.getItem("theme");

    // Apply the saved theme on load
    if (savedTheme) {
        document.body.className = savedTheme; // Set the theme class
        if (themeSelector) themeSelector.value = savedTheme; // Set the dropdown value
    }

    // Listen for theme changes
    if (themeSelector) {
        themeSelector.addEventListener("change", (event) => {
            const selectedTheme = event.target.value;

            // Apply the selected theme
            document.body.className = selectedTheme;

            // Save the preference in localStorage
            localStorage.setItem("theme", selectedTheme);
        });
    }
});
