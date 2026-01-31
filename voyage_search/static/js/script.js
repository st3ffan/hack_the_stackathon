// DOM Elements
const searchForm = document.getElementById('searchForm');
const searchInput = document.getElementById('searchInput');
const loadingState = document.getElementById('loadingState');
const errorState = document.getElementById('errorState');
const resultsSection = document.getElementById('resultsSection');
const resultsGrid = document.getElementById('resultsGrid');
const resultsCount = document.querySelector('.results-count');
const errorMessage = document.querySelector('.error-message');
const exampleChips = document.querySelectorAll('.example-chip');

// State
let isSearching = false;

// Event Listeners
searchForm.addEventListener('submit', handleSearch);

exampleChips.forEach(chip => {
    chip.addEventListener('click', () => {
        const query = chip.dataset.query;
        searchInput.value = query;
        handleSearch(new Event('submit'));
    });
});

// Main search handler
async function handleSearch(e) {
    e.preventDefault();
    
    if (isSearching) return;
    
    const query = searchInput.value.trim();
    if (!query) return;
    
    isSearching = true;
    
    // Hide previous states
    hideAllStates();
    
    // Show loading
    loadingState.classList.remove('hidden');
    
    try {
        const response = await fetch('/search', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ query })
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Search failed');
        }
        
        displayResults(data);
        
    } catch (error) {
        console.error('Search error:', error);
        showError(error.message || 'An error occurred during search');
    } finally {
        isSearching = false;
        loadingState.classList.add('hidden');
    }
}

// Display search results
function displayResults(data) {
    if (!data.results || data.results.length === 0) {
        showError('No results found. Try a different query.');
        return;
    }
    
    // Clear previous results
    resultsGrid.innerHTML = '';
    
    // Update results count
    resultsCount.textContent = `${data.count} result${data.count !== 1 ? 's' : ''}`;
    
    // Create result cards
    data.results.forEach((result, index) => {
        const card = createResultCard(result, index);
        resultsGrid.appendChild(card);
    });
    
    // Show results section
    resultsSection.classList.remove('hidden');
    
    // Smooth scroll to results
    setTimeout(() => {
        resultsSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }, 100);
}

// Create a result card
function createResultCard(result, index) {
    const card = document.createElement('div');
    card.className = 'result-card';
    card.style.animationDelay = `${index * 0.05}s`;
    
    const imageWrapper = document.createElement('div');
    imageWrapper.className = 'result-image-wrapper';
    
    if (result.image_data) {
        const img = document.createElement('img');
        img.className = 'result-image';
        img.src = result.image_data;
        img.alt = result.filename || result.name;
        img.loading = 'lazy';
        imageWrapper.appendChild(img);
    } else {
        const placeholder = document.createElement('div');
        placeholder.className = 'result-placeholder';
        placeholder.textContent = '◉';
        imageWrapper.appendChild(placeholder);
    }
    
    const info = document.createElement('div');
    info.className = 'result-info';
    
    const filename = document.createElement('div');
    filename.className = 'result-filename';
    filename.textContent = result.filename || result.name || 'Untitled';
    
    const score = document.createElement('div');
    score.className = 'result-score';
    
    const scoreLabel = document.createElement('span');
    scoreLabel.className = 'result-score-label';
    scoreLabel.textContent = 'Similarity:';
    
    const scoreValue = document.createElement('span');
    scoreValue.textContent = result.score ? result.score.toFixed(4) : 'N/A';
    
    score.appendChild(scoreLabel);
    score.appendChild(scoreValue);
    
    info.appendChild(filename);
    info.appendChild(score);
    
    card.appendChild(imageWrapper);
    card.appendChild(info);
    
    return card;
}

// Show error message
function showError(message) {
    errorMessage.textContent = message;
    errorState.classList.remove('hidden');
}

// Hide all state sections
function hideAllStates() {
    loadingState.classList.add('hidden');
    errorState.classList.add('hidden');
    resultsSection.classList.add('hidden');
}

// Auto-focus on search input
searchInput.focus();
