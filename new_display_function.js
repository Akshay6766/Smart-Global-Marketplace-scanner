function extractMobileSpecs(title, snippet) {
    const text = (title + ' ' + (snippet || '')).toLowerCase();
    const specs = { processor: '', battery: '', display: '', camera: '', connectivity: '', storage: '' };
    
    const procPatterns = [/snapdragon\s*(\d+)/i, /mediatek\s*dimensity\s*(\d+)/i, /helio\s*[gp]\d+/i, /exynos\s*(\d+)/i, /apple\s*a\d+/i, /bionic/i, /tensor/i, /octa[\s-]?core/i, /quad[\s-]?core/i, /(\d+)\s*nm/i];
    for (let p of procPatterns) { const m = text.match(p); if (m) { specs.processor = m[0]; break; } }
    
    const battPatterns = [/(\d{4,5})\s*mah/i, /(\d+)w\s*fast\s*charg/i, /wireless\s*charg/i];
    for (let p of battPatterns) { const m = text.match(p); if (m) { specs.battery = m[0]; break; } }
    
    const dispPatterns = [/(\d+\.\d+)[\s-]?inch/i, /(\d+)hz/i, /amoled/i, /oled/i, /lcd/i, /(\d{3,4})\s*x\s*(\d{3,4})/i, /retina/i, /super\s*amoled/i];
    for (let p of dispPatterns) { const m = text.match(p); if (m) { specs.display = m[0]; break; } }
    
    const camPatterns = [/(\d+)\s*mp/i, /triple\s*camera/i, /quad\s*camera/i, /dual\s*camera/i, /(\d+)mp\s*\+\s*(\d+)mp/i, /ultra[\s-]?wide/i, /telephoto/i, /periscope/i];
    for (let p of camPatterns) { const m = text.match(p); if (m) { specs.camera = m[0]; break; } }
    
    const connPatterns = [/5g/i, /4g\s*lte/i, /wifi\s*6/i, /bluetooth\s*5/i, /nfc/i];
    const connFound = []; for (let p of connPatterns) { const m = text.match(p); if (m) connFound.push(m[0]); }
    if (connFound.length > 0) specs.connectivity = connFound.join(', ');
    
    const storPatterns = [/(\d+)gb\s*ram/i, /(\d+)gb\s*storage/i, /(\d+)gb\s*rom/i, /(\d+)gb\s*\/\s*(\d+)gb/i, /expandable/i, /microsd/i];
    const storFound = []; for (let p of storPatterns) { const m = text.match(p); if (m) storFound.push(m[0]); }
    if (storFound.length > 0) specs.storage = storFound.slice(0, 2).join(', ');
    
    return specs;
}

function displayLiveResults(results, sym, country) {
    const container = document.getElementById('resultsContainer');
    const statsSection = document.getElementById('statsSection');
    if (statsSection) statsSection.style.display = 'none';
    if (container) container.style.display = 'block';
    
    if (!results || results.length === 0) { container.innerHTML = '<div class="loading"><p>No products found</p></div>'; return; }
    
    let html = '<h2 style="margin-bottom:20px;">Live Results (' + results.length + ' from ' + country + ')</h2>';
    
    results.forEach(p => {
        const specs = extractMobileSpecs(p.title, p.snippet);
        const getScoreBadge = (score, label) => {
            let badgeClass = 'score-fair';
            if (score >= 80) badgeClass = 'score-excellent';
            else if (score >= 60) badgeClass = 'score-good';
            else if (score < 40) badgeClass = 'score-poor';
            return '<span class="score-badge ' + badgeClass + '">' + label + ': ' + score + '</span>';
        };
        
        html += '<div class="live-product-card">';
        html += '<div style="display:flex;justify-content:space-between;margin-bottom:15px;flex-wrap:wrap;gap:10px;">';
        html += '<div style="flex:1;min-width:200px;"><h3 style="margin:0 0 8px 0;">' + p.title + '</h3>';
        html += '<span class="marketplace-badge">' + p.source + '</span></div>';
        html += '<div style="text-align:right;"><div style="font-size:1.8em;font-weight:bold;color:#28a745;">' + sym + p.price.toLocaleString() + '</div></div></div>';
        
        html += '<div style="display:flex;flex-wrap:wrap;gap:10px;margin-bottom:15px;">';
        html += getScoreBadge(p.trust_score, 'Trust') + getScoreBadge(p.quality_score, 'Quality') + getScoreBadge(p.value_score, 'Value');
        html += '</div>';
        
        const hasSpecs = specs.processor || specs.battery || specs.display || specs.camera || specs.connectivity || specs.storage;
        if (hasSpecs) {
            html += '<div style="background:#f8f9fa;padding:15px;border-radius:8px;margin-bottom:15px;">';
            html += '<div style="font-weight:600;margin-bottom:10px;">📱 Specifications</div>';
            html += '<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:10px;">';
            if (specs.processor) html += '<div style="font-size:0.85em;"><span style="font-weight:600;">⚡ Processor:</span> ' + specs.processor + '</div>';
            if (specs.battery) html += '<div style="font-size:0.85em;"><span style="font-weight:600;">🔋 Battery:</span> ' + specs.battery + '</div>';
            if (specs.display) html += '<div style="font-size:0.85em;"><span style="font-weight:600;">📺 Display:</span> ' + specs.display + '</div>';
            if (specs.camera) html += '<div style="font-size:0.85em;"><span style="font-weight:600;">📷 Camera:</span> ' + specs.camera + '</div>';
            if (specs.connectivity) html += '<div style="font-size:0.85em;"><span style="font-weight:600;">📡 Connectivity:</span> ' + specs.connectivity + '</div>';
            if (specs.storage) html += '<div style="font-size:0.85em;"><span style="font-weight:600;">💾 Storage:</span> ' + specs.storage + '</div>';
            html += '</div></div>';
        }
        
        html += '<a href="' + p.link + '" target="_blank" style="display:inline-block;padding:12px 24px;background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);color:white;text-decoration:none;border-radius:8px;font-weight:600;">View on ' + p.source + '</a>';
        html += '</div>';
    });
    
    container.innerHTML = html;
    const sortingControls = document.getElementById('sortingControls');
    if (sortingControls) sortingControls.style.display = 'none';
}
