// API Configuration
const API_URL = 'http://localhost:8000';

// DOM Elements
const textInput = document.getElementById('textInput');
const analyzeBtn = document.getElementById('analyzeBtn');
const btnText = document.getElementById('btnText');
const btnLoader = document.getElementById('btnLoader');
const resultsSection = document.getElementById('resultsSection');
const predictionBadge = document.getElementById('predictionBadge');
const predictionText = document.getElementById('predictionText');
const confidencePercent = document.getElementById('confidencePercent');
const confidenceFill = document.getElementById('confidenceFill');
const toxicityPercent = document.getElementById('toxicityPercent');
const toxicityFill = document.getElementById('toxicityFill');
const analyzedText = document.getElementById('analyzedText');
const statusDot = document.getElementById('statusDot');
const statusText = document.getElementById('statusText');
const exampleButtons = document.querySelectorAll('.btn-example');

// Check API health on load
async function checkAPIHealth() {
    try {
        const response = await fetch(`${API_URL}/health`);
        const data = await response.json();

        if (data.status === 'ok') {
            statusDot.classList.add('online');
            statusDot.classList.remove('offline');
            statusText.textContent = data.model_loaded
                ? 'Model loaded & ready'
                : 'API online (mock mode)';
        }
    } catch (error) {
        statusDot.classList.add('offline');
        statusDot.classList.remove('online');
        statusText.textContent = 'API offline';
        console.error('API health check failed:', error);
    }
}

// Analyze text function
async function analyzeText() {
    const text = textInput.value.trim();

    if (!text) {
        alert('Please enter some text to analyze');
        return;
    }

    // Disable button and show loader
    analyzeBtn.disabled = true;
    btnText.classList.add('hidden');
    btnLoader.classList.remove('hidden');

    try {
        const response = await fetch(`${API_URL}/predict`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text: text })
        });

        if (!response.ok) {
            throw new Error('Prediction failed');
        }

        const data = await response.json();
        displayResults(data);

    } catch (error) {
        alert('Error: Could not connect to API. Make sure the FastAPI server is running on port 8000.');
        console.error('Prediction error:', error);
    } finally {
        // Re-enable button
        analyzeBtn.disabled = false;
        btnText.classList.remove('hidden');
        btnLoader.classList.add('hidden');
    }
}


// Add this new function after analyzeText()
async function rephraseText() {
    const text = textInput.value.trim();

    if (!text) {
        alert('Please enter some text to rephrase');
        return;
    }

    // Show loading state on rephrase button
    const rephraseBtn = document.getElementById('rephraseBtn');
    rephraseBtn.disabled = true;
    rephraseBtn.innerHTML = '<span class="loader"></span> Rephrasing...';

    try {
        const response = await fetch(`${API_URL}/rephrase`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text: text })
        });

        if (!response.ok) {
            throw new Error('Rephrasing failed');
        }

        const data = await response.json();
        displayRephraseResults(data);

    } catch (error) {
        alert('Error: Could not rephrase text. ' + error.message);
        console.error('Rephrase error:', error);
    } finally {
        rephraseBtn.disabled = false;
        rephraseBtn.innerHTML = '✨ Rephrase Text';
    }
}


// Display results
function displayResults(data) {
    // Show results section
    resultsSection.classList.remove('hidden');

    // Set prediction badge
    const isToxic = data.prediction === 'toxic';
    predictionText.textContent = isToxic ? 'TOXIC' : 'NON-TOXIC';
    predictionBadge.className = 'prediction-badge ' + (isToxic ? 'toxic' : 'non-toxic');

    // Set confidence score
    const confidence = (data.confidence * 100).toFixed(1);
    confidencePercent.textContent = `${confidence}%`;
    confidenceFill.style.width = `${confidence}%`;

    // Set toxicity probability
    const toxicity = (data.toxic_probability * 100).toFixed(1);
    toxicityPercent.textContent = `${toxicity}%`;
    toxicityFill.style.width = `${toxicity}%`;

    // Set analyzed text
    analyzedText.textContent = data.input;

    // Scroll to results
    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}


// Add this new function to display rephrase results
function displayRephraseResults(data) {
    const rephraseSection = document.getElementById('rephraseSection');

    if (!data.is_toxic) {
        // Show non-toxic message
        rephraseSection.classList.remove('hidden');
        rephraseSection.innerHTML = `
            <div class="result-card">
                <div class="prediction-badge non-toxic">
                    <span>✓ NON-TOXIC</span>
                </div>
                <p>${data.message}</p>
            </div>
        `;
        rephraseSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        return;
    }

    // Show rephrased result with examples
    const examplesHTML = data.retrieved_examples.map((ex, i) => `
        <div class="example-card">
            <div class="example-number">#${i + 1}</div>
            <div class="example-content">
                <p class="example-toxic"><strong>Toxic:</strong> ${ex.toxic}</p>
                <p class="example-professional"><strong>Professional:</strong> ${ex.professional}</p>
                <span class="example-category">${ex.category}</span>
            </div>
        </div>
    `).join('');

    rephraseSection.innerHTML = `
        <h2>✨ Rephrased Result</h2>
        <div class="result-card">
            <div class="rephrase-result">
                <h3>Original (Toxic):</h3>
                <p class="toxic-text">${data.input}</p>

                <div class="arrow-down">↓</div>

                <h3>Rephrased (Professional):</h3>
                <p class="professional-text">${data.rephrased}</p>
            </div>
        </div>

        <div class="examples-used">
            <h3>📚 Examples Used (Top ${data.num_examples_used})</h3>
            <div class="examples-grid">
                ${examplesHTML}
            </div>
        </div>
    `;

    rephraseSection.classList.remove('hidden');
    rephraseSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}


// Event Listeners
analyzeBtn.addEventListener('click', analyzeText);

textInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && e.ctrlKey) {
        analyzeText();
    }
});

// Example buttons
exampleButtons.forEach(btn => {
    btn.addEventListener('click', () => {
        textInput.value = btn.dataset.text;
        textInput.focus();
    });
});

// Check API health on page load
checkAPIHealth();
