// Cache refresh: 1772785544.1242313
// Global state
let currentResults = [];
let currentCountry = 'IN';  // Default to India
let currentCurrency = 'Rs.';
let displayedResults = 12;

let currentPage = 1;
let totalPages = 1;
let currentSearchParams = {};
let currentBanners = {};  // Store banners for products
let currentSuggestions = [];  // Store AI suggestions

// API Base URL
const API_BASE = '';

// Country data with flags
const COUNTRIES = {
    'IN': { name: 'India', flag: '', currency: 'Rs.' },
    'US': { name: 'United States', flag: '', currency: '$' },
    'GB': { name: 'United Kingdom', flag: '', currency: '' },
    'DE': { name: 'Germany', flag: '', currency: '' },
    'FR': { name: 'France', flag: '', currency: '' },
    'CA': { name: 'Canada', flag: '', currency: 'C$' },
    'AU': { name: 'Australia', flag: '', currency: 'A$' }
};

// Detect country from IP using free API
async function detectCountry() {
    try {
        const response = await fetch('https://ipapi.co/json/');
        const data = await response.json();
        const countryCode = data.country_code || 'IN';
        
        if (COUNTRIES[countryCode]) {
            currentCountry = countryCode;
            currentCurrency = COUNTRIES[countryCode].currency;
            updateCountryDisplay();
        }
    } catch (error) {
        console.log('Geolocation detection failed, using default India');
        updateCountryDisplay();
    }
}

// Update country display
function updateCountryDisplay() {
    const country = COUNTRIES[currentCountry] || COUNTRIES['IN'];
    document.getElementById('countryFlag').textContent = country.flag;
    document.getElementById('countryName').textContent = country.name;
}



// Quick search from suggestion chips
function quickSearch(query) {
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        searchInput.value = query;
        performSearch();
    }
}

// Initialize app
document.addEventListener('DOMContentLoaded', () => {
    detectCountry();
    setupEventListeners();
    console.log('App initialized');
});

// Load countries
async function loadCountries() {
    try {
        const response = await fetch(`${API_BASE}/api/countries`);
        const data = await response.json();
        
        if (data.success) {
            populateCountrySelect(data.countries);
        }
    } catch (error) {
        console.error('Error loading countries:', error);
        showNotification('Failed to load countries', 'error');
    }
}

// Populate country dropdown
function populateCountrySelect(countries) {
    const select = document.getElementById('countrySelect');
    select.innerHTML = '<option value="">Select a country...</option>';
    
    countries.forEach(country => {
        const option = document.createElement('option');
        option.value = country.code;
        option.textContent = `${country.name} (${country.currency})`;
        if (country.code === 'US') option.selected = true;
        select.appendChild(option);
    });
}

// Setup event listeners
function setupEventListeners() {
    // Search
    const searchBtn = document.getElementById('searchBtn');
    const searchInput = document.getElementById('searchInput');
    const aiResponseClose = document.getElementById('aiResponseClose');
    const countryBadge = document.getElementById('countryBadge');
    
    if (searchBtn) {
        searchBtn.addEventListener('click', performSearch);
    }
    
    if (searchInput) {
        searchInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') performSearch();
        });
    }
    
    if (aiResponseClose) {
        aiResponseClose.addEventListener('click', () => {
            document.getElementById('aiResponseWindow').style.display = 'none';
        });
    }
    
    if (countryBadge) {
        countryBadge.addEventListener('click', () => {
            alert('Country selection coming soon! Currently using: ' + (COUNTRIES[currentCountry] || COUNTRIES['IN']).name);
        });
    }
}

// Budget input handlers
function onBudgetInput(e) {
    const clearBtn = document.getElementById('budgetClear');
    if (e.target.value) {
        clearBtn.style.display = 'flex';
    } else {
        clearBtn.style.display = 'none';
    }
}

function clearBudget() {
    document.getElementById('budgetInput').value = '';
    document.getElementById('budgetClear').style.display = 'none';
}

// Country change handler
async function onCountryChange(e) {
    currentCountry = e.target.value;
    
    if (!currentCountry) return;
    
    try {
        const response = await fetch(`${API_BASE}/api/marketplaces/${currentCountry}`);
        const data = await response.json();
        
        if (data.success) {
            currentCurrency = data.currency_symbol;
            showCountryInfo(data);
        }
    } catch (error) {
        console.error('Error loading marketplaces:', error);
    }
}

// Show country info
function showCountryInfo(data) {
    const infoDiv = document.getElementById('countryInfo');
    infoDiv.innerHTML = `
        <strong>${data.currency} ${data.currency_symbol}</strong> • 
        ${data.marketplaces.length} marketplaces: 
        ${data.marketplaces.slice(0, 3).map(m => m.name).join(', ')}
        ${data.marketplaces.length > 3 ? '...' : ''}
    `;
    infoDiv.classList.add('active');
    
    // Update currency prefix in budget input
    document.getElementById('currencyPrefix').textContent = data.currency_symbol;
}

// Perform search
function displayResults(data) {
    hideLoading();
    
    if (data.results.length === 0) {
        showEmpty();
        return;
    }
    
    // Update header
    document.getElementById('resultsTitle').textContent = `Results for "${data.query}"`;
    document.getElementById('resultsMeta').textContent = 
        `${data.total_results} products found in ${data.country_name}`;
    
    // Show controls and results
    document.getElementById('controlsSection').style.display = 'block';
    document.getElementById('resultsSection').style.display = 'block';
    
    // Render products
    renderProducts(data.results.slice(0, displayedResults));
    
    // Scroll to budget analysis if present, otherwise to results
    if (document.getElementById('budgetAnalysisSection').style.display === 'block') {
        document.getElementById('budgetAnalysisSection').scrollIntoView({ behavior: 'smooth' });
    } else {
        document.getElementById('resultsSection').scrollIntoView({ behavior: 'smooth' });
    }
}

// Display budget analysis
function displayBudgetAnalysis(analysis) {
    const section = document.getElementById('budgetAnalysisSection');
    const card = document.getElementById('budgetCard');
    
    let html = `
        <div class="budget-header">
            <div class="budget-title">
                💰 Budget Analysis
            </div>
            <div class="budget-amount">${analysis.currency_symbol}${analysis.budget.toFixed(2)}</div>
        </div>
        
        <div class="budget-stats">
            <div class="budget-stat">
                <div class="budget-stat-label">Products in Budget</div>
                <div class="budget-stat-value">${analysis.products_in_budget}</div>
            </div>
            <div class="budget-stat">
                <div class="budget-stat-label">Average Score</div>
                <div class="budget-stat-value">${analysis.avg_score}/100</div>
            </div>
            <div class="budget-stat">
                <div class="budget-stat-label">Budget Quality</div>
                <div class="budget-quality-badge" style="background-color: ${analysis.quality_color}; color: white;">
                    ${analysis.quality_label}
                </div>
            </div>
        </div>
    `;
    
    // Add warning if present
    if (analysis.warning) {
        html += `
            <div class="budget-warning ${analysis.warning.type}">
                <div class="budget-warning-icon">${analysis.warning.title.split(' ')[0]}</div>
                <div class="budget-warning-content">
                    <div class="budget-warning-title">${analysis.warning.title}</div>
                    <div class="budget-warning-message">${analysis.warning.message}</div>
                </div>
            </div>
        `;
    }
    
    // Add recommendations if present
    if (analysis.has_recommendations && analysis.recommended_products) {
        html += `
            <div class="budget-recommendation">
                <div class="budget-recommendation-header">
                    <div class="budget-recommendation-icon">💡</div>
                    <div class="budget-recommendation-title">Smart Recommendation</div>
                </div>
                <div class="budget-recommendation-content">${analysis.upgrade_message}</div>
                <div class="budget-recommendation-products">
        `;
        
        analysis.recommended_products.forEach(product => {
            html += `
                <div class="budget-recommendation-product" onclick="window.open('${product.url}', '_blank')">
                    <div class="budget-recommendation-product-title">${escapeHtml(product.title)}</div>
                    <div class="budget-recommendation-product-details">
                        <div class="budget-recommendation-product-price">
                            ${analysis.currency_symbol}${product.price.toFixed(2)}
                            <span style="font-size: 14px; color: var(--text-secondary);">
                                (+${analysis.currency_symbol}${product.price_diff.toFixed(2)})
                            </span>
                        </div>
                        <div class="budget-recommendation-product-improvement">
                            <span>↑ ${product.score_improvement.toFixed(0)} points</span>
                            <span style="font-weight: 600;">${product.score}/100</span>
                        </div>
                    </div>
                </div>
            `;
        });
        
        html += `
                </div>
            </div>
        `;
    }
    
    // Add savings message if present
    if (analysis.savings_message) {
        html += `
            <div class="budget-savings">
                <div class="budget-savings-header">
                    <div class="budget-savings-icon">💰</div>
                    <div class="budget-savings-title">Savings Opportunity</div>
                </div>
                <div class="budget-savings-content">${analysis.savings_message}</div>
            </div>
        `;
    }
    
    card.innerHTML = html;
    section.style.display = 'block';
}

// Render products
function renderProducts(products) {
    const grid = document.getElementById('resultsGrid');
    grid.innerHTML = '';
    
    products.forEach((product, index) => {
        const card = createProductCard(product, index + 1);
        grid.appendChild(card);
    });
}

// Create product card
function createProductCard(product, rank) {
    const card = document.createElement('div');
    card.className = product.is_best_value ? 'product-card best-value' : 'product-card';
    
    const rankClass = rank <= 3 ? `top-${rank}` : '';
    const rankBadge = rank === 1 ? '🥇' : rank === 2 ? '🥈' : rank === 3 ? '🥉' : `#${rank}`;
    
    const stars = product.product_rating ? '⭐'.repeat(Math.round(product.product_rating)) : '';
    
    // Check if product has a banner
    const productName = product.name || product.title;
    const banner = currentBanners[productName];
    
    
    card.innerHTML = `
        ${product.is_best_value ? '<div class="best-value-badge">Best Value</div>' : ''}
        
        ${banner ? `
            <div class="smart-banner ${banner.type}">
                <div class="smart-banner-message">${banner.message}</div>
                ${banner.details && banner.details.length > 0 ? `
                    <div class="smart-banner-details">${banner.details.join('  ')}</div>
                ` : ''}
            </div>
        ` : ''}
        
        <div class="product-rank ${rankClass}">
            <span>${rankBadge}</span>
            <span>Score: ${product.overall_rank}/100</span>
        </div>
        
        
        ${product.image_url ? `
            <img src="${escapeHtml(product.image_url)}" alt="${escapeHtml(product.title)}" class="product-image" onerror="this.style.display='none'">
        ` : ''}
        
        <h3 class="product-title">${escapeHtml(product.title)}</h3>
        
        
        ${product.description ? `
            <p class="product-description">${escapeHtml(product.description)}</p>
        ` : ''}
        
        <div class="product-price">${currentCurrency}${product.price.toFixed(2)}</div>
        
        <div class="product-source">
            <span>🏪</span>
            <span>${escapeHtml(product.source)}</span>
        </div>
        
        ${product.product_rating ? `
            <div class="product-rating">
                <span class="stars">${stars}</span>
                <span>${product.product_rating.toFixed(1)}/5.0</span>
                <span class="review-count">(${product.review_count} reviews)</span>
            </div>
        ` : ''}
        
        <div class="product-scores">
            <div class="score-item">
                <span class="score-label">🛡️ Trust</span>
                <div class="score-bar">
                    <div class="score-fill" style="width: ${product.trust_score}%"></div>
                </div>
                <span class="score-value">${product.trust_score}</span>
            </div>
            
            <div class="score-item">
                <span class="score-label">✨ Quality</span>
                <div class="score-bar">
                    <div class="score-fill" style="width: ${product.quality_score}%"></div>
                </div>
                <span class="score-value">${product.quality_score}</span>
            </div>
            
            <div class="score-item">
                <span class="score-label">💎 Value</span>
                <div class="score-bar">
                    <div class="score-fill" style="width: ${product.value_score}%"></div>
                </div>
                <span class="score-value">${product.value_score}</span>
            </div>
        </div>
        
        <a href="${escapeHtml(product.url)}" target="_blank" class="product-link" onclick="event.stopPropagation()">
            View Product →
        </a>
    `;
    
    return card;
}

// Sort change handler
async function onSortChange(e) {
    const sortBy = e.target.value;
    
    if (currentResults.length === 0) return;
    
    try {
        const response = await fetch(`${API_BASE}/api/sort`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                results: currentResults,
                sort_by: sortBy,
                order: 'desc'
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            currentResults = data.sorted_results;
            renderProducts(currentResults.slice(0, displayedResults));
        }
    } catch (error) {
        console.error('Sort error:', error);
        showNotification('Failed to sort results', 'error');
    }
}

// Show filter modal
function showFilterModal(filterType) {
    const modal = document.getElementById('filterModal');
    const title = document.getElementById('modalTitle');
    const body = document.getElementById('modalBody');
    
    let content = '';
    
    if (filterType === 'price') {
        title.textContent = 'Filter by Price Range';
        content = `
            <div class="form-group">
                <label class="form-label">Minimum Price (${currentCurrency})</label>
                <input type="number" id="minPrice" class="form-input" placeholder="0" min="0">
            </div>
            <div class="form-group">
                <label class="form-label">Maximum Price (${currentCurrency})</label>
                <input type="number" id="maxPrice" class="form-input" placeholder="10000" min="0">
            </div>
        `;
    } else if (filterType === 'rating') {
        title.textContent = 'Filter by Minimum Rating';
        content = `
            <div class="form-group">
                <label class="form-label">Minimum Rating</label>
                <input type="number" id="minRating" class="form-input" placeholder="4.0" min="0" max="5" step="0.1">
            </div>
        `;
    } else if (filterType === 'source') {
        const sources = [...new Set(currentResults.map(r => r.source))];
        title.textContent = 'Filter by Marketplace';
        content = `
            <div class="form-group">
                <label class="form-label">Select Marketplace</label>
                <select id="sourceSelect" class="form-input">
                    <option value="">All Marketplaces</option>
                    ${sources.map(s => `<option value="${s}">${s}</option>`).join('')}
                </select>
            </div>
        `;
    }
    
    body.innerHTML = content;
    modal.style.display = 'flex';
    modal.dataset.filterType = filterType;
}

// Apply filter
async function applyFilter() {
    const filterType = document.getElementById('filterModal').dataset.filterType;
    let filterValue = {};
    
    if (filterType === 'price') {
        const min = parseFloat(document.getElementById('minPrice').value) || 0;
        const max = parseFloat(document.getElementById('maxPrice').value) || Infinity;
        filterValue = { min, max };
    } else if (filterType === 'rating') {
        const min = parseFloat(document.getElementById('minRating').value) || 0;
        filterValue = { min };
    } else if (filterType === 'source') {
        const source = document.getElementById('sourceSelect').value;
        filterValue = { source };
    }
    
    try {
        const response = await fetch(`${API_BASE}/api/filter`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                results: currentResults,
                filter_type: filterType,
                filter_value: filterValue
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            renderProducts(data.filtered_results.slice(0, displayedResults));
            showNotification(`Filtered to ${data.count} results`, 'success');
            closeModal();
        }
    } catch (error) {
        console.error('Filter error:', error);
        showNotification('Failed to apply filter', 'error');
    }
}

// Modal controls
function closeModal() {
    document.getElementById('filterModal').style.display = 'none';
}

function showAboutModal() {
    document.getElementById('aboutModal').style.display = 'flex';
}

function closeAboutModal() {
    document.getElementById('aboutModal').style.display = 'none';
}

// UI state functions
function showLoading() {
    document.getElementById('loadingState').style.display = 'block';
}

function hideLoading() {
    document.getElementById('loadingState').style.display = 'none';
}

function showResults() {
    document.getElementById('resultsSection').style.display = 'block';
}

function hideResults() {
    document.getElementById('resultsSection').style.display = 'none';
}

function showEmpty() {
    document.getElementById('emptyState').style.display = 'block';
}

function hideEmpty() {
    document.getElementById('emptyState').style.display = 'none';
}

function hideBudgetAnalysis() {
    document.getElementById('budgetAnalysisSection').style.display = 'none';
}

// Notification system
function showNotification(message, type = 'info') {
    // Simple console notification for now
    // Can be enhanced with toast notifications
    console.log(`[${type.toUpperCase()}] ${message}`);
    
    // You can add a toast library here for better UX
    alert(message);
}

// Utility functions
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}


// AI Filter Functions
let originalResults = [];
let aiFilterActive = false;

function applyAIFilter() {
    const filterText = document.getElementById('aiFilterInput').value.trim().toLowerCase();
    
    if (!filterText) {
        showNotification('Please enter a filter query', 'warning');
        return;
    }
    
    // Store original results if first time filtering
    if (!aiFilterActive) {
        originalResults = [...currentResults];
    }
    
    // Filter products based on AI query
    const filtered = originalResults.filter(product => {
        // Search in title, description, and source
        const searchText = `${product.title} ${product.description || ''} ${product.source || ''}`.toLowerCase();
        
        // Extract keywords from filter query (remove common words)
        const commonWords = ['show', 'with', 'the', 'all', 'phones', 'phone', 'mobile', 'products'];
        const keywords = filterText.split(' ')
            .filter(w => w.length > 2 && !commonWords.includes(w));
        
        // If no valid keywords, search for the whole phrase
        if (keywords.length === 0) {
            return searchText.includes(filterText);
        }
        
        // Check if product matches ALL keywords (AND logic)
        return keywords.every(keyword => searchText.includes(keyword));
    });
    
    if (filtered.length === 0) {
        showNotification(`No products found matching "${filterText}". Try simpler keywords like "5G", "pro", "ultra", or brand names.`, 'warning');
        return;
    }
    
    // Update display
    currentResults = filtered;
    renderProducts(currentResults);
    
    // Show active filter badge
    document.getElementById('aiFilterActive').style.display = 'flex';
    document.getElementById('aiFilterActiveText').textContent = filterText;
    document.getElementById('aiFilterClear').style.display = 'block';
    
    aiFilterActive = true;
    
    showNotification(`Found ${filtered.length} products matching "${filterText}"`, 'success');
}

function clearAIFilter() {
    if (!aiFilterActive) return;
    
    // Restore original results
    currentResults = [...originalResults];
    renderProducts(currentResults);
    
    // Clear UI
    document.getElementById('aiFilterInput').value = '';
    document.getElementById('aiFilterActive').style.display = 'none';
    document.getElementById('aiFilterClear').style.display = 'none';
    
    aiFilterActive = false;
    originalResults = [];
    
    showNotification('Filter cleared', 'success');
}




// Regular search function
async function performRegularSearch(query, budget) {
    currentSearchParams = {
        query: query,
        country_code: currentCountry,
        budget: budget ? parseFloat(budget) : null,
        page: 1,
        per_page: 20,
        sort_by: 'overall_rank',
        sort_order: 'desc'
    };
    
    performSearchWithPagination(currentSearchParams);
}

// Close AI response window
document.addEventListener('DOMContentLoaded', () => {
    const closeBtn = document.getElementById('aiResponseClose');
    if (closeBtn) {
        closeBtn.addEventListener('click', () => {
            document.getElementById('aiResponseWindow').style.display = 'none';
        });
    }
});


// Smart Query Parser - Extract search term and budget from natural language
function parseNaturalQuery(query) {
    const lowerQuery = query.toLowerCase();
    
    // Extract budget patterns
    let budget = null;
    const budgetPatterns = [
        /under\s+(\d+)k/i,           // "under 20k"
        /under\s+(\d+)/i,            // "under 20000"
        /below\s+(\d+)k/i,           // "below 25k"
        /below\s+(\d+)/i,            // "below 25000"
        /budget\s+(\d+)k/i,          // "budget 30k"
        /budget\s+(\d+)/i,           // "budget 30000"
        /around\s+(\d+)k/i,          // "around 15k"
        /around\s+(\d+)/i,           // "around 15000"
        /(\d+)k\s+budget/i,          // "20k budget"
        /(\d+)\s+budget/i            // "20000 budget"
    ];
    
    for (const pattern of budgetPatterns) {
        const match = query.match(pattern);
        if (match) {
            budget = parseInt(match[1]);
            // If it's in 'k' format, multiply by 1000
            if (pattern.source.includes('k')) {
                budget = budget * 1000;
            }
            break;
        }
    }
    
    // Extract product keywords (order matters - check longer/specific terms first)
    const productKeywords = [
        'headphone', 'earphone', 'earbud', 'airpod',
        'smartphone', 'mobile', 'phone',
        'laptop', 'computer', 'notebook',
        'watch', 'smartwatch',
        'tablet', 'ipad',
        'camera', 'dslr',
        'speaker', 'bluetooth',
        'charger', 'powerbank',
        'mouse', 'keyboard',
        'monitor', 'display',
        'tv', 'television'
    ];
    
    let searchTerm = '';
    for (const keyword of productKeywords) {
        if (lowerQuery.includes(keyword)) {
            searchTerm = keyword;
            break;
        }
    }
    
    // If no keyword found, extract main words (remove common words)
    if (!searchTerm) {
        const commonWords = ['i', 'need', 'want', 'looking', 'for', 'a', 'an', 'the', 'under', 'below', 'around', 'budget'];
        const words = query.toLowerCase().split(/\s+/).filter(w => !commonWords.includes(w) && !/\d/.test(w));
        searchTerm = words[0] || query;
    }
    
    return { searchTerm, budget };
}




// AI Chat Integration with Smart Fallback
async function performSearch() {
    const query = document.getElementById('searchInput').value.trim();
    
    if (!query) {
        alert('Please enter a search term');
        return;
    }
    
    // Parse query for budget FIRST
    const parsed = parseNaturalQuery(query);
    
    // Show AI response window
    const aiWindow = document.getElementById('aiResponseWindow');
    const aiText = document.getElementById('aiResponseText');
    const aiStatus = document.getElementById('aiResponseStatus');
    
    aiWindow.style.display = 'block';
    aiText.textContent = 'Let me help you find that...';
    aiStatus.style.display = 'flex';
    
    try {
        // Call AI chat API
        const aiResponse = await fetch('/api/ai/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                message: query,
                context: {
                    budget: parsed.budget,
                    country_code: currentCountry
                }
            })
        });
        
        const aiData = await aiResponse.json();
        
        if (aiData.success && aiData.response) {
            aiText.textContent = aiData.response;
            aiStatus.style.display = 'none';
            
            // Check if AI wants to redirect (for mobile searches)
            if (aiData.redirect && aiData.redirect_url) {
                setTimeout(() => {
                    window.location.href = aiData.redirect_url;
                }, 1000);
                return;
            }
            
            // If AI found products, show them
            if (aiData.products && aiData.products.length > 0) {
                // Store banners and suggestions
                currentBanners = aiData.banners || {};
                currentSuggestions = aiData.suggestions || [];
                
                // Show AI suggestions if available
                if (currentSuggestions.length > 0) {
                    aiText.innerHTML = currentSuggestions.join('<br>');
                }
                
                // Display products immediately
                displayResults({
                    results: aiData.products,
                    query: query,
                    total_results: aiData.products.length
                });
                // Keep AI window open for personalization
                return;
            }
        }
        
        // AI failed or denied - use smart fallback
        aiText.textContent = "I'm having a bit of trouble with fancy searches right now, but let me get that data straight to you! ";
        
        // Use already parsed query
        const finalBudget = parsed.budget;
        
        // Check if mobile search - redirect to mobile CPI page (exclude headphone/earphone)
        const queryLower = query.toLowerCase();
        const isHeadphone = queryLower.includes('headphone') || queryLower.includes('earphone') || queryLower.includes('earbud') || queryLower.includes('airpod');
        const mobileKeywords = ['phone', 'mobile', 'smartphone', 'iphone', 'samsung'];
        const isMobileSearch = !isHeadphone && mobileKeywords.some(k => queryLower.includes(k));
        
        if (isMobileSearch) {
            // Pass the ORIGINAL query to preserve battery/camera/RAM specs
            let redirectUrl = `/mobile?query=${encodeURIComponent(query)}`;
            if (finalBudget) {
                redirectUrl += `&budget=${finalBudget}`;
            }
            console.log('Redirecting to mobile page with full query:', query, 'budget:', finalBudget);
            setTimeout(() => window.location.href = redirectUrl, 800);
            return;
        }
        
        // Regular search for non-mobile items - keep AI window open
        setTimeout(() => {
            performRegularSearch(parsed.searchTerm, finalBudget);
            // AI window stays open for follow-up questions
        }, 800);
        
    } catch (error) {
        console.error('AI chat error:', error);
        
        // Fallback with friendly message
        aiText.textContent = "I'm having a bit of trouble with fancy searches right now, but let me get that data straight to you! ";
        
        // Use already parsed query (no redeclaration needed)
        const finalBudget = parsed.budget;
        
        // Check if mobile search - redirect to mobile CPI page (exclude headphone/earphone)
        const queryLower = query.toLowerCase();
        const isHeadphone = queryLower.includes('headphone') || queryLower.includes('earphone') || queryLower.includes('earbud') || queryLower.includes('airpod');
        const mobileKeywords = ['phone', 'mobile', 'smartphone', 'iphone', 'samsung'];
        const isMobileSearch = !isHeadphone && mobileKeywords.some(k => queryLower.includes(k));
        
        if (isMobileSearch) {
            // Pass the ORIGINAL query to preserve battery/camera/RAM specs
            let redirectUrl = `/mobile?query=${encodeURIComponent(query)}`;
            if (finalBudget) {
                redirectUrl += `&budget=${finalBudget}`;
            }
            console.log('Redirecting to mobile page with full query:', query, 'budget:', finalBudget);
            setTimeout(() => window.location.href = redirectUrl, 800);
            return;
        }
        
        // Regular search for non-mobile items - keep AI window open
        setTimeout(() => {
            performRegularSearch(parsed.searchTerm, finalBudget);
            // AI window stays open for follow-up questions
        }, 800);
    }
}



// Simplified display functions for minimal UI
function showLoading() {
    const aiWindow = document.getElementById('aiResponseWindow');
    const aiStatus = document.getElementById('aiResponseStatus');
    if (aiWindow) aiWindow.style.display = 'block';
    if (aiStatus) aiStatus.style.display = 'block';
}

function hideLoading() {
    const aiStatus = document.getElementById('aiResponseStatus');
    if (aiStatus) aiStatus.style.display = 'none';
}

function displayResults(data) {
    hideLoading();
    
    const resultsSection = document.getElementById('resultsSection');
    const resultsGrid = document.getElementById('resultsGrid');
    const aiText = document.getElementById('aiResponseText');
    
    if (!data.results || data.results.length === 0) {
        if (aiText) aiText.textContent = 'No products found. Try a different search term.';
        return;
    }
    
    // Update AI response
    if (aiText) aiText.textContent = `Found ${data.results.length} products for "${data.query}"`;
    
    // Show results section
    if (resultsSection) resultsSection.style.display = 'block';
    
    // Clear and populate results grid
    if (resultsGrid) {
        resultsGrid.innerHTML = '';
        data.results.slice(0, 12).forEach(product => {
            const card = document.createElement('div');
            card.className = 'product-card';
            card.innerHTML = `
                <h3 class="product-title">${escapeHtml(product.title)}</h3>
                <div class="product-price">${currentCurrency}${product.price.toFixed(2)}</div>
                <div style="font-size:14px;color:#666;margin-bottom:12px;">
                    Score: ${product.overall_rank}/100 | ${product.source}
                </div>
                <a href="${escapeHtml(product.url)}" target="_blank" class="product-link">
                    View Product 
                </a>
            `;
            resultsGrid.appendChild(card);
        });
        
        // Scroll to results
        resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
}

function showError(message) {
    const aiText = document.getElementById('aiResponseText');
    if (aiText) aiText.textContent = message;
    hideLoading();
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Pagination and Sorting Functions
function applySorting() {
    const sortBy = document.getElementById('sortBy').value;
    let sortField = sortBy;
    let sortOrder = 'desc';
    
    if (sortBy === 'price_low') {
        sortField = 'price';
        sortOrder = 'asc';
    } else if (sortBy === 'price_high') {
        sortField = 'price';
        sortOrder = 'desc';
    }
    
    currentSearchParams.sort_by = sortField;
    currentSearchParams.sort_order = sortOrder;
    currentPage = 1;
    currentSearchParams.page = 1;
    performSearchWithPagination(currentSearchParams);
}

function goToPage(page) {
    if (page < 1 || page > totalPages) return;
    currentPage = page;
    currentSearchParams.page = page;
    performSearchWithPagination(currentSearchParams);
}

async function performSearchWithPagination(params) {
    showLoading();
    
    try {
        const response = await fetch('/api/search', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(params)
        });
        
        const data = await response.json();
        
        if (data.success) {
            displayResultsWithPagination(data);
            updatePagination(data.page, data.total_pages, data.total_results);
            document.getElementById('sortingControls').style.display = 'block';
        } else {
            showError(data.error || 'Search failed');
        }
    } catch (error) {
        showError('Network error: ' + error.message);
    }
}

function displayResultsWithPagination(data) {
    hideLoading();
    
    const resultsSection = document.getElementById('resultsSection');
    const resultsGrid = document.getElementById('resultsGrid');
    const aiText = document.getElementById('aiResponseText');
    
    if (!data.results || data.results.length === 0) {
        if (aiText) aiText.textContent = 'No products found. Try a different search term.';
        return;
    }
    
    // Update AI response
    if (aiText) aiText.textContent = `Found ${data.total_results} products for "${data.query}" (Page ${data.page} of ${data.total_pages})`;
    
    // Show results section
    if (resultsSection) resultsSection.style.display = 'block';
    
    // Clear and populate results grid
    if (resultsGrid) {
        resultsGrid.innerHTML = '';
        data.results.forEach(product => {
            const card = document.createElement('div');
            card.className = 'product-card';
            card.innerHTML = `
                <h3 class="product-title">${escapeHtml(product.title)}</h3>
                <div class="product-price">${currentCurrency}${product.price.toFixed(2)}</div>
                <div style="font-size:14px;color:#666;margin-bottom:12px;">
                    Score: ${product.overall_rank}/100 | ${product.source}
                </div>
                <a href="${escapeHtml(product.url)}" target="_blank" class="product-link">
                    View Product 
                </a>
            `;
            resultsGrid.appendChild(card);
        });
        
        // Scroll to results
        resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
}

function updatePagination(page, pages, total) {
    currentPage = page;
    totalPages = pages;
    
    const paginationControls = document.getElementById('paginationControls');
    const pageInfo = document.getElementById('pageInfo');
    const resultsCount = document.getElementById('resultsCount');
    const firstPage = document.getElementById('firstPage');
    const prevPage = document.getElementById('prevPage');
    const nextPage = document.getElementById('nextPage');
    const lastPage = document.getElementById('lastPage');
    
    if (pages > 1) {
        paginationControls.style.display = 'block';
        pageInfo.textContent = 'Page ' + page + ' of ' + pages;
        
        firstPage.disabled = (page === 1);
        prevPage.disabled = (page === 1);
        nextPage.disabled = (page === pages);
        lastPage.disabled = (page === pages);
        
        [firstPage, prevPage, nextPage, lastPage].forEach(btn => {
            if (btn.disabled) {
                btn.style.opacity = '0.5';
                btn.style.cursor = 'not-allowed';
            } else {
                btn.style.opacity = '1';
                btn.style.cursor = 'pointer';
            }
        });
    } else {
        paginationControls.style.display = 'none';
    }
    
    if (resultsCount) {
        resultsCount.textContent = total + ' results found';
    }
}



// Interactive Chat Functions
let chatHistory = [];

function clearAIChat() {
    chatHistory = [];
    const aiChatMessages = document.getElementById('aiChatMessages');
    const aiResponseText = document.getElementById('aiResponseText');
    if (aiResponseText) {
        aiResponseText.textContent = '';
    }
    if (aiChatMessages) {
        aiChatMessages.innerHTML = '<div id="aiResponseText" style="padding: 12px; background: #f8f9fa; border-radius: 8px; margin-bottom: 10px; color: #333;"></div>';
    }
}

function addChatMessage(message, isUser = false) {
    chatHistory.push({ message, isUser, timestamp: new Date() });
    const aiChatMessages = document.getElementById('aiChatMessages');
    if (!aiChatMessages) return;
    
    const messageDiv = document.createElement('div');
    messageDiv.style.cssText = `
        margin-bottom: 10px;
        padding: 12px;
        border-radius: 8px;
        ${isUser ? 
            'background: #e3f2fd; color: #1976d2; text-align: right; margin-left: 40px;' : 
            'background: #f8f9fa; color: #333; margin-right: 40px;'}
    `;
    messageDiv.textContent = message;
    aiChatMessages.appendChild(messageDiv);
    aiChatMessages.scrollTop = aiChatMessages.scrollHeight;
}

async function askAI(question) {
    const aiFollowUpInput = document.getElementById('aiFollowUpInput');
    if (aiFollowUpInput) {
        aiFollowUpInput.value = question;
    }
    await sendAIFollowUp();
}

async function sendAIFollowUp() {
    const input = document.getElementById('aiFollowUpInput');
    const question = input.value.trim();
    
    if (!question) return;
    
    addChatMessage(question, true);
    input.value = '';
    
    const aiStatus = document.getElementById('aiResponseStatus');
    if (aiStatus) {
        aiStatus.style.display = 'block';
        aiStatus.innerHTML = '<span></span> Thinking...';
    }
    
    try {
        const context = {
            currentQuery: currentSearchParams?.query || '',
            budget: currentSearchParams?.price_max || 0,
            country: currentCountry,
            chatHistory: chatHistory.slice(-5)
        };
        
        const response = await fetch('/api/ai/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                message: question,
                context: context
            })
        });
        
        const data = await response.json();
        
        if (aiStatus) aiStatus.style.display = 'none';
        
        if (data.success) {
            addChatMessage(data.response);
            
            if (data.action === 'search' && data.params) {
                setTimeout(() => {
                    if (data.params.query) {
                        currentSearchParams = {
                            ...currentSearchParams,
                            ...data.params,
                            page: 1
                        };
                        performSearch(data.params.query);
                    }
                }, 500);
            }
        } else {
            addChatMessage('Sorry, I encountered an error. Please try again.');
        }
    } catch (error) {
        if (aiStatus) aiStatus.style.display = 'none';
        addChatMessage('Network error. Please check your connection and try again.');
    }
}
