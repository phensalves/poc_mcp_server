
document.addEventListener('DOMContentLoaded', () => {
    const languageSelect = document.getElementById('language-select');
    const providerSelect = document.getElementById('provider-select');
    const codeInput = document.getElementById('code-input');
    const analyzeBtn = document.getElementById('analyze-btn');
    const resultsContainer = document.getElementById('results-container');
    const resultsOutput = document.getElementById('results-output');

    // Fetch and populate dropdowns
    const populateDropdown = async (url, selectElement) => {
        try {
            const response = await fetch(url);
            const data = await response.json();
            const key = Object.keys(data)[0]; // e.g., 'languages' or 'providers'
            data[key].forEach(item => {
                const option = document.createElement('option');
                option.value = item;
                option.textContent = item;
                selectElement.appendChild(option);
            });
        } catch (error) {
            console.error(`Failed to load ${url}:`, error);
        }
    };

    populateDropdown('/supported-languages', languageSelect);
    populateDropdown('/supported-providers', providerSelect);

    // Handle analyze button click
    analyzeBtn.addEventListener('click', async () => {
        const requestBody = {
            language: languageSelect.value,
            provider: providerSelect.value,
            code: codeInput.value
        };

        resultsContainer.classList.add('hidden');
        resultsOutput.textContent = 'Analyzing...';

        try {
            const response = await fetch('/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(requestBody)
            });

            const result = await response.json();
            resultsOutput.textContent = JSON.stringify(result, null, 2);
            resultsContainer.classList.remove('hidden');

        } catch (error) {
            resultsOutput.textContent = `Error: ${error.message}`;
            resultsContainer.classList.remove('hidden');
        }
    });
});
