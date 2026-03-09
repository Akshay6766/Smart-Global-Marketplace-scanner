# Mobile CPI Page Update Instructions

## Goal
Add live marketplace search alongside the existing indexed CPI search on the mobile CPI page.

## Changes Required

### 1. Add Tab System to HTML (After line 45 - in search-section)

Replace the current search section with:

```html
<div class="search-section">
    <!-- Tab Navigation -->
    <div class="search-tabs">
        <button class="tab-btn active" onclick="switchTab('indexed')">
             Indexed Search (978 Phones)
        </button>
        <button class="tab-btn" onclick="switchTab('live')">
             Live Marketplace Search
        </button>
    </div>
    
    <!-- Indexed Search Tab -->
    <div id="indexedTab" class="tab-content active">
        <div class="search-form">
            <input type="text" id="searchQuery" class="search-input-full" placeholder="What phone are you looking for? (e.g., phone under 30k)">
            <button onclick="performAISearch()" class="search-btn">Search Indexed Phones</button>
        </div>
        <!-- Keep existing AI response window here -->
    </div>
    
    <!-- Live Search Tab -->
    <div id="liveTab" class="tab-content">
        <div class="search-form">
            <input type="text" id="liveSearchQuery" class="search-input-full" placeholder="Search live marketplaces (e.g., Samsung Galaxy S24)">
            <div class="price-row">
                <input type="number" id="liveBudget" class="price-input" placeholder="Budget (optional)">
                <select id="liveCountry" class="price-input">
                    <option value="IN">🇮🇳 India (INR)</option>
                    <option value="US">🇺🇸 USA (USD)</option>
                    <option value="UK">🇬🇧 UK (GBP)</option>
                    <option value="CA">🇨🇦 Canada (CAD)</option>
                    <option value="AU">🇦🇺 Australia (AUD)</option>
                </select>
            </div>
            <button onclick="performLiveSearch()" class="search-btn">Search Live Marketplaces</button>
        </div>
        
        <!-- Live Search AI Response Window -->
        <div id="liveAIResponseWindow" style="display:none; margin-top: 15px; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 12px;">
            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 15px;">
                <div style="display: flex; align-items: center; gap: 10px;">
                    <span style="font-size: 24px;"></span>
                    <span style="color: white; font-weight: 600;">Live Search Results</span>
                </div>
            </div>
            <div id="liveSearchStatus" style="color: white; font-size: 14px; padding: 12px; background: rgba(255,255,255,0.15); border-radius: 8px;"></div>
        </div>
    </div>
</div>
```

### 2. Add CSS for Tabs (After line 45 in CSS)

```css
.search-tabs {
    display: flex;
    gap: 10px;
    margin-bottom: 20px;
    border-bottom: 2px solid #e0e0e0;
}

.tab-btn {
    background: transparent;
    border: none;
    padding: 12px 24px;
    font-size: 16px;
    font-weight: 600;
    color: #666;
    cursor: pointer;
    border-bottom: 3px solid transparent;
    transition: all 0.3s;
}

.tab-btn.active {
    color: #667eea;
    border-bottom-color: #667eea;
}

.tab-btn:hover {
    color: #667eea;
}

.tab-content {
    display: none;
}

.tab-content.active {
    display: block;
}

.live-product-card {
    background: white;
    border: 1px solid #e0e0e0;
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 20px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}

.marketplace-badge {
    display: inline-block;
    padding: 4px 12px;
    background: #667eea;
    color: white;
    border-radius: 12px;
    font-size: 12px;
    font-weight: 600;
    margin-right: 8px;
}

.score-badge {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    padding: 6px 12px;
    background: #f0f0f0;
    border-radius: 8px;
    font-size: 13px;
    font-weight: 600;
}

.score-excellent { background: #d4edda; color: #155724; }
.score-good { background: #d1ecf1; color: #0c5460; }
.score-fair { background: #fff3cd; color: #856404; }
.score-poor { background: #f8d7da; color: #721c24; }
```

### 3. Add JavaScript Functions (Before closing </script> tag)

```javascript
// Tab Switching
function switchTab(tabName) {
    // Hide all tabs
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    // Show selected tab
    if (tabName === 'indexed') {
        document.getElementById('indexedTab').classList.add('active');
        document.querySelectorAll('.tab-btn')[0].classList.add('active');
    } else if (tabName === 'live') {
        document.getElementById('liveTab').classList.add('active');
        document.querySelectorAll('.tab-btn')[1].classList.add('active');
    }
}

// Live Marketplace Search
async function performLiveSearch() {
    const query = document.getElementById('liveSearchQuery').value.trim();
    const budget = document.getElementById('liveBudget').value;
    const country = document.getElementById('liveCountry').value;
    
    if (!query) {
        alert('Please enter a search term');
        return;
    }
    
    // Show status
    const statusDiv = document.getElementById('liveSearchStatus');
    const windowDiv = document.getElementById('liveAIResponseWindow');
    
    if (windowDiv) windowDiv.style.display = 'block';
    if (statusDiv) statusDiv.textContent = `Searching ${query} across Amazon, Flipkart, eBay, Walmart...`;
    
    showLoading('Searching live marketplaces...');
    
    try {
        const response = await fetch('/api/search', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                query: query,
                country_code: country,
                max_results: 20,
                budget: budget ? parseFloat(budget) : null
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            displayLiveResults(data.results, data.country_name, data.currency_symbol);
            if (statusDiv) {
                statusDiv.textContent = `Found ${data.total_results || data.results.length} products from ${data.country_name}`;
            }
        } else {
            showError(data.error || 'Search failed');
            if (statusDiv) statusDiv.textContent = 'Search failed. Please try again.';
        }
    } catch (error) {
        showError('Network error: ' + error.message);
        if (statusDiv) statusDiv.textContent = 'Network error. Please check your connection.';
    }
}

// Display Live Marketplace Results
function displayLiveResults(results, countryName, currencySymbol) {
    const container = document.getElementById('resultsContainer');
    
    if (!results || results.length === 0) {
        container.innerHTML = `
            <div class="loading">
                <p>No products found. Try a different search term.</p>
            </div>
        `;
        return;
    }
    
    let html = `<h2 style="margin-bottom: 20px;">Live Marketplace Results from ${countryName} (${results.length} products)</h2>`;
    
    results.forEach((product, index) => {
        // Get score color class
        let scoreClass = 'score-poor';
        if (product.overall_rank >= 85) scoreClass = 'score-excellent';
        else if (product.overall_rank >= 75) scoreClass = 'score-good';
        else if (product.overall_rank >= 65) scoreClass = 'score-fair';
        
        html += `
            <div class="live-product-card">
                <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 15px;">
                    <div style="flex: 1;">
                        <div style="margin-bottom: 8px;">
                            <span class="marketplace-badge">${product.source}</span>
                            <span style="color: #999; font-size: 13px;">#${index + 1}</span>
                        </div>
                        <h3 style="margin: 0 0 8px 0; color: #333; font-size: 1.2em;">${product.title}</h3>
                        ${product.seller_name ? `<div style="color: #666; font-size: 14px;">Sold by: ${product.seller_name}</div>` : ''}
                    </div>
                    <div style="text-align: right;">
                        <div style="font-size: 1.8em; font-weight: bold; color: #28a745;">${currencySymbol}${product.price.toLocaleString()}</div>
                    </div>
                </div>
                
                <div style="display: flex; gap: 10px; margin-bottom: 15px; flex-wrap: wrap;">
                    <div class="score-badge ${scoreClass}">
                         Overall: ${product.overall_rank.toFixed(1)}/100
                    </div>
                    <div class="score-badge">
                         Trust: ${product.trust_score.toFixed(1)}/100
                    </div>
                    <div class="score-badge">
                         Quality: ${product.quality_score.toFixed(1)}/100
                    </div>
                    <div class="score-badge">
                         Value: ${product.value_score.toFixed(1)}/100
                    </div>
                </div>
                
                ${product.product_rating ? `
                    <div style="margin-bottom: 15px; color: #666;">
                        <span style="color: #f39c12; font-size: 16px;">★</span>
                        <span style="font-weight: 600;">${product.product_rating.toFixed(1)}</span>
                        <span style="font-size: 13px;">(${product.review_count} reviews)</span>
                    </div>
                ` : ''}
                
                ${product.description ? `
                    <p style="color: #666; font-size: 14px; margin-bottom: 15px; line-height: 1.5;">${product.description.substring(0, 150)}...</p>
                ` : ''}
                
                <a href="${product.url}" target="_blank" style="display: inline-block; padding: 12px 24px; background: #667eea; color: white; text-decoration: none; border-radius: 8px; font-weight: 600;">
                     View on ${product.source}
                </a>
            </div>
        `;
    });
    
    container.innerHTML = html;
    
    // Show sorting controls
    const sortingControls = document.getElementById('sortingControls');
    if (sortingControls) sortingControls.style.display = 'block';
}

// Add Enter key support for live search
window.addEventListener('load', function() {
    const liveSearchInput = document.getElementById('liveSearchQuery');
    if (liveSearchInput) {
        liveSearchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                performLiveSearch();
            }
        });
    }
});
```

### 4. Update Quick Actions Section

Add a link to switch between modes:

```html
<div class="quick-actions">
    <button onclick="getTopCPIPhones()" class="quick-btn">Top CPI Phones</button>
    <button onclick="getBestValuePhones()" class="quick-btn">Best Value</button>
    <button onclick="getStats()" class="quick-btn">Statistics</button>
    <button onclick="switchTab('live')" class="quick-btn" style="background: rgba(102, 126, 234, 0.9);"> Try Live Search</button>
</div>
```

## Implementation Steps

1. Open `templates/mobile_cpi.html`
2. Add the CSS for tabs in the `<style>` section
3. Replace the search section HTML with the tabbed version
4. Add the JavaScript functions before the closing `</script>` tag
5. Update the quick actions to include the "Try Live Search" button
6. Save and test

## Testing

1. **Indexed Search Tab**: Should work as before with 978 pre-indexed phones
2. **Live Search Tab**: Should search Amazon, Flipkart, eBay, Walmart in real-time
3. **Tab Switching**: Should smoothly switch between the two modes
4. **Results Display**: Both tabs should display results in the same container

## Benefits

- Users can choose between fast indexed search (978 phones) or comprehensive live search (all marketplaces)
- Live search uses the same API as the main page (`/api/search`)
- Maintains all existing functionality while adding new capabilities
- Clean UI with tab navigation
- Mobile responsive design maintained
