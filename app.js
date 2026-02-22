/***********************************************
 * THE SLOPULATOR - Retro JavaScript
 * Maximum Weirdness Achieved
 ***********************************************/

// ============================================
// GLOBAL STATE
// ============================================

let currentPropertyData = null;
let currentAddress = '';
let calculationResults = null;
let visitorCount = 0;

// ============================================
// VISITOR COUNTER (Retro Digital Style)
// ============================================

function initVisitorCounter() {
    // Get stored count or start from a "believable" retro number
    const stored = localStorage.getItem('slopulator_visitors');
    if (stored) {
        visitorCount = parseInt(stored) + 1;
    } else {
        visitorCount = 42069; // Nice retro starting number
    }
    
    localStorage.setItem('slopulator_visitors', visitorCount);
    
    // Animate the counter
    animateVisitorCounter();
    
    // Also update footer hit counter to match main counter
    document.getElementById('footer-hit-count').textContent = visitorCount.toString().padStart(7, '0');
}

function animateVisitorCounter() {
    const display = visitorCount.toString().padStart(7, '0');
    const counterEl = document.getElementById('visitor-counter');
    
    // Create animated digits
    let html = '';
    for (let i = 0; i < display.length; i++) {
        const delay = i * 0.1;
        html += `<span class="digit" style="animation-delay: ${delay}s">${display[i]}</span>`;
    }
    counterEl.innerHTML = html;
    
    // Add flip animation to last digit
    setTimeout(() => {
        const digits = counterEl.querySelectorAll('.digit');
        if (digits.length > 0) {
            digits[digits.length - 1].style.animation = 'digit-flip 0.5s ease';
        }
    }, 500);
}

// ============================================
// BOUNCING EMOJIS
// ============================================

function initBouncingEmojis() {
    const container = document.getElementById('bouncing-emojis');
    const emojis = ['🏠', '💰', '🔨', '📈', '💵', '🏗️'];
    
    emojis.forEach((emoji, index) => {
        const span = document.createElement('span');
        span.className = 'bouncing-emoji';
        span.textContent = emoji;
        span.style.animationDelay = `${index}s`;
        span.style.left = `${10 + (index * 15)}%`;
        span.style.top = `${10 + (index * 10)}%`;
        span.style.animationDuration = `${6 + Math.random() * 4}s`;
        
        // Easter egg: click house emoji
        span.addEventListener('click', () => {
            if (emoji === '🏠') {
                showEasterEgg();
            } else {
                createSparkles(span);
                span.style.transform = 'scale(2)';
                setTimeout(() => span.style.transform = 'scale(1)', 200);
            }
        });
        
        container.appendChild(span);
    });
}

function createSparkles(element) {
    const rect = element.getBoundingClientRect();
    const container = document.getElementById('sparkles');
    
    for (let i = 0; i < 10; i++) {
        const sparkle = document.createElement('div');
        sparkle.className = 'sparkle';
        sparkle.style.left = `${rect.left + rect.width/2 + (Math.random() - 0.5) * 50}px`;
        sparkle.style.top = `${rect.top + rect.height/2 + (Math.random() - 0.5) * 50}px`;
        sparkle.style.animationDelay = `${i * 0.05}s`;
        container.appendChild(sparkle);
        
        setTimeout(() => sparkle.remove(), 1000);
    }
}

// ============================================
// CONFETTI EXPLOSION
// ============================================

function fireConfetti() {
    const colors = ['#FF00FF', '#00FFFF', '#FFFF00', '#00FF00', '#FF0000', '#FF9900'];
    const container = document.getElementById('sparkles');
    
    // Create many confetti particles
    for (let i = 0; i < 100; i++) {
        setTimeout(() => {
            const confetti = document.createElement('div');
            confetti.style.cssText = `
                position: fixed;
                width: ${10 + Math.random() * 10}px;
                height: ${10 + Math.random() * 10}px;
                background: ${colors[Math.floor(Math.random() * colors.length)]};
                left: 50%;
                top: 50%;
                z-index: 99999;
                pointer-events: none;
            `;
            
            // Random trajectory
            const angle = Math.random() * Math.PI * 2;
            const velocity = 5 + Math.random() * 15;
            let x = window.innerWidth / 2;
            let y = window.innerHeight / 2;
            let vx = Math.cos(angle) * velocity;
            let vy = Math.sin(angle) * velocity;
            let gravity = 0.5;
            let rotation = 0;
            let rotationSpeed = (Math.random() - 0.5) * 20;
            
            container.appendChild(confetti);
            
            const animate = () => {
                x += vx;
                y += vy;
                vy += gravity;
                rotation += rotationSpeed;
                
                confetti.style.left = x + 'px';
                confetti.style.top = y + 'px';
                confetti.style.transform = `rotate(${rotation}deg)`;
                
                if (y < window.innerHeight) {
                    requestAnimationFrame(animate);
                } else {
                    confetti.remove();
                }
            };
            
            requestAnimationFrame(animate);
        }, i * 10);
    }
}

// ============================================
// EASTER EGG
// ============================================

function showEasterEgg() {
    const modal = document.getElementById('easterEggModal');
    modal.style.display = 'flex';
    
    // Play a "ka-ching" sound effect (placeholder)
    playRetroSound('ka-ching');
}

function closeEasterEgg() {
    document.getElementById('easterEggModal').style.display = 'none';
}

function playRetroSound(type) {
    // Simple beep using Web Audio API
    try {
        const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        const oscillator = audioCtx.createOscillator();
        const gainNode = audioCtx.createGain();
        
        oscillator.connect(gainNode);
        gainNode.connect(audioCtx.destination);
        
        if (type === 'ka-ching') {
            oscillator.frequency.setValueAtTime(800, audioCtx.currentTime);
            oscillator.frequency.exponentialRampToValueAtTime(1200, audioCtx.currentTime + 0.1);
            gainNode.gain.setValueAtTime(0.3, audioCtx.currentTime);
            gainNode.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.3);
            oscillator.start();
            oscillator.stop(audioCtx.currentTime + 0.3);
        }
    } catch (e) {
        console.log('Audio not supported');
    }
}

function playWhipSound() {
    // Whip crack sound using Web Audio API
    try {
        const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        
        // Create whip crack noise
        const bufferSize = audioCtx.sampleRate * 0.5; // 0.5 seconds
        const buffer = audioCtx.createBuffer(1, bufferSize, audioCtx.sampleRate);
        const data = buffer.getChannelData(0);
        
        // Fill with filtered noise
        for (let i = 0; i < bufferSize; i++) {
            data[i] = (Math.random() * 2 - 1) * Math.pow(1 - i / bufferSize, 2);
        }
        
        const noise = audioCtx.createBufferSource();
        noise.buffer = buffer;
        
        const filter = audioCtx.createBiquadFilter();
        filter.type = 'highpass';
        filter.frequency.value = 1000;
        
        const gainNode = audioCtx.createGain();
        gainNode.gain.setValueAtTime(0.8, audioCtx.currentTime);
        gainNode.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.3);
        
        noise.connect(filter);
        filter.connect(gainNode);
        gainNode.connect(audioCtx.destination);
        
        noise.start();
    } catch (e) {
        console.log('Whip sound not supported');
    }
}

// ============================================
// UTILITY FUNCTIONS
// ============================================

function formatCurrency(value) {
    if (value === undefined || value === null) return '$0';
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
        minimumFractionDigits: 0,
        maximumFractionDigits: 0
    }).format(value);
}

function formatPercent(value) {
    if (value === undefined || value === null) return '0%';
    return value.toFixed(2) + '%';
}

function showLoading() {
    document.getElementById('loadingOverlay').style.display = 'flex';
}

function hideLoading() {
    document.getElementById('loadingOverlay').style.display = 'none';
}

function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// ============================================
// ADDRESS AUTOCOMPLETE (OpenStreetMap)
// ============================================

// Address autocomplete using PropertyReach API
let lastQuery = '';
let autocompleteTimeout;

async function fetchAddressSuggestions(query) {
    clearTimeout(autocompleteTimeout);
    
    const suggestionsEl = document.getElementById('addressSuggestions');
    
    if (!suggestionsEl) return;
    
    if (query.length < 3) {
        suggestionsEl.style.display = 'none';
        return;
    }
    
    if (query === lastQuery) return;
    lastQuery = query;
    
    // Debounce for 200ms
    autocompleteTimeout = setTimeout(async () => {
        try {
            // Try PropertyReach search API
            const searchUrl = PROXY_URL + encodeURIComponent('https://api.propertyreach.com/v1/search');
            const response = await fetch(searchUrl, {
                method: 'POST',
                headers: { 
                    'x-api-key': PROPERTYREACH_API_KEY,
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
                body: JSON.stringify({
                    target: { city: query.split(',')[0]?.trim() || query, state: 'OK' },
                    filter: {},
                    limit: 10
                })
            });
            
            if (response.ok) {
                const data = await response.json();
                if (data && data.properties && data.properties.length > 0) {
                    const suggestions = data.properties.map(p => ({
                        display_name: p.streetAddress + ', ' + p.city + ', ' + p.state + ' ' + p.zip,
                        lat: p.latitude,
                        lon: p.longitude
                    }));
                    displaySuggestions(suggestions);
                    return;
                }
            }
            
            // Fallback to Nominatim if PropertyReach fails
            // Prioritize Chickasha, OK by appending city to query
            const chickashaQuery = query.includes('Chickasha') ? query : `${query}, Chickasha, OK`;
            const osmResponse = await fetch(`https://nominatim.openstreetmap.org/search?q=${encodeURIComponent(chickashaQuery)}&format=json&addressdetails=1&limit=5&countrycodes=us`, {
                headers: { 'User-Agent': 'Slopulator/1.0' }
            });
            
            let osmData = [];
            if (osmResponse.ok) {
                osmData = await osmResponse.json();
            }
            
            // If no results from Chickasha-prioritized search, try broader search
            if (osmData.length === 0) {
                const broaderResponse = await fetch(`https://nominatim.openstreetmap.org/search?q=${encodeURIComponent(query)}&format=json&addressdetails=1&limit=5&countrycodes=us`, {
                    headers: { 'User-Agent': 'Slopulator/1.0' }
                });
                if (broaderResponse.ok) {
                    osmData = await broaderResponse.json();
                }
            }
            
            displaySuggestions(osmData);
        } catch (error) {
            console.error('Autocomplete error:', error);
            suggestionsEl.style.display = 'none';
        }
    }, 200);
}

function displaySuggestions(suggestions) {
    const suggestionsEl = document.getElementById('addressSuggestions');
    
    if (!suggestions || suggestions.length === 0) {
        suggestionsEl.style.display = 'none';
        return;
    }

    suggestionsEl.innerHTML = suggestions.map(s => `
        <div class="suggestion-item" 
             data-address="${s.display_name}" 
             data-lat="${s.lat}" 
             data-lon="${s.lon}">
            ${s.display_name}
        </div>
    `).join('');

    suggestionsEl.style.display = 'block';

    // Add click handlers
    suggestionsEl.querySelectorAll('.suggestion-item').forEach(item => {
        item.addEventListener('click', () => {
            document.getElementById('addressInput').value = item.dataset.address;
            currentAddress = item.dataset.address;
            suggestionsEl.style.display = 'none';
            loadPropertyData(item.dataset.address, item.dataset.lat, item.dataset.lon);
        });
    });
}

// ============================================
// MOCK PROPERTY DATA (since we don't have API keys)
// ============================================

function mockPropertyData(address, lat, lon) {
    // Generate deterministic values based on address hash
    let hash = 0;
    for (let i = 0; i < address.length; i++) {
        const char = address.charCodeAt(i);
        hash = ((hash << 5) - hash) + char;
        hash = hash & hash;
    }
    hash = Math.abs(hash);
    
    // Base values
    const basePrice = 200000 + (hash % 400000);
    const bedrooms = 2 + (hash % 4);
    const bathrooms = 1 + (hash % 3);
    const sqft = 1000 + (hash % 2000);
    
    // PropertyReach Estimate with variance
    const estimatedValue = basePrice + ((hash >> 4) % 50000) - 25000;
    
    // Generate comps
    const comps = [];
    for (let i = 0; i < 5; i++) {
        const compPrice = basePrice + (((hash >> (i * 4)) % 60000) - 30000);
        const daysAgo = ((hash >> (i * 3)) % 180);
        comps.push({
            address: `${(hash % 900) + 100} ${address.split(',')[0].split(' ').slice(1).join(' ').split(' ')[0] || 'Main'} St`,
            sale_price: Math.round(compPrice / 1000) * 1000,
            sale_date: `${daysAgo} days ago`,
            beds: bedrooms,
            baths: bathrooms,
            sqft: sqft + (((hash >> i) % 400) - 200)
        });
    }
    
    // Sort by recency
    comps.sort((a, b) => parseInt(a.sale_date) - parseInt(b.sale_date));
    
    // Tax and rent estimates
    const taxRate = 0.015 + ((hash % 50) / 10000);
    const annualTaxes = Math.round(basePrice * taxRate / 100) * 100;
    const rentRate = 0.008 + ((hash % 40) / 10000);
    const rentEstimate = Math.round(basePrice * rentRate / 100) * 100;
    
    // Calculate insurance based on sqft ($0.50 per sqft annually)
    const insurancePerSqft = 0.50;
    const annualInsurance = Math.round(sqft * insurancePerSqft);
    
    return {
        estimatedValue: Math.round(estimatedValue / 1000) * 1000,
        comps: comps,
        annual_taxes: annualTaxes,
        monthly_taxes: Math.round(annualTaxes / 12),
        rent_estimate: rentEstimate,
        annual_insurance: annualInsurance,
        monthly_insurance: Math.round(annualInsurance / 12),
        property_details: {
            bedrooms: bedrooms,
            bathrooms: bathrooms,
            sqft: sqft,
            year_built: 1960 + (hash % 60),
            lot_size: `${3000 + (hash % 7000)} sqft`
        }
    };
}

// Make loadPropertyData available globally for inline scripts
window.loadPropertyData = async function(address, lat, lon) {
    showLoading();
    
    try {
        // Try PropertyReach API
        let data = null;
        
        try {
            const addressParts = address.split(',').map(s => s.trim());
            const streetAddress = addressParts[0] || '';
            const city = addressParts[1] || '';
            const state = addressParts[2]?.split(' ')[0] || '';
            
            const propertyUrl = PROXY_URL + encodeURIComponent(`https://api.propertyreach.com/v1/property?streetAddress=${encodeURIComponent(streetAddress)}&city=${encodeURIComponent(city)}&state=${encodeURIComponent(state)}`);
            const response = await fetch(propertyUrl, {
                headers: {
                    'x-api-key': PROPERTYREACH_API_KEY,
                    'Accept': 'application/json'
                }
            });
            
            if (response.ok) {
                const propertyData = await response.json();
                
                if (propertyData && propertyData.property) {
                    const prop = propertyData.property;
                    data = {
                        estimatedValue: prop.estimatedValue || 0,
                        rent_estimate: prop.estimatedRentAmount || 0,
                        annual_taxes: prop.taxAmount || 0,
                        monthly_taxes: prop.taxAmount ? Math.round(prop.taxAmount / 12) : 0,
                        annual_insurance: Math.round((prop.squareFeet || 1500) * 0.50),
                        property_details: {
                            sqft: prop.squareFeet || prop.livingSquareFeet || 1500,
                            bedrooms: prop.bedrooms || 0,
                            bathrooms: prop.bathrooms || 0,
                            year_built: prop.yearBuilt || 0
                        }
                    };
                }
            }
        } catch (err) {
            console.warn('PropertyReach API failed, using mock data:', err);
        }
        
        // Fallback to mock data if API fails
        if (!data) {
            data = mockPropertyData(address, lat, lon);
        }
        
        currentPropertyData = data;
        
        // Populate fields
        const el = document.getElementById('arvInput'); if(el) el.value = data.estimatedValue || '';
        // Rent: use PropertyReach if available, else leave blank
        document.getElementById('rentEstimate').value = data.rent_estimate || '';
        // rentEstimateDetail removed from DOM
        document.getElementById('monthlyTaxes').value = data.monthly_taxes || '';
        document.getElementById('annualInsurance').value = data.annual_insurance || '';
        document.getElementById('sqft').value = data.property_details?.sqft || '';
        
        // Ensure loan term is set to default if empty
        const loanTermEl = document.getElementById('loanTerm');
        if (loanTermEl && !loanTermEl.value) {
            loanTermEl.value = 20;
        }
        
        // Populate comps table
        populateCompsTable(data.comps || []);
        document.getElementById('compsSection').style.display = 'table-row';
        
        // Create sparkles
        const searchBtn = document.getElementById('searchBtn');
        createSparkles(searchBtn);
        
    } catch (error) {
        console.error('Error:', error);
        alert('Error loading data! The internet tubes might be clogged! 🚧');
    } finally {
        hideLoading();
    }
}

function populateCompsTable(comps) {
    const tbody = document.querySelector('#compsTable tbody');
    
    if (!comps || comps.length === 0) {
        tbody.innerHTML = '<tr><td colspan="6" align="center"><font color="#FF0000">No comps found!</font></td></tr>';
        return;
    }

    tbody.innerHTML = comps.map(comp => `
        <tr>
            <td><font color="#00FFFF">${comp.address}</font></td>
            <td><font color="#00FF00">${formatCurrency(comp.sale_price)}</font></td>
            <td><font color="#FFFF00">${comp.sale_date}</font></td>
            <td><font color="#FF9900">${comp.beds}</font></td>
            <td><font color="#FF9900">${comp.baths}</font></td>
            <td><font color="#00FFFF">${comp.sqft.toLocaleString()}</font></td>
        </tr>
    `).join('');
}

// ============================================
// CALCULATIONS
// ============================================

function calculateARV(estimatedValue, comps) {
    if (!comps || comps.length === 0) {
        return Math.round(estimatedValue / 1000) * 1000;
    }
    
    const compPrices = comps.slice(0, 5).map(c => c.sale_price);
    const avgComps = compPrices.reduce((a, b) => a + b, 0) / compPrices.length;
    
    // Weighted average: 60% PropertyReach Estimate + 40% Comps
    const arv = (estimatedValue * 0.60) + (avgComps * 0.40);
    return Math.round(arv / 1000) * 1000;
}

function calculateRentalCashflow(purchasePrice, repairs, rentEstimate, monthlyTaxes, insuranceAnnual, interestRate) {
    const effectiveRent = rentEstimate * 0.90;
    const loanAmount = purchasePrice + repairs;
    const monthlyRate = (interestRate / 100) / 12;
    const numPayments = 25 * 12;
    
    let mortgagePayment;
    if (monthlyRate > 0) {
        mortgagePayment = loanAmount * (monthlyRate * Math.pow(1 + monthlyRate, numPayments)) / 
                          (Math.pow(1 + monthlyRate, numPayments) - 1);
    } else {
        mortgagePayment = loanAmount / numPayments;
    }
    
    const monthlyInsurance = insuranceAnnual / 12;
    const maintenanceReserve = rentEstimate * 0.05;
    const totalExpenses = mortgagePayment + monthlyTaxes + monthlyInsurance + maintenanceReserve;
    const monthlyCashflow = effectiveRent - totalExpenses;
    const annualCashflow = monthlyCashflow * 12;
    const cashOnCash = purchasePrice > 0 ? (annualCashflow / (purchasePrice * 0.20)) * 100 : 0;
    
    return {
        monthly_rent: rentEstimate,
        effective_monthly_rent: Math.round(effectiveRent * 100) / 100,
        mortgage_payment: Math.round(mortgagePayment * 100) / 100,
        monthly_taxes: monthlyTaxes,
        monthly_insurance: Math.round(monthlyInsurance * 100) / 100,
        maintenance_reserve: Math.round(maintenanceReserve * 100) / 100,
        total_monthly_expenses: Math.round(totalExpenses * 100) / 100,
        monthly_cashflow: Math.round(monthlyCashflow * 100) / 100,
        annual_cashflow: Math.round(annualCashflow * 100) / 100,
        cash_on_cash_return: Math.round(cashOnCash * 100) / 100
    };
}

function calculateFlipAnalysis(purchasePrice, repairs, arv, interestRate) {
    const totalInvestment = purchasePrice + repairs;
    const holdingMonths = 5;
    const monthlyInterest = (totalInvestment * (interestRate / 100)) / 12;
    const holdingCosts = monthlyInterest * holdingMonths;
    const sellingCosts = arv * 0.07;
    const totalCosts = purchasePrice + repairs + holdingCosts + sellingCosts;
    const profit = arv - totalCosts;
    const roi = totalInvestment > 0 ? (profit / totalInvestment) * 100 : 0;
    const mao = (arv * 0.70) - repairs;
    
    return {
        arv: arv,
        purchase_price: purchasePrice,
        repairs: repairs,
        holding_costs: Math.round(holdingCosts * 100) / 100,
        selling_costs: Math.round(sellingCosts * 100) / 100,
        total_costs: Math.round(totalCosts * 100) / 100,
        profit: Math.round(profit * 100) / 100,
        roi_percent: Math.round(roi * 100) / 100,
        mao_70_percent: Math.round(mao / 100) * 100,
        suggested_offer: Math.round(mao * 0.95 / 100) * 100
    };
}

async function runCalculations() {
    const purchasePrice = parseFloat(document.getElementById('purchasePrice').value) || 0;
    const repairs = parseFloat(document.getElementById('repairCost').value) || 0;
    const arv = parseFloat(document.getElementById('arvInput').value) || 0;
    const rentEstimate = parseFloat(document.getElementById('rentEstimate').value) || 0;
    const monthlyTaxes = parseFloat(document.getElementById('monthlyTaxes').value) || 0;
    const insuranceAnnual = parseFloat(document.getElementById('annualInsurance').value) || 0;
    const interestRate = parseFloat(document.getElementById('interestRate').value) || 6.8;
    const loanTerm = parseInt(document.getElementById('loanTerm').value) || 20;
    
    if (!purchasePrice) {
        alert('Please fill in Purchase Price! 🏠');
        return;
    }
    
    showLoading();
    
    await new Promise(r => setTimeout(r, 800));
    
    // Comprehensive Analysis
    const analysis = performComprehensiveAnalysis({
        purchasePrice,
        repairs,
        arv,
        rentEstimate,
        monthlyTaxes,
        insuranceAnnual,
        interestRate,
        loanTerm
    });
    
    calculationResults = analysis;
    
    displayComprehensiveResults(analysis);
    
    hideLoading();
    
    // Fire confetti!
    fireConfetti();
    
    // Play sound
    playRetroSound('ka-ching');
}

function performComprehensiveAnalysis(data) {
    const { purchasePrice, repairs, arv, rentEstimate, monthlyTaxes, insuranceAnnual, interestRate, loanTerm } = data;
    
    const totalInvestment = purchasePrice + repairs;
    const monthlyInsurance = insuranceAnnual / 12;
    
    // FLIP ANALYSIS
    // 8% interest only on total investment for 6 months
    const holdingCosts = totalInvestment * (interestRate / 100) * 0.5; // 6 months = 0.5 years
    // Closing/broker fees ~6% of ARV
    const closingCosts = arv * 0.06;
    const totalFlipCosts = totalInvestment + holdingCosts + closingCosts;
    const flipProfit = arv - totalFlipCosts;
    
    // RENTAL ANALYSIS
    // PITI calculation
    const loanAmount = totalInvestment;
    const monthlyRate = (interestRate / 100) / 12;
    const numPayments = loanTerm * 12;
    const monthlyPI = loanAmount * (monthlyRate * Math.pow(1 + monthlyRate, numPayments)) / (Math.pow(1 + monthlyRate, numPayments) - 1);
    const piti = monthlyPI + monthlyTaxes + monthlyInsurance;
    
    // LTV based on AVM
    const currentLTV = (loanAmount / arv) * 100;
    
    // Cash flow at 95% occupancy
    const effectiveMonthlyRent = rentEstimate * 0.95;
    const monthlyCashFlow = effectiveMonthlyRent - piti;
    const annualCashFlow = monthlyCashFlow * 12;
    
    // BRRR ANALYSIS
    const maxRefinance = arv * 0.80; // 80% LTV
    const cashInvested = totalInvestment; // Assuming 100% financing for BRRR
    const cashLeftInDeal = Math.max(0, cashInvested - maxRefinance);
    const canPullOut100 = maxRefinance >= cashInvested;
    
    // DEAL RATING
    let rating, recommendation, actionPlan;
    
    // Calculate scores
    const flipScore = flipProfit > 30000 ? 3 : flipProfit > 15000 ? 2 : flipProfit > 0 ? 1 : 0;
    const cashFlowScore = monthlyCashFlow > 300 ? 3 : monthlyCashFlow > 150 ? 2 : monthlyCashFlow > 0 ? 1 : 0;
    const brrrScore = canPullOut100 ? 3 : cashLeftInDeal < 10000 ? 2 : cashLeftInDeal < 20000 ? 1 : 0;
    
    const totalScore = flipScore + cashFlowScore + brrrScore;
    
    if (totalScore >= 7) {
        rating = "⭐⭐⭐ EXCELLENT ⭐⭐⭐";
        recommendation = "🎯 STRONG BUY - This is a home run deal!";
        actionPlan = "• BRRR Strategy: Refinance immediately after rehab to pull out 100% of capital\n" +
                     "• Keep as rental for long-term cash flow and appreciation\n" +
                     "• Flip backup: Strong profit margin if you decide to sell\n" +
                     "• Consider adding to your permanent portfolio";
    } else if (totalScore >= 5) {
        rating = "⭐⭐ GOOD ⭐⭐";
        recommendation = "✅ BUY - Solid deal with multiple exit strategies";
        actionPlan = "• BRRR Strategy recommended - good cash flow with minimal cash left in\n" +
                     "• Flip option viable if you need quick capital\n" +
                     "• Negotiate final $2-5k if possible to improve margins\n" +
                     "• Get contractor bids to confirm rehab budget";
    } else if (totalScore >= 3) {
        rating = "⭐ FAIR ⭐";
        recommendation = "⚠️ CONDITIONAL BUY - Deal works but has limitations";
        actionPlan = "• Try to negotiate purchase price down by 5-10%\n" +
                     "• Get accurate rehab estimates - buffer in your budget\n" +
                     "• BRRR likely best exit - expect some cash to stay in deal\n" +
                     "• Consider partnering to reduce risk";
    } else {
        rating = "❌ PASS ❌";
        recommendation = "🚫 WALK AWAY - Numbers don't work";
        actionPlan = "• Offer $" + Math.round(purchasePrice * 0.85).toLocaleString() + " or less to make it work\n" +
                     "• Look for properties with better rent-to-price ratios\n" +
                     "• Consider markets with lower property taxes\n" +
                     "• Keep this as a comp but move on to next deal";
    }
    
    return {
        flip: {
            purchasePrice,
            repairs,
            totalInvestment,
            holdingCosts,
            closingCosts,
            totalCosts: totalFlipCosts,
            arv,
            profit: flipProfit
        },
        rental: {
            loanAmount,
            interestRate,
            loanTerm,
            monthlyPI,
            monthlyTaxes,
            monthlyInsurance,
            piti,
            arv,
            currentLTV,
            monthlyRent: rentEstimate,
            effectiveMonthlyRent,
            monthlyCashFlow,
            annualCashFlow
        },
        brrr: {
            maxRefinance,
            cashInvested,
            cashLeftInDeal,
            canPullOut100
        },
        rating: {
            score: totalScore,
            rating,
            recommendation,
            actionPlan
        }
    };
}

function displayComprehensiveResults(analysis) {
    // Show deal analysis section
    const dealSection = document.getElementById('dealAnalysisSection');
    if (dealSection) {
        dealSection.style.display = 'table-row';
    }
    
    // FLIP ANALYSIS
    setText('flipPurchasePrice', formatCurrency(analysis.flip.purchasePrice));
    setText('flipRepairCosts', formatCurrency(analysis.flip.repairs));
    setText('flipTotalInvestment', formatCurrency(analysis.flip.totalInvestment));
    setText('flipHoldingCosts', formatCurrency(analysis.flip.holdingCosts));
    setText('flipClosingCosts', formatCurrency(analysis.flip.closingCosts));
    setText('flipTotalCosts', formatCurrency(analysis.flip.totalCosts));
    setText('flipARV', formatCurrency(analysis.flip.arv));
    
    const flipProfitEl = document.getElementById('flipProfit');
    if (flipProfitEl) {
        flipProfitEl.textContent = (analysis.flip.profit >= 0 ? '+' : '-') + formatCurrency(Math.abs(analysis.flip.profit));
        flipProfitEl.style.color = analysis.flip.profit >= 0 ? '#00FF00' : '#FF0000';
    }
    
    // RENTAL ANALYSIS
    setText('rentalLoanAmount', formatCurrency(analysis.rental.loanAmount));
    setText('rentalInterestRate', analysis.rental.interestRate.toFixed(1) + '%');
    setText('rentalLoanTerm', analysis.rental.loanTerm + ' years');
    setText('rentalPI', formatCurrency(analysis.rental.monthlyPI));
    setText('rentalTaxes', formatCurrency(analysis.rental.monthlyTaxes));
    setText('rentalInsurance', formatCurrency(analysis.rental.monthlyInsurance));
    
    const pitiEl = document.getElementById('rentalPITI');
    if (pitiEl) {
        pitiEl.textContent = formatCurrency(analysis.rental.piti);
        pitiEl.style.color = '#00FFFF';
    }
    
    setText('rentalAVM', formatCurrency(analysis.rental.arv));
    setText('rentalCurrentLTV', analysis.rental.currentLTV.toFixed(1) + '%');
    setText('rentalMonthlyRent', formatCurrency(analysis.rental.monthlyRent));
    setText('rentalEffectiveRent', formatCurrency(analysis.rental.effectiveMonthlyRent));
    
    const cashFlowEl = document.getElementById('rentalCashFlow');
    if (cashFlowEl) {
        cashFlowEl.textContent = (analysis.rental.monthlyCashFlow >= 0 ? '+' : '-') + formatCurrency(Math.abs(analysis.rental.monthlyCashFlow));
        cashFlowEl.style.color = analysis.rental.monthlyCashFlow >= 0 ? '#00FF00' : '#FF0000';
    }
    
    setText('rentalAnnualCashFlow', formatCurrency(analysis.rental.annualCashFlow));
    
    // BRRR ANALYSIS
    setText('brrrMaxRefi', formatCurrency(analysis.brrr.maxRefinance));
    setText('brrrCashInvested', formatCurrency(analysis.brrr.cashInvested));
    setText('brrrCashLeft', formatCurrency(analysis.brrr.cashLeftInDeal));
    
    const pulloutEl = document.getElementById('brrrPulloutPossible');
    if (pulloutEl) {
        pulloutEl.textContent = analysis.brrr.canPullOut100 ? '✅ YES!' : '❌ NO';
        pulloutEl.style.color = analysis.brrr.canPullOut100 ? '#00FF00' : '#FF0000';
    }
    
    // DEAL RATING
    const ratingEl = document.getElementById('dealRating');
    if (ratingEl) {
        ratingEl.textContent = analysis.rating.rating;
        ratingEl.style.color = analysis.rating.score >= 7 ? '#FFD700' : analysis.rating.score >= 5 ? '#00FF00' : analysis.rating.score >= 3 ? '#FFA500' : '#FF0000';
    }
    
    const recEl = document.getElementById('dealRecommendation');
    if (recEl) {
        recEl.textContent = analysis.rating.recommendation;
    }
    
    const actionEl = document.getElementById('actionPlanText');
    if (actionEl) {
        actionEl.innerHTML = analysis.rating.actionPlan.replace(/\n/g, '<br>');
    }
    
    // Scroll to results
    if (dealSection) {
        dealSection.scrollIntoView({ behavior: 'smooth' });
    }
}

function setText(id, text) {
    const el = document.getElementById(id);
    if (el) el.textContent = text;
}

// Expose main functions to window for inline onclick handlers
window.runCalculations = runCalculations;

// ============================================
// SAVE/LOAD EVALUATIONS (localStorage)
// ============================================

function loadEvaluations() {
    try {
        const stored = localStorage.getItem('slopulator_evaluations');
        return stored ? JSON.parse(stored) : [];
    } catch (e) {
        return [];
    }
}

function saveEvaluations(evaluations) {
    localStorage.setItem('slopulator_evaluations', JSON.stringify(evaluations));
}

function saveEvaluation() {
    if (!calculationResults) {
        alert('Please calculate an analysis first! 🧮');
        return;
    }
    
    const evaluations = loadEvaluations();
    const purchasePrice = parseFloat(document.getElementById('purchasePrice').value) || 0;
    const repairs = parseFloat(document.getElementById('repairCost').value) || 0;
    const rentEstimate = parseFloat(document.getElementById('rentEstimate').value) || 0;
    
    const newEval = {
        id: Date.now(),
        address: currentAddress || document.getElementById('addressInput').value || 'Unknown',
        purchase_price: purchasePrice,
        repairs: repairs,
        arv: calculationResults.arv,
        rent_estimate: rentEstimate,
        monthly_cashflow: calculationResults.rental.monthlyCashFlow,
        flip_profit: calculationResults.flip.profit,
        created_at: new Date().toISOString()
    };
    
    evaluations.push(newEval);
    saveEvaluations(evaluations);
    
    // Celebrate!
    createSparkles(document.getElementById('saveEvalBtn'));
    alert('Evaluation saved! 💾✨');
}

function displayEvaluationsList() {
    const evaluations = loadEvaluations();
    const listEl = document.getElementById('evaluationsList');
    
    if (evaluations.length === 0) {
        listEl.innerHTML = '<font color="#FF6666" size="4">No saved evaluations found!</font>';
        return;
    }
    
    listEl.innerHTML = evaluations.map(eval => `
        <div class="evaluation-item" onclick="loadEvaluation(${eval.id})">
            <h4>${eval.address}</h4>
            <p>
                Purchase: ${formatCurrency(eval.purchase_price)} | 
                ARV: ${formatCurrency(eval.arv)} | 
                Cashflow: ${formatCurrency(eval.monthly_cashflow)}/mo | 
                Flip: ${formatCurrency(eval.flip_profit)}
            </p>
            <p style="font-size: 0.8rem; color: #666;">${new Date(eval.created_at).toLocaleString()}</p>
            <button class="retro-button-small" onclick="event.stopPropagation(); deleteEvaluation(${eval.id})" style="margin-top: 10px;">
                DELETE
            </button>
        </div>
    `).join('');
}

function loadEvaluation(id) {
    const evaluations = loadEvaluations();
    const eval = evaluations.find(e => e.id === id);
    
    if (!eval) {
        alert('Evaluation not found! 😱');
        return;
    }
    
    document.getElementById('addressInput').value = eval.address || '';
    currentAddress = eval.address || '';
    document.getElementById('purchasePrice').value = eval.purchase_price || '';
    document.getElementById('repairCost').value = eval.repairs || '';
    
    closeModal();
    
    // Load property data if address exists
    if (eval.address) {
        loadPropertyReachData(eval.address);
    }
    
    alert('Evaluation loaded! Click CALCULATE to see results! 📊');
}

function deleteEvaluation(id) {
    if (!confirm('Delete this evaluation? 🤔')) return;
    
    let evaluations = loadEvaluations();
    evaluations = evaluations.filter(e => e.id !== id);
    saveEvaluations(evaluations);
    displayEvaluationsList();
}

function closeModal() {
    document.getElementById('loadModal').style.display = 'none';
}

// ============================================
// COMP ME DADDY - DETAILED ANALYSIS
// ============================================

function showCompMeDaddyButton() {
    const btn = document.getElementById('compMeDaddyBtn');
    if (btn && currentPropertyData) {
        btn.style.display = 'inline-block';
        // Add sparkle animation
        setInterval(() => {
            if (btn.style.display !== 'none') {
                createSparkles(btn);
            }
        }, 3000);
    }
}

// Expose Comp Me Daddy functions globally
window.openCompMeDaddy = function() {
    // Effects
    fireConfetti();
    playWhipSound();
    
    // Get address from input
    const addr = document.getElementById('addressInput')?.value || '';
    console.log('Comp Me Daddy clicked with address:', addr);
    window.currentAddress = addr;
    
    // Show page
    document.getElementById('compMeDaddyPage').style.display = 'block';
    document.body.style.overflow = 'hidden';
    
    // Pre-fill address
    const cmdAddress = document.getElementById('compMeDaddyAddress');
    if (cmdAddress) {
        cmdAddress.value = addr;
    }
    
    // Auto-trigger analysis if address is valid
    if (addr && addr.length > 5) {
        setTimeout(function() {
            window.runCompMeDaddyAnalysis();
        }, 500);
    }
}

window.runCompMeDaddyAnalysis = async function() {
    const addressInput = document.getElementById('compMeDaddyAddress');
    if (!addressInput) {
        console.error('compMeDaddyAddress input not found!');
        alert('Error: Page not fully loaded. Please refresh.');
        return;
    }
    
    const address = addressInput.value;
    console.log('runCompMeDaddyAnalysis called with address:', address);
    
    if (!address || address.length < 5) {
        alert('Please enter a valid address! 🏠');
        return;
    }
    
    currentAddress = address;
    
    // Show loading state
    if (document.getElementById('rentcastAVMLoading')) {
        document.getElementById('rentcastAVMLoading').style.display = 'block';
    }
    if (document.getElementById('rentcastAVMData')) {
        document.getElementById('rentcastAVMData').style.display = 'none';
    }
    if (document.getElementById('detailedCompsBody')) {
        document.getElementById('detailedCompsBody').innerHTML = '<tr><td colspan="6" align="center"><font color="#00FF00">Loading comps...</font></td></tr>';
    }
    if (document.getElementById('propertyTake')) {
        document.getElementById('propertyTake').innerHTML = '<font color="#00FF00" face="Courier New">Analyzing market data...</font>';
    }
    if (document.getElementById('compsDashboard')) {
        document.getElementById('compsDashboard').style.display = 'none';
    }
    if (document.getElementById('avmJustification')) {
        document.getElementById('avmJustification').style.display = 'none';
    }
    
    // Load mock property data for this address
    await loadPropertyDataForCompMeDaddy(address);

    // Load all the analysis
    try {
        console.log('Starting PropertyReach data load...');
        await loadPropertyReachAVM();
        console.log('PropertyReach load completed');

        console.log('All analysis complete!');
    } catch (err) {
        console.error('Error in analysis:', err);
        const tbody = document.getElementById('detailedCompsBody');
        if (tbody) {
            tbody.innerHTML = '<tr><td colspan="6" align="center"><font color="#FF0000">Error loading data: ' + err.message + '</font></td></tr>';
        }
    }
}

async function loadPropertyDataForCompMeDaddy(address) {
    const PROXY_URL = 'https://srv1336418.hstgr.cloud/?url=';
    const API_KEY = 'live_u9JyD3Hmp58wmEQEnyZ5GosDjDcXHH5SuUN';
    
    // Parse address
    let streetAddress, city, state;
    if (address.includes(',')) {
        const parts = address.split(',').map(s => s.trim());
        streetAddress = parts[0] || '';
        city = parts[1] || '';
        state = parts[2]?.split(' ')[0] || '';
    } else {
        const parts = address.trim().split(' ');
        state = parts[parts.length - 1] || '';
        city = parts[parts.length - 2] || '';
        streetAddress = parts.slice(0, parts.length - 2).join(' ');
    }
    
    try {
        // Search for property
        const searchUrl = PROXY_URL + encodeURIComponent('https://api.propertyreach.com/v1/search');
        const body = {
            target: { city, state: state?.toUpperCase() },
            filter: { streetAddress: streetAddress.split(' ')[0] },
            limit: 50
        };
        
        const resp = await fetch(searchUrl, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'x-api-key': API_KEY },
            body: JSON.stringify(body)
        });
        
        if (!resp.ok) throw new Error('Search failed');
        
        const data = await resp.json();
        
        // Find matching property
        let prop = null;
        const streetNum = (streetAddress.split(' ')[0] || '').toLowerCase();
        
        if (data.properties && data.properties.length > 0) {
            for (let p of data.properties) {
                const pStreet = (p.streetAddress || '').toLowerCase();
                if (pStreet.startsWith(streetNum)) {
                    prop = p;
                    break;
                }
            }
            if (!prop) prop = data.properties[0];
        }
        
        if (prop) {
            // Fetch full property details
            const propUrl = PROXY_URL + encodeURIComponent('https://api.propertyreach.com/v1/property?streetAddress=' + encodeURIComponent(prop.streetAddress) + '&city=' + encodeURIComponent(city) + '&state=' + encodeURIComponent(state));
            const propResp = await fetch(propUrl);
            if (propResp.ok) {
                const propData = await propResp.json();
                if (propData.property) {
                    prop = propData.property;
                }
            }
            
            currentPropertyData = {
                estimatedValue: prop.estimatedValue || 0,
                rent_estimate: prop.estimatedRentAmount || 0
            };
            
            // Store values
            if (!window.compMeDaddyData) window.compMeDaddyData = {};
            window.compMeDaddyData.estimatedValue = prop.estimatedValue || 0;
        }
    } catch(e) {
        console.error('Comp Me Daddy error:', e);
    }
}

window.closeCompMeDaddy = function() {
    document.getElementById('compMeDaddyPage').style.display = 'none';
    document.body.style.overflow = 'auto';
}

// PropertyReach API Integration
const PROPERTYREACH_API_KEY = 'live_u9JyD3Hmp58wmEQEnyZ5GosDjDcXHH5SuUN';
const PROXY_URL_GLOBAL = 'https://srv1336418.hstgr.cloud/?url=';

async function loadPropertyReachAVM() {
    const PROXY_URL = 'https://srv1336418.hstgr.cloud/?url=';
    const loadingDiv = document.getElementById('rentcastAVMLoading');
    const dataDiv = document.getElementById('rentcastAVMData');
    const compsDashboard = document.getElementById('compsDashboard');
    
    if (loadingDiv) loadingDiv.style.display = 'block';
    if (dataDiv) dataDiv.style.display = 'none';
    if (compsDashboard) compsDashboard.style.display = 'none';
    
    try {
        console.log('loadPropertyReachAVM starting... (PropertyReach)');
        
        // Parse address - handle both comma and space separated
        let streetAddress, city, state;
        
        if (currentAddress.includes(',')) {
            const parts = currentAddress.split(',').map(s => s.trim());
            streetAddress = parts[0] || '';
            city = parts[1] || '';
            state = parts[2]?.split(' ')[0] || '';
            if (parts.length > 3) {
                city = parts[2] || '';
                state = parts[3] || '';
            }
        } else {
            // Space separated format
            const parts = currentAddress.trim().split(' ');
            state = parts[parts.length - 1] || '';
            city = parts[parts.length - 2] || '';
            streetAddress = parts.slice(0, parts.length - 2).join(' ');
        }
        
        // Normalize street address
        streetAddress = streetAddress
            .replace(/\bSouth\b/g, 'S')
            .replace(/\bNorth\b/g, 'N')
            .replace(/\bEast\b/g, 'E')
            .replace(/\bWest\b/g, 'W')
            .replace(/\bStreet\b/g, 'St')
            .replace(/\bAvenue\b/g, 'Ave')
            .replace(/\bDrive\b/g, 'Dr')
            .replace(/\bRoad\b/g, 'Rd')
            .replace(/\bLane\b/g, 'Ln')
            .replace(/\bCourt\b/g, 'Ct')
            .replace(/\bPlace\b/g, 'Pl')
            .replace(/\bBoulevard\b/g, 'Blvd')
            .replace(/\bCircle\b/g, 'Cir')
            .replace(/\bTerrace\b/g, 'Ter');
        
        // Convert state name to abbreviation
        const stateMap = {
            'Alabama':'AL','Alaska':'AK','Arizona':'AZ','Arkansas':'AR','California':'CA',
            'Colorado':'CO','Connecticut':'CT','Delaware':'DE','Florida':'FL','Georgia':'GA',
            'Hawaii':'HI','Idaho':'ID','Illinois':'IL','Indiana':'IN','Iowa':'IA',
            'Kansas':'KS','Kentucky':'KY','Louisiana':'LA','Maine':'ME','Maryland':'MD',
            'Massachusetts':'MA','Michigan':'MI','Minnesota':'MN','Mississippi':'MS','Missouri':'MO',
            'Montana':'MT','Nebraska':'NE','Nevada':'NV','NewHampshire':'NH','NewJersey':'NJ',
            'NewMexico':'NM','NewYork':'NY','NorthCarolina':'NC','NorthDakota':'ND','Ohio':'OH',
            'Oklahoma':'OK','Oregon':'OR','Pennsylvania':'PA','RhodeIsland':'RI','SouthCarolina':'SC',
            'SouthDakota':'SD','Tennessee':'TN','Texas':'TX','Utah':'UT','Vermont':'VT',
            'Virginia':'VA','Washington':'WA','WestVirginia':'WV','Wisconsin':'WI','Wyoming':'WY'
        };
        if (state.length > 2) {
            state = stateMap[state] || state.substring(0, 2).toUpperCase();
        }
        
        // Step 1: Get property details (ARV, estimated value)
        const propertyUrl = PROXY_URL + encodeURIComponent(`https://api.propertyreach.com/v1/property?streetAddress=${encodeURIComponent(streetAddress)}&city=${encodeURIComponent(city)}&state=${encodeURIComponent(state)}`);
        console.log('Fetching property:', propertyUrl);
        
        const propertyResponse = await fetch(propertyUrl, { 
            headers: { 
                'x-api-key': PROPERTYREACH_API_KEY,
                'Accept': 'application/json'
            } 
        });
        
        if (!propertyResponse.ok) {
            throw new Error(`PropertyReach property API error: ${propertyResponse.status}`);
        }
        
        const propertyData = await propertyResponse.json();
        console.log('Property data:', propertyData);
        
        if (!propertyData.property) {
            throw new Error('Property not found');
        }
        
        const subjectProperty = propertyData.property;
        const estimatedValue = subjectProperty.estimatedValue || 0;
        const lowRange = Math.round(estimatedValue * 0.92);
        const highRange = Math.round(estimatedValue * 1.08);
        
        // Step 2: Get comparables
        const compsUrl = PROXY_URL + encodeURIComponent('https://api.propertyreach.com/v1/comparables');
        console.log('Fetching comps:', compsUrl);
        
        const compsResponse = await fetch(compsUrl, { 
            method: 'POST',
            headers: { 
                'x-api-key': PROPERTYREACH_API_KEY,
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify({
                target: { streetAddress, city, state },
                limit: 15
            })
        });
        
        if (!compsResponse.ok) {
            throw new Error(`PropertyReach comps API error: ${compsResponse.status}`);
        }
        
        const compsData = await compsResponse.json();
        console.log('Comps data:', compsData);
        
        // Process PropertyReach comparables
        let allComps = compsData.properties || [];
        
        // Sort by distance
        allComps.sort((a, b) => (a.distanceFromSubject || 999) - (b.distanceFromSubject || 999));

        // Deduplicate comps by address
        const compMap = new Map();
        for (const comp of allComps) {
            const addr = comp.streetAddress || comp.addressLine1 || '';
            if (!compMap.has(addr)) {
                compMap.set(addr, comp);
            }
        }
        const uniqueComps = Array.from(compMap.values());
        
        // Filter: valid price AND decent finish level (exclude fixer-uppers for reno deals)
        const validComps = uniqueComps.filter(comp => {
            const price = Number(comp.lastSaleAmount || comp.lastSalePrice || 0);
            const sqft = Number(comp.squareFeet || 1);
            const pricePerSqft = sqft > 0 ? price / sqft : 0;

            // Skip if price is invalid
            if (price <= 0) return false;

            // Skip "needs work" and "fixer-upper" comps (below $85/sqft)
            if (pricePerSqft < 85) return false;

            return true;
        }).slice(0, 5);
        
        // Store data globally for sharing
        window.compMeDaddyData = {
            address: currentAddress,
            timestamp: new Date().toISOString()
        };
        
        // Store selected comps
        window.compMeDaddyData.selectedComps = validComps;
        
        // Calculate HIGH-END ARV based on filtered comps
        const subjectSqft = subjectProperty.squareFeet || 0;
        const highEndCompsPPSF = validComps
            .filter(c => c.squareFeet > 0)
            .map(c => {
                const price = Number(c.lastSaleAmount || c.lastSalePrice || 0);
                const sqft = Number(c.squareFeet || 1);
                return price / sqft;
            });
        
        // Calculate average $/sqft of quality comps
        const avgPPSF = highEndCompsPPSF.length > 0 
            ? highEndCompsPPSF.reduce((a, b) => a + b, 0) / highEndCompsPPSF.length 
            : 0;
        
        // Calculate renovated ARV
        const renovatedARV = subjectSqft > 0 && avgPPSF > 0 
            ? Math.round(subjectSqft * avgPPSF)
            : 0;
        
        window.compMeDaddyData.renovatedARV = renovatedARV;
        window.compMeDaddyData.avgCompPPSF = avgPPSF;
        
        // Calculate median price/sqft for comps
        const compPricesPerSqft = highEndCompsPPSF.sort((a, b) => a - b);
        
        const medianCompPricePerSqft = compPricesPerSqft.length > 0 
            ? compPricesPerSqft[Math.floor(compPricesPerSqft.length / 2)] 
            : 0;
        
        // Calculate subject property price/sqft
        const subjectPricePerSqft = subjectSqft > 0 ? estimatedValue / subjectSqft : 0;

        // Store subject property data for generatePropertyTake and other consumers
        window.compMeDaddyData.estimatedValue = estimatedValue;
        window.compMeDaddyData.subjectSqft = subjectSqft;
        window.compMeDaddyData.subjectPricePerSqft = subjectPricePerSqft;
        window.compMeDaddyData.subjectBeds = subjectProperty.bedrooms || 0;
        window.compMeDaddyData.subjectBaths = subjectProperty.bathrooms || 0;
        window.compMeDaddyData.subjectYearBuilt = subjectProperty.yearBuilt || '';
        
        // Generate AVM justification
        console.log('Generating AVM justification...');
        generateAVMJustification(estimatedValue, subjectPricePerSqft, medianCompPricePerSqft, validComps);

        // Populate detailed comps table
        console.log('Populating detailed comps...');
        populateDetailedComps();

        // Display comps dashboard
        console.log('Displaying comps dashboard...');
        displayCompsDashboard(validComps, subjectProperty, { price: estimatedValue, squareFootage: subjectProperty.squareFeet || 0 });

        // Generate property take
        console.log('Generating property take...');
        generatePropertyTake();

        // Display map
        console.log('Displaying map...');
        displayCompMap(subjectProperty, validComps);
        
        // Show avm justification
        const avmJust = document.getElementById('avmJustification');
        if (avmJust) avmJust.style.display = 'block';
        
        // Update basic AVM display
        if (document.getElementById('rentcastEstimate')) {
            document.getElementById('rentcastEstimate').textContent = formatCurrency(estimatedValue);
            document.getElementById('rentcastEstimate').style.color = '#00FFFF';
        }
        if (document.getElementById('rentcastRange')) {
            document.getElementById('rentcastRange').textContent = `${formatCurrency(lowRange)} - ${formatCurrency(highRange)}`;
        }
        if (document.getElementById('renovatedARV')) {
            document.getElementById('renovatedARV').textContent = formatCurrency(renovatedARV);
        }
        if (document.getElementById('compAvgPPSF')) {
            document.getElementById('compAvgPPSF').textContent = '$' + avgPPSF.toFixed(0) + '/sqft';
        }
        if (document.getElementById('rentcastConfidence')) {
            // PropertyReach doesn't have confidence score, estimate based on comp count
            const compCount = validComps.length;
            let confText = 'MEDIUM';
            let confColor = '#FFFF00';
            if (compCount >= 5) {
                confText = 'HIGH';
                confColor = '#00FF00';
            } else if (compCount < 2) {
                confText = 'LOW';
                confColor = '#FF0000';
            }
            const confEl = document.getElementById('rentcastConfidence');
            confEl.textContent = confText + ` (${compCount} comps)`;
            confEl.style.color = confColor;
        }

        // Inject subject property summary row into the AVM data div
        const subjectInfoId = 'subjectPropertyInfo';
        let subjectInfoEl = document.getElementById(subjectInfoId);
        if (!subjectInfoEl && dataDiv) {
            subjectInfoEl = document.createElement('div');
            subjectInfoEl.id = subjectInfoId;
            dataDiv.appendChild(subjectInfoEl);
        }
        if (subjectInfoEl) {
            const beds = subjectProperty.bedrooms || '';
            const baths = subjectProperty.bathrooms || '';
            const sqftDisp = subjectSqft || 'N/A';
            const yrBuilt = subjectProperty.yearBuilt || '';
            const parts = [];
            if (beds) parts.push(`🛏️ ${beds} Beds`);
            if (baths) parts.push(`🛁 ${baths} Baths`);
            if (sqftDisp !== 'N/A') parts.push(`📐 ${sqftDisp.toLocaleString()} sqft`);
            if (yrBuilt) parts.push(`🏗️ Built ${yrBuilt}`);
            subjectInfoEl.innerHTML = parts.length > 0
                ? `<br><table border="2" cellpadding="8" cellspacing="0" width="100%"><tr><td bgcolor="#002200" align="center"><font face="Courier New" color="#00FF00" size="2"><b>SUBJECT PROPERTY:</b> ${parts.join(' &nbsp;|&nbsp; ')}</font></td></tr></table>`
                : '';
        }
        
        // Generate share link
        generateShareLink();
        
        // Show the dashboard
        if (loadingDiv) loadingDiv.style.display = 'none';
        if (dataDiv) dataDiv.style.display = 'block';
        if (compsDashboard) compsDashboard.style.display = 'block';
        
    } catch (error) {
        console.error('Error loading PropertyReach data:', error);
        if (loadingDiv) loadingDiv.style.display = 'none';

        // Show error in dashboard
        const dashboard = document.getElementById('compsDashboard');
        if (dashboard) {
            dashboard.innerHTML = `
                <div style="padding: 20px; text-align: center;">
                    <font color="#FF0000" size="4"><b>⚠️ Error Loading Data</b></font><br><br>
                    <font color="#FFFF00">${error.message}</font><br><br>
                    <font color="#00FF00">Please check the address and try again.</font>
                </div>
            `;
            dashboard.style.display = 'block';
        }
    }
}

// Fetch PropertyReach property data including taxes
async function loadPropertyReachPropertyData(address) {
    try {
        const addressParts = address.split(',').map(s => s.trim());
        const streetAddress = addressParts[0] || '';
        const city = addressParts[1] || '';
        const state = addressParts[2]?.split(' ')[0] || '';
        
        const url = PROXY_URL + encodeURIComponent(`https://api.propertyreach.com/v1/property?streetAddress=${encodeURIComponent(streetAddress)}&city=${encodeURIComponent(city)}&state=${encodeURIComponent(state)}`);
        
        const response = await fetch(url, {
            headers: {
                'x-api-key': PROPERTYREACH_API_KEY,
                'Accept': 'application/json'
            }
        });
        
        if (!response.ok) {
            console.warn('PropertyReach property API error:', response.status);
            return null;
        }
        
        const data = await response.json();
        
        if (data && data.property) {
            const property = data.property;
            return {
                sqft: property.squareFeet || property.livingSquareFeet || 0,
                annualTaxes: property.taxAmount || 0,
                monthlyTaxes: property.taxAmount ? Math.round(property.taxAmount / 12) : 0,
                yearBuilt: property.yearBuilt || 0,
                bedrooms: property.bedrooms || 0,
                bathrooms: property.bathrooms || 0
            };
        }
        
        return null;
    } catch (error) {
        console.error('PropertyReach property data error:', error);
        return null;
    }
}

function populateDetailedComps() {
    const tbody = document.getElementById('detailedCompsBody');
    // Use PropertyReach comps from API response
    const comps = window.compMeDaddyData?.selectedComps || [];

    if (!comps.length) {
        tbody.innerHTML = '<tr><td colspan="7" align="center"><font color="#FF0000">No comps available from PropertyReach API</font></td></tr>';
        return;
    }

    tbody.innerHTML = comps.map((comp, index) => {
        // Handle PropertyReach response format
        const salePrice = Number(comp.lastSaleAmount || comp.lastSalePrice || 0);
        const sqft = Number(comp.squareFeet || 0);
        const pricePerSqft = sqft > 0 ? Math.round(salePrice / sqft) : '-';
        const distance = comp.distanceFromSubject ? Number(comp.distanceFromSubject).toFixed(2) : 'N/A';
        const finishLevel = determineFinishLevel(comp, pricePerSqft === '-' ? 0 : pricePerSqft);
        const finishColor = getFinishColor(finishLevel);
        
        // Parse date from ISO format
        let saleDate = 'N/A';
        const dateStr = comp.lastSaleDate;
        if (dateStr) {
            try {
                const d = new Date(dateStr);
                if (!isNaN(d.getTime())) {
                    saleDate = (d.getMonth() + 1) + '/' + d.getDate() + '/' + d.getFullYear();
                }
            } catch (e) {}
        }
        
        // Distance score (instead of correlation)
        const distanceScore = comp.distanceFromSubject ? 
            (comp.distanceFromSubject < 0.2 ? 'HIGH' : comp.distanceFromSubject < 0.5 ? 'MEDIUM' : 'LOW') : 'N/A';
        
        const address = comp.streetAddress || 'N/A';

        return `
            <tr bgcolor="${index % 2 === 0 ? '#000033' : '#000066'}">
                <td><font color="#00FFFF">${address}</font></td>
                <td align="center"><font color="#00FF00">${formatCurrency(salePrice)}</font></td>
                <td align="center"><font color="#FF9900">$${pricePerSqft}</font></td>
                <td align="center"><font color="#FFFF00">${saleDate}</font></td>
                <td align="center"><font color="#00FFFF">${distance} mi</font></td>
                <td align="center"><font color="#00FF00">${distanceScore}</font></td>
                <td align="center"><font color="${finishColor}"><b>${finishLevel}</b></font></td>
            </tr>
        `;
    }).join('');
}

function determineFinishLevel(comp, pricePerSqft) {
    // Analyze comp to determine finish level
    // This is based on price per sqft relative to market
    
    if (pricePerSqft > 180) return 'LUXURY';
    if (pricePerSqft > 140) return 'HIGH-END';
    if (pricePerSqft > 110) return 'UPDATED';
    if (pricePerSqft > 85) return 'AVERAGE';
    if (pricePerSqft > 60) return 'NEEDS WORK';
    return 'FIXER-UPPER';
}

function getFinishColor(level) {
    const colors = {
        'LUXURY': '#FF00FF',
        'HIGH-END': '#00FFFF',
        'UPDATED': '#00FF00',
        'AVERAGE': '#FFFF00',
        'NEEDS WORK': '#FF9900',
        'FIXER-UPPER': '#FF0000'
    };
    return colors[level] || '#FFFFFF';
}

function generatePropertyTake() {
    // Generate property valuation opinion based on comps
    const comps = window.compMeDaddyData?.selectedComps || [];
    const container = document.getElementById('propertyTake');
    
    if (!container) return;
    
    if (!comps.length) {
        const avmFallback = window.compMeDaddyData?.estimatedValue || 0;
        container.innerHTML = `
            <div style="background: #1a0000; border: 3px solid #FF6600; border-radius: 10px; padding: 20px; text-align: center;">
                <font color="#FF6600" size="4"><b>⚠️ No Qualifying Comparable Sales Found</b></font>
                <br><br>
                <font face="Courier New" color="#ffffff" size="2">
                    A valuation opinion cannot be generated without comparable sales data.<br><br>
                    <b style="color:#FFFF00;">Possible reasons:</b><br>
                    • Property is in a rural or low-activity market<br>
                    • No recent sales of similar properties within search radius<br>
                    • Property may be unique or recently built<br>
                    • Sales data may not yet be recorded in the database<br><br>
                    ${avmFallback > 0 ? `<b style="color:#00FFFF;">PropertyReach Estimated Value: ${formatCurrency(avmFallback)}</b><br>(Based on automated model — no comp support)` : ''}
                </font>
            </div>
        `;
        return;
    }
    
    // Get AVM and subject property data from stored compMeDaddyData
    const avmValue = window.compMeDaddyData.estimatedValue || 0;
    const subjectSqft = window.compMeDaddyData.subjectSqft || 0;
    const subjectPricePerSqft = window.compMeDaddyData.subjectPricePerSqft || (subjectSqft > 0 ? avmValue / subjectSqft : 0);
    
    // Calculate comp metrics
    const prices = comps.map(c => Number(c.lastSaleAmount || c.lastSalePrice || 0));
    const avgCompPrice = prices.reduce((a, b) => a + b, 0) / prices.length;
    const minCompPrice = Math.min(...prices);
    const maxCompPrice = Math.max(...prices);
    
    const sqfts = comps.map(c => Number(c.squareFeet || 0)).filter(s => s > 0);
    const avgCompSqft = sqfts.length > 0 ? sqfts.reduce((a, b) => a + b, 0) / sqfts.length : 0;
    const avgCompPricePerSqft = avgCompSqft > 0 ? Math.round(avgCompPrice / avgCompSqft) : 0;
    
    // Calculate price spreads
    const spreadLow = avmValue - minCompPrice;
    const spreadHigh = maxCompPrice - avmValue;
    const spreadPercentLow = avmValue > 0 ? (spreadLow / avmValue * 100) : 0;
    const spreadPercentHigh = avmValue > 0 ? (spreadHigh / avmValue * 100) : 0;
    
    // Determine finish level of subject based on price/sqft vs comps
    let finishAssessment = '';
    let finishColor = '';
    let valuationVerdict = '';
    let confidence = '';
    
    if (subjectPricePerSqft > avgCompPricePerSqft * 1.1) {
        finishAssessment = 'PREMIUM / HIGH-END';
        finishColor = '#FF00FF';
        valuationVerdict = 'The AVM appears aggressive. Subject is priced above comparable sales.';
        confidence = 'If the subject has superior finishes, larger lot, or better location, this could be justified. Otherwise, expect appraisal closer to $' + formatCurrency(Math.round(avgCompPrice)) + ' range.';
    } else if (subjectPricePerSqft > avgCompPricePerSqft * 0.95) {
        finishAssessment = 'UPDATED / MARKET';
        finishColor = '#00FF00';
        valuationVerdict = 'The AVM is well-supported by comparable sales.';
        confidence = 'Strong valuation confidence. Subject is priced in line with similar properties in the area.';
    } else if (subjectPricePerSqft > avgCompPricePerSqft * 0.8) {
        finishAssessment = 'AVERAGE / STANDARD';
        finishColor = '#FFFF00';
        valuationVerdict = 'The AVM is reasonable but leaves room for upside.';
        confidence = 'Conservative valuation. With light updates (paint, flooring), subject could justify higher end of range.';
    } else {
        finishAssessment = 'NEEDS WORK / VALUE-ADD';
        finishColor = '#FF9900';
        valuationVerdict = 'The AVM is conservative, indicating opportunity.';
        confidence = 'Excellent value-add potential. Even basic improvements could push value toward $' + formatCurrency(Math.round(avgCompPrice)) + ' range.';
    }
    
    // Generate the take HTML
    const html = `
        <div style="background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); border: 3px solid ${finishColor}; border-radius: 10px; padding: 20px;">
            <font face="Papyrus" color="${finishColor}" size="5"><b>🏠 ${finishAssessment} FINISH</b></font>
            <br><br>
            
            <table border="1" cellpadding="10" cellspacing="0" width="100%" style="margin-bottom: 20px;">
                <tr bgcolor="#000066">
                    <td width="50%"><font color="#FFFF00"><b>Subject PropertyReach:</b></font></td>
                    <td><font color="#00FFFF" size="4"><b>${formatCurrency(avmValue)}</b></font></td>
                </tr>

                <tr bgcolor="#000066">
                    <td><font color="#FFFF00"><b>Subject $/sqft:</b></font></td>
                    <td><font color="#00FF00">$${subjectPricePerSqft.toFixed(0)}</font></td>
                </tr>
                <tr bgcolor="#000033">
                    <td><font color="#FFFF00"><b>Comp Average:</b></font></td>
                    <td><font color="#00FF00">${formatCurrency(Math.round(avgCompPrice))} ($${avgCompPricePerSqft}/sqft)</font></td>
                </tr>
                <tr bgcolor="#000066">
                    <td><font color="#FFFF00"><b>Comp Range:</b></font></td>
                    <td><font color="#FFFF00">${formatCurrency(minCompPrice)} - ${formatCurrency(maxCompPrice)}</font></td>
                </tr>
            </table>
            
            <font face="Comic Sans MS" color="#00FFFF" size="4"><b>📊 THE VERDICT:</b></font>
            <br><br>
            <font face="Courier New" color="#ffffff" size="2">
                ${valuationVerdict}
                <br><br>
                <font color="#ffd700"><b>💡 ASSESSMENT:</b></font> ${confidence}
            </font>
            
            <br><br>
            <hr style="border-color: #333;">
            <br>
            
            <font face="Comic Sans MS" color="#FF00FF" size="3"><b>🎯 INVESTMENT STRATEGY:</b></font>
            <br><br>
            <font face="Courier New" color="#ffffff" size="2">
                ${generateStrategyText(finishAssessment, avmValue, avgCompPrice, subjectPricePerSqft, avgCompPricePerSqft)}
            </font>
        </div>
    `;
    
    container.innerHTML = html;
}

function generateStrategyText(finishLevel, avmValue, avgCompPrice, subjectPpsf, compPpsf) {
    const diff = avmValue - avgCompPrice;
    const diffPercent = avgCompPrice > 0 ? (diff / avgCompPrice * 100) : 0;
    
    if (finishLevel.includes('PREMIUM') || finishLevel.includes('HIGH-END')) {
        return `
            • <b>Flip Strategy:</b> Challenging. Already at top of market. Need to ensure finishes justify premium.<br>
            • <b>BRRRR Strategy:</b> Risky. Conservative ARV estimate recommended.<br>
            • <b>Recommendation:</b> Only pursue if you can acquire significantly below AVM or property has unique advantages.
        `;
    } else if (finishLevel.includes('UPDATED') || finishLevel.includes('MARKET')) {
        return `
            • <b>Flip Strategy:</b> Moderate. Focus on cosmetic updates only. Avoid major structural work.<br>
            • <b>BRRRR Strategy:</b> Solid. Rental income should support refinance at AVM.<br>
            • <b>Recommendation:</b> Good rental candidate. Cash flow should be positive with standard financing.
        `;
    } else if (finishLevel.includes('AVERAGE')) {
        return `
            • <b>Flip Strategy:</b> Good opportunity. Light reno ($15-25/sqft) can push value to comp average.<br>
            • <b>BRRRR Strategy:</b> Excellent. Forced appreciation potential through updates.<br>
            • <b>Recommendation:</b> Ideal value-add play. Budget for kitchen/bath refresh, flooring, paint.
        `;
    } else {
        return `
            • <b>Flip Strategy:</b> Excellent opportunity. Full reno can capture ${diffPercent.toFixed(0)}% upside to comp average.<br>
            • <b>BRRRR Strategy:</b> Very strong. Significant forced appreciation potential.<br>
            • <b>Recommendation:</b> Best case for value-add. Plan comprehensive renovation for maximum ARV.
        `;
    }
}

// ============================================
// EVENT LISTENERS
// ============================================

document.addEventListener('DOMContentLoaded', () => {
    // Initialize
    initVisitorCounter();
    initBouncingEmojis();
    
    // Welcome alert (retro style)
    setTimeout(() => {
        if (!localStorage.getItem('slopulator_visited')) {
            alert('Welcome to the SLOPULATOR, brother! 🏠💰🔨\n\nThe ULTIMATE tool for real estate investors!');
            localStorage.setItem('slopulator_visited', 'true');
        }
    }, 1000);
    
    // Address input
    const addressInput = document.getElementById('addressInput');
    if (!addressInput) {
        console.error('Address input element not found!');
    } else {
        console.log('Address input found, attaching listeners');
        addressInput.addEventListener('input', (e) => {
            handleAddressInput(e.target.value);
        });
        
        addressInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                // On Enter, if suggestions are showing, pick the first one
                const el = document.getElementById('addressSuggestions');
                const first = el?.querySelector('.suggestion-item');
                if (first) { first.click(); }
                else { handleAddressInput(e.target.value); }
            }
        });
    }
    
    // Hide suggestions when clicking outside
    document.addEventListener('click', (e) => {
        const suggestionsEl = document.getElementById('addressSuggestions');
        const addressInput = document.getElementById('addressInput');
        if (suggestionsEl && e.target !== addressInput && !suggestionsEl.contains(e.target)) {
            suggestionsEl.style.display = 'none';
        }
    });
    
    // Search button
    document.getElementById('searchBtn').addEventListener('click', () => {
        const query = addressInput.value;
        if (query.length >= 3) {
            handleAddressInput(query);
        } else {
            alert('Please enter at least 3 characters! 🔍');
        }
    });
    
    // Calculate button
    // calculateBtn removed from DOM - SLOP MY DEAL is the single calculate trigger
    if (document.getElementById('calculateBtn')) document.getElementById('calculateBtn').addEventListener('click', runCalculations);
    
    // Comp Me Daddy button (with null check)
    const compMeDaddyBtn = document.getElementById('compMeDaddyBtn');
    if (compMeDaddyBtn) {
        console.log('Comp Me Daddy button found, attaching listener');
        const handleClick = function(e) {
            console.log('Comp Me Daddy button clicked!');
            e.preventDefault();
            e.stopPropagation();
            window.openCompMeDaddy();
        };
        compMeDaddyBtn.addEventListener('click', handleClick);
        compMeDaddyBtn.addEventListener('touchstart', handleClick, {passive: false});
    } else {
        console.log('Comp Me Daddy button NOT found!');
    }
    
    // Comp Me Daddy search button (with null check)
    const compMeDaddySearchBtn = document.getElementById('compMeDaddySearchBtn');
    if (compMeDaddySearchBtn) {
        compMeDaddySearchBtn.addEventListener('click', window.runCompMeDaddyAnalysis);
    }
    
    // Check if address was already selected before page loaded
    if (window.selectedAddress) {
        window.loadPropertyData(window.selectedAddress, window.selectedLat, window.selectedLon);
    }
    
    // Comp Me Daddy address input (Enter key) (with null check)
    const compMeDaddyAddress = document.getElementById('compMeDaddyAddress');
    if (compMeDaddyAddress) {
        compMeDaddyAddress.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                runCompMeDaddyAnalysis();
            }
        });
    }
    
    // Save/Load/Print buttons
    document.getElementById('saveEvalBtn').addEventListener('click', saveEvaluation);
    
    document.getElementById('loadEvalBtn').addEventListener('click', () => {
        displayEvaluationsList();
        document.getElementById('loadModal').style.display = 'flex';
    });
    
    document.getElementById('printBtn').addEventListener('click', () => {
        if (!calculationResults) {
            alert('Calculate something first! 🧮');
            return;
        }
        window.print();
    });
    
    // Close modal when clicking outside
    document.getElementById('loadModal').addEventListener('click', (e) => {
        if (e.target.id === 'loadModal') {
            closeModal();
        }
    });
    
    // Add hover sparkles to buttons
    document.querySelectorAll('button, input').forEach(el => {
        el.addEventListener('mouseenter', () => {
            if (Math.random() > 0.7) {
                createSparkles(el);
            }
        });
    });
});

// ============================================
// COMP ME DADDY - ANALYSIS FUNCTIONS
// ============================================

function generateAVMJustification(avmValue, subjectPricePerSqft, medianCompPricePerSqft, comps) {
    const subjectSqft = subjectPricePerSqft > 0 ? avmValue / subjectPricePerSqft : 0;
    const justificationEl = document.getElementById('avmJustification');
    if (!justificationEl || comps.length === 0) return;
    
    const highestComp = comps.reduce((max, comp) => 
        (comp.lastSalePrice / (comp.squareFootage || 1)) > (max.lastSalePrice / (max.squareFootage || 1)) ? comp : max
    , comps[0]);
    
    const highestCompAddress = highestComp.formattedAddress || highestComp.addressLine1 || 'the highest comp';
    const highestCompPricePerSqft = highestComp.lastSalePrice && highestComp.squareFootage > 0 
        ? (highestComp.lastSalePrice / highestComp.squareFootage).toFixed(0) 
        : 'N/A';
    
    let justification = '';
    const diff = subjectPricePerSqft - medianCompPricePerSqft;
    const diffPercent = medianCompPricePerSqft > 0 ? (diff / medianCompPricePerSqft * 100) : 0;
    
    if (diffPercent > 5) {
        justification = `
            <div style="background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); border: 3px solid #ff6b6b; border-radius: 10px; padding: 20px; margin: 15px 0;">
                <font face="Papyrus" color="#ff6b6b" size="4"><b>📊 PropertyReach Value ASSESSMENT: AGGRESSIVE</b></font><br><br>
                <font face="Courier New" color="#ffffff" size="2">
                The PropertyReach ARV of <b>${formatCurrency(avmValue)}</b> (${subjectSqft > 0 ? (avmValue / subjectSqft).toFixed(0) + "/sqft" : "N/A"}) is 
                <b>${diffPercent.toFixed(1)}% higher</b> than the median comp price/sqft of $${medianCompPricePerSqft.toFixed(0)}.<br><br>
                
                This aggressive valuation is likely supported by <b>${highestCompAddress}</b>, which sold at 
                ${highestCompPricePerSqft ? "$" + highestCompPricePerSqft + "/sqft" : "N/A"} and is only ${highestComp.distance?.toFixed(2) || 'unknown'} miles away.<br><br>
                
                <font color="#ffd700"><b>💡 Appraisal Insight:</b></font> Expect the appraiser to anchor toward the 
                median range unless your subject property has significant advantages (larger lot, better condition, 
                recent updates) over the comparable sales.
                </font>
            </div>
        `;
    } else if (diffPercent < -5) {
        justification = `
            <div style="background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); border: 3px solid #4ecdc4; border-radius: 10px; padding: 20px; margin: 15px 0;">
                <font face="Papyrus" color="#4ecdc4" size="4"><b>📊 PropertyReach Value ASSESSMENT: CONSERVATIVE</b></font><br><br>
                <font face="Courier New" color="#ffffff" size="2">
                The PropertyReach ARV of <b>${formatCurrency(avmValue)}</b> (${subjectSqft > 0 ? (avmValue / subjectSqft).toFixed(0) + "/sqft" : "N/A"}) is 
                <b>${Math.abs(diffPercent).toFixed(1)}% lower</b> than the median comp price/sqft of $${medianCompPricePerSqft.toFixed(0)}.<br><br>
                
                This conservative valuation may reflect historical data patterns or the subject's last sale price. 
                The comparable sales suggest stronger market support at higher values.<br><br>
                
                <font color="#ffd700"><b>💡 Appraisal Insight:</b></font> This presents an opportunity! The appraisal 
                should come in at or above the AVM. If renovating, you have room to create equity above the projected value.
                </font>
            </div>
        `;
    } else {
        justification = `
            <div style="background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); border: 3px solid #00ff00; border-radius: 10px; padding: 20px; margin: 15px 0;">
                <font face="Papyrus" color="#00ff00" size="4"><b>📊 PropertyReach Value ASSESSMENT: STRONGLY SUPPORTED</b></font><br><br>
                <font face="Courier New" color="#ffffff" size="2">
                The PropertyReach ARV of <b>${formatCurrency(avmValue)}</b> (${subjectSqft > 0 ? (avmValue / subjectSqft).toFixed(0) + "/sqft" : "N/A"}) is 
                <b>within ${Math.abs(diffPercent).toFixed(1)}%</b> of the median comp price/sqft of $${medianCompPricePerSqft.toFixed(0)}.<br><br>
                
                This AVM is strongly supported by the local market data. The selected comparables show consistent 
                pricing within a tight range around your subject property.<br><br>
                
                <font color="#ffd700"><b>💡 Appraisal Insight:</b></font> High confidence in this valuation. 
                Expect the appraisal to align closely with the AVM, assuming typical property condition and no 
                unusual market factors.
                </font>
            </div>
        `;
    }
    
    justificationEl.innerHTML = justification;
}

function displayCompsDashboard(comps, subjectProperty, avmData) {
    const dashboard = document.getElementById('compsDashboard');
    if (!dashboard) return;
    
    const avmValue = avmData.price || 0;
    const subjectSqft = avmData.squareFootage || subjectProperty.squareFeet || 0;

    // Handle zero comps case
    if (!comps || comps.length === 0) {
        dashboard.innerHTML = `
            <div style="background: #0a0a0a; border: 3px groove #ffd700; padding: 30px; margin: 20px 0; text-align: center;">
                <font face="Comic Sans MS" color="#ffd700" size="5"><b>🏘️ COMPARABLE SALES</b></font>
                <br><br>
                <font color="#FF6600" size="4"><b>⚠️ No Qualifying Comps Found</b></font>
                <br><br>
                <font face="Courier New" color="#ffffff" size="2">
                    This can happen for several reasons:<br><br>
                    • <b style="color:#FFFF00;">Rural area</b> — limited recent sales activity<br>
                    • <b style="color:#FFFF00;">Recently built</b> — insufficient comparable sales history<br>
                    • <b style="color:#FFFF00;">Unique property</b> — no similar homes nearby<br>
                    • <b style="color:#FFFF00;">Data lag</b> — sales may not yet be recorded in the database<br><br>
                    <font color="#00FF00">Try expanding your search area or adjusting filters.</font>
                </font>
            </div>
        `;
        dashboard.style.display = 'block';
        return;
    }
    
    let html = `
        <div style="background: #0a0a0a; border: 3px groove #ffd700; padding: 20px; margin: 20px 0;">
            <font face="Comic Sans MS" color="#ffd700" size="5">
                <b>🏘️ TOP ${comps.length} COMPARABLE SALES</b>
            </font>
            <br><br>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 15px;">
    `;
    
    comps.forEach((comp, index) => {
        const salePrice = Number(comp.lastSaleAmount || comp.lastSalePrice || 0);
        const sqft = Number(comp.squareFeet || 0);
        const pricePerSqft = sqft > 0 ? (salePrice / sqft).toFixed(0) : 'N/A';

        // Format sale date nicely
        let saleDate = 'N/A';
        if (comp.lastSaleDate) {
            try {
                const d = new Date(comp.lastSaleDate);
                saleDate = d.toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' });
            } catch(e) { saleDate = comp.lastSaleDate; }
        }

        const distance = comp.distanceFromSubject != null ? Number(comp.distanceFromSubject).toFixed(2) : 'N/A';

        // Proximity score based on distance (closer = higher score)
        let proximityScore = 'N/A';
        if (comp.distanceFromSubject != null) {
            const d = Number(comp.distanceFromSubject);
            if (d < 0.25) proximityScore = '🟢 Very Close';
            else if (d < 0.5) proximityScore = '🟡 Close';
            else if (d < 1.0) proximityScore = '🟠 Moderate';
            else proximityScore = '🔴 Far';
        }

        const address = comp.streetAddress || comp.addressLine1 || 'N/A';

        // Beds/baths/year built extras
        let extraDetails = '';
        if (comp.bedrooms || comp.bathrooms) {
            const beds = comp.bedrooms ? `${comp.bedrooms} bd` : '';
            const baths = comp.bathrooms ? `${comp.bathrooms} ba` : '';
            extraDetails += `<b>🛏️ Beds/Baths:</b> ${[beds, baths].filter(Boolean).join(' / ')}<br>`;
        }
        if (comp.yearBuilt) {
            extraDetails += `<b>🏗️ Year Built:</b> ${comp.yearBuilt}<br>`;
        }
        
        html += `
            <div style="background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); border: 2px solid #00ff00; border-radius: 10px; padding: 15px;">
                <font face="Papyrus" color="#ff00ff" size="3"><b>Comp #${index + 1}</b></font>
                <hr style="border-color: #333; margin: 10px 0;">
                <font face="Courier New" color="#ffffff" size="2">
                    <b>📍 Address:</b><br>
                    <span style="color: #00ffff;">${address}</span><br><br>
                    
                    <b>💰 Sale Price:</b> <span style="color: #00ff00; font-size: 16px;">${formatCurrency(salePrice)}</span><br>
                    <b>📅 Sold:</b> ${saleDate}<br>
                    <b>📏 Distance:</b> ${distance} miles<br>
                    <b>📐 Sqft:</b> ${sqft || 'N/A'}<br>
                    <b>💵 Price/Sqft:</b> <span style="color: #ffd700;">$${pricePerSqft}</span><br>
                    ${extraDetails}<b>📍 Proximity:</b> ${proximityScore}
                </font>
            </div>
        `;
    });

    // Subject property card
    const subjectAddress = subjectProperty.streetAddress 
        ? `${subjectProperty.streetAddress}, ${subjectProperty.city || ''}, ${subjectProperty.state || ''}`.replace(/, ,/, ',').replace(/,\s*$/, '')
        : currentAddress;
    const subjectBeds = window.compMeDaddyData?.subjectBeds || subjectProperty.bedrooms || '';
    const subjectBaths = window.compMeDaddyData?.subjectBaths || subjectProperty.bathrooms || '';
    const subjectYearBuilt = window.compMeDaddyData?.subjectYearBuilt || subjectProperty.yearBuilt || '';
    
    let subjectExtras = '';
    if (subjectBeds || subjectBaths) {
        subjectExtras += ` | <b>Beds/Baths:</b> ${subjectBeds || '?'}bd / ${subjectBaths || '?'}ba`;
    }
    if (subjectYearBuilt) {
        subjectExtras += ` | <b>Built:</b> ${subjectYearBuilt}`;
    }

    html += `
            </div>
            
            <div style="background: linear-gradient(135deg, #330000 0%, #220000 100%); border: 3px solid #ff6b6b; border-radius: 10px; padding: 20px; margin-top: 20px;">
                <font face="Comic Sans MS" color="#ff6b6b" size="4"><b>🎯 SUBJECT PROPERTY</b></font>
                <hr style="border-color: #ff6b6b;">
                <font face="Courier New" color="#ffffff" size="3">
                    <b>Address:</b> <span style="color: #00ffff;">${subjectAddress}</span><br>
                    <b>AVM Value:</b> <span style="color: #00ff00; font-size: 20px;">${formatCurrency(avmValue)}</span><br>
                    <b>Sqft:</b> ${subjectSqft || 'N/A'} | 
                    <b>Price/Sqft:</b> <span style="color: #ffd700;">$${subjectSqft > 0 ? (avmValue / subjectSqft).toFixed(0) : 'N/A'}</span>${subjectExtras}
                </font>
            </div>
        </div>
    `;
    
    dashboard.innerHTML = html;
}

let compMap = null;

function displayCompMap(subjectProperty, comps) {
    const mapContainer = document.getElementById('compMap');
    if (!mapContainer) return;

    const subjectLat = parseFloat(subjectProperty?.latitude || window.selectedLat);
    const subjectLon = parseFloat(subjectProperty?.longitude || window.selectedLon);

    if (!subjectLat || !subjectLon) {
        mapContainer.innerHTML = '<font color="#FF0000">Map coordinates not available</font>';
        return;
    }

    // Clear previous map instance
    if (compMap) {
        compMap.remove();
    }

    // Create new map with dark theme
    compMap = L.map('compMap', {
        center: [subjectLat, subjectLon],
        zoom: 14,
        zoomControl: false,
        attributionControl: false
    });

    // Add OSM tiles (blue water, yellow highways - like hoodmaps)
    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
        maxZoom: 19
    }).addTo(compMap);

    // Add zoom control to bottom right
    L.control.zoom({ position: 'bottomright' }).addTo(compMap);

    // Custom marker styles
    const subjectIcon = L.divIcon({
        className: 'custom-marker',
        html: '<div style="background-color:#FF0000;width:24px;height:24px;border-radius:50%;border:3px solid #FFFFFF;box-shadow:0 0 15px #FF0000, 0 0 30px #FF0000;display:flex;align-items:center;justify-content:center;"><span style="color:#FFF;font-size:12px;font-weight:bold;">★</span></div>',
        iconSize: [24, 24],
        iconAnchor: [12, 12]
    });

    // Add subject property marker
    L.marker([subjectLat, subjectLon], { icon: subjectIcon })
        .addTo(compMap)
        .bindPopup('<b style="color:#FF0000;">🏠 SUBJECT PROPERTY</b><br>' + (currentAddress || 'Target Property'));

    // Add comp markers with numbers
    const compColors = ['#00FFFF', '#00FF00', '#FFFF00', '#FF9900', '#FF00FF'];
    const bounds = [[subjectLat, subjectLon]];

    comps.forEach((comp, index) => {
        if (!comp.latitude || !comp.longitude) return;

        const lat = parseFloat(comp.latitude);
        const lon = parseFloat(comp.longitude);
        bounds.push([lat, lon]);

        const color = compColors[index % compColors.length];
        const compIcon = L.divIcon({
            className: 'custom-marker',
            html: `<div style="background-color:${color};width:28px;height:28px;border-radius:50%;border:3px solid #000;box-shadow:0 0 10px ${color};display:flex;align-items:center;justify-content:center;"><span style="color:#000;font-size:14px;font-weight:bold;">${index + 1}</span></div>`,
            iconSize: [28, 28],
            iconAnchor: [14, 14]
        });

        const price = formatCurrency(Number(comp.price || comp.lastSalePrice || 0));
        const address = comp.formattedAddress || comp.addressLine1 || 'Comp ' + (index + 1);

        L.marker([lat, lon], { icon: compIcon })
            .addTo(compMap)
            .bindPopup(`<b style="color:${color};">🏘️ COMP #${index + 1}</b><br>${address}<br><b>${price}</b>`);
    });

    // Fit bounds to show all markers
    if (bounds.length > 1) {
        compMap.fitBounds(bounds, { padding: [50, 50] });
    }
}

function generateShareLink() {
    const shareContainer = document.getElementById('shareLinkContainer');
    if (!shareContainer || !window.compMeDaddyData) return;
    
    const shareText = `Here is a comp analysis for ${window.compMeDaddyData.address}`;
    const encodedText = encodeURIComponent(shareText);
    const currentUrl = window.location.href.split('?')[0];
    const shareUrl = `${currentUrl}?share=${encodedText}`;
    
    shareContainer.innerHTML = `
        <div style="background: #001a33; border: 2px solid #00ff00; padding: 15px; margin: 15px 0; border-radius: 8px;">
            <font face="Comic Sans MS" color="#00ff00" size="3"><b>🔗 SHARE THIS ANALYSIS</b></font><br><br>
            <textarea id="shareText" readonly style="width: 100%; height: 60px; background: #000; color: #0f0; border: 1px solid #00ff00; padding: 10px; font-family: monospace; resize: none;">${shareText}

${shareUrl}</textarea>
            <br><br>
            <button onclick="copyShareText()" style="background: linear-gradient(45deg, #00ff00, #00aa00); color: #000; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; font-weight: bold;">
                📋 COPY TO CLIPBOARD
            </button>
        </div>
    `;
}

window.copyShareText = function() {
    const textarea = document.getElementById('shareText');
    if (textarea) {
        textarea.select();
        document.execCommand('copy');
        alert('Copied to clipboard! 📋');
    }
};

// ============================================
// KEYBOARD SHORTCUTS
// ============================================

document.addEventListener('keydown', (e) => {
    // Ctrl+Enter to calculate
    if (e.ctrlKey && e.key === 'Enter') {
        runCalculations();
    }
    // Escape to close modals
    if (e.key === 'Escape') {
        closeModal();
        closeEasterEgg();
        closeCompMeDaddy();
    }
});

// ============================================
// SHARE FUNCTIONS
// ============================================

function shareCompMeDaddy() {
    if (!window.compMeDaddyData) {
        alert('Run an analysis first! 📊');
        return;
    }
    
    const data = window.compMeDaddyData;
    
    // Get additional fields from DOM
    const repairCost = document.getElementById('repairCost')?.value || '0';
    const purchasePrice = document.getElementById('purchasePrice')?.value || '0';
    const flipProfit = (document.getElementById('flipProfit')?.textContent || '0').replace(/[+$, ]/g, '');
    const monthlyRent = (document.getElementById('rentEstimate')?.value || '0').replace(/[$,]/g, '');
    const maxRefi = parseFloat((document.getElementById('brrrMaxRefi')?.textContent || '0').replace(/[$,]/g, '')) || 0;
    
    // Calculate BRRRR cash out %
    let cashOutPct = '0%';
    const totalCost = parseFloat(purchasePrice || 0) + parseFloat(repairCost || 0);
    if (totalCost > 0 && maxRefi > 0) {
        cashOutPct = Math.min(100, Math.round((maxRefi / totalCost) * 100)) + "%";
    }
    
    const renovatedARV = data.renovatedARV ? '$' + data.renovatedARV.toLocaleString() : 'N/A';
    const avgPPSF = data.avgCompPPSF ? '$' + data.avgCompPPSF.toFixed(0) + '/sqft' : 'N/A';
    const compCount = data.selectedComps ? data.selectedComps.length : 0;
    const address = data.address || document.getElementById('addressInput')?.value || 'Property';
    
    const shareText = `🏠 Comp Analysis for ${address}\n\n💎 Renovated ARV: ${renovatedARV}\n📐 Avg Comp $/sqft: ${avgPPSF}\n📊 Comps Used: ${compCount}\n\n💵 Purchase: $${purchasePrice}\n🔨 Repairs: $${repairCost}\n🔨 Flip Profit: $${flipProfit}\n💵 Monthly Rent: $${monthlyRent}/mo\n🏦 BRRRR Cash Out: ${cashOutPct}\n\nPowered by The Slopulator! 🔥`;
    
    if (navigator.share) {
        navigator.share({
            title: 'Property Comp Analysis - The Slopulator',
            text: shareText
        }).catch(err => console.log('Share cancelled'));
    } else {
        // Fallback - copy to clipboard
        navigator.clipboard.writeText(shareText).then(() => {
            alert('Analysis copied to clipboard! 📋');
        });
    }
}

function shareDealAnalysis() {
    const address = document.getElementById('addressInput')?.value || 'Property';
    const purchasePrice = document.getElementById('purchasePrice')?.value || '0';
    const repairs = document.getElementById('repairCost')?.value || '0';
    const arv = document.getElementById('arvInput')?.value || '0';
    const rating = document.getElementById('dealRating')?.textContent || '--';
    // Read from DOM elements - strip $ and convert to number
    const flipProfitEl = document.getElementById('flipProfit');
    const cashFlowEl = document.getElementById('rentalCashFlow');
    const brrrEl = document.getElementById('brrrMaxRefi');
    const flipProfit = parseFloat(flipProfitEl?.textContent?.replace(/[+$, ]/g, '')) || 0;
    const maxRefi = parseFloat(brrrEl?.textContent?.replace(/[+$, ]/g, '')) || 0;
    const monthlyCashFlow = parseFloat(document.getElementById('rentalCashFlow')?.textContent?.replace(/[+$, ]/g, '')) || 0;
    const monthlyRent = document.getElementById('rentEstimate')?.value || '0';
    
    let cashOutPct = '0%';
    const totalCost = parseFloat(purchasePrice || 0) + parseFloat(repairs || 0);
    if (totalCost > 0 && maxRefi > 0) {
        cashOutPct = Math.min(100, Math.round((maxRefi / totalCost) * 100)) + "%";
    }
    
    const shareText = `🏠 Deal Analysis for ${address}\n\n💵 Purchase: $${purchasePrice}\n🔨 Repairs: $${repairs}\n💎 ARV: $${arv}\n🔨 Flip Profit: $${flipProfit}\n💵 Cash Flow: $${monthlyCashFlow}/mo | Rent: $${monthlyRent}/mo\n🏦 BRRRR Cash Out: ${cashOutPct}\n🏆 Rating: ${rating}\n\nPowered by The Slopulator! 🔥`;
    
    if (navigator.share) {
        navigator.share({
            title: 'Deal Analysis - The Slopulator',
            text: shareText
        }).catch(err => console.log('Share cancelled'));
    } else {
        // Fallback - copy to clipboard
        navigator.clipboard.writeText(shareText).then(() => {
            alert('Analysis copied to clipboard! 📋');
        });
    }
}

// ============================================
// EXPOSE FUNCTIONS TO WINDOW
// ============================================

window.runComprehensiveAnalysis = runCalculations;
window.shareCompMeDaddy = shareCompMeDaddy;
window.shareDealAnalysis = shareDealAnalysis;

// ============================================
// ADDRESS AUTOCOMPLETE
// ============================================

let acTimeout;
let acGeneration = 0; // Increments each keystroke; stale results check against this

// State detection helpers
const STATE_ABBREVS = { 'OK': 'Oklahoma', 'IN': 'Indiana', 'AL':'Alabama','AK':'Alaska','AZ':'Arizona','AR':'Arkansas','CA':'California','CO':'Colorado','CT':'Connecticut','DE':'Delaware','FL':'Florida','GA':'Georgia','HI':'Hawaii','ID':'Idaho','IL':'Illinois','IA':'Iowa','KS':'Kansas','KY':'Kentucky','LA':'Louisiana','ME':'Maine','MD':'Maryland','MA':'Massachusetts','MI':'Michigan','MN':'Minnesota','MS':'Mississippi','MO':'Missouri','MT':'Montana','NE':'Nebraska','NV':'Nevada','NH':'New Hampshire','NJ':'New Jersey','NM':'New Mexico','NY':'New York','NC':'North Carolina','ND':'North Dakota','OH':'Ohio','OR':'Oregon','PA':'Pennsylvania','RI':'Rhode Island','SC':'South Carolina','SD':'South Dakota','TN':'Tennessee','TX':'Texas','UT':'Utah','VT':'Vermont','VA':'Virginia','WA':'Washington','WV':'West Virginia','WI':'Wisconsin','WY':'Wyoming' };

function hasStateInQuery(query) {
    const q = query.toUpperCase();
    // Check for state abbreviation after comma or at end: ", OK" ", IN" etc.
    if (/,\s*[A-Z]{2}\b/.test(query)) return true;
    // Check for full state names
    for (const name of Object.values(STATE_ABBREVS)) {
        if (query.toLowerCase().includes(name.toLowerCase())) return true;
    }
    return false;
}

async function nominatimSearch(query) {
    const url = `https://nominatim.openstreetmap.org/search?q=${encodeURIComponent(query)}&format=json&addressdetails=1&limit=5&countrycodes=us`;
    const resp = await fetch(url, { headers: { 'User-Agent': 'Slopulator/1.0' } });
    if (!resp.ok) return [];
    return await resp.json();
}

function handleAddressInput(value) {
    clearTimeout(acTimeout);
    const el = document.getElementById('addressSuggestions');
    if (!el) return;
    if (value.length < 3) { el.style.display = 'none'; return; }
    
    const gen = ++acGeneration; // Capture this search's generation

    acTimeout = setTimeout(async () => {
        try {
            let results = [];

            if (hasStateInQuery(value)) {
                // User already specified a state — search as-is
                results = await nominatimSearch(value);
            } else {
                // No state specified — bias toward OK and IN in parallel
                const [okResults, inResults, rawResults] = await Promise.all([
                    nominatimSearch(value + ', Oklahoma'),
                    nominatimSearch(value + ', Indiana'),
                    nominatimSearch(value)
                ]);
                // Merge: OK first, then IN, then anything else from raw not already included
                const seen = new Set();
                for (const r of [...okResults, ...inResults, ...rawResults]) {
                    const key = r.place_id || r.display_name;
                    if (!seen.has(key)) {
                        seen.add(key);
                        results.push(r);
                    }
                }
                results = results.slice(0, 7);
            }

            // Discard if a newer search already fired
            if (gen !== acGeneration) return;

            if (results.length > 0) {
                // Filter to house/building/address results only (exclude parks, counties, etc.)
                const addressTypes = new Set(['house','building','residential','apartments','yes','street','road']);
                const filtered = results.filter(p => {
                    const t = (p.type || '').toLowerCase();
                    const c = (p.class || '').toLowerCase();
                    // Keep if it looks like an address (has a house number) or is a place type we want
                    return p.display_name.match(/^\d/) || c === 'place' || c === 'highway' || addressTypes.has(t);
                });
                const toShow = filtered.length > 0 ? filtered : results;

                el.innerHTML = toShow.slice(0, 6).map(place => {
                    const short = formatShortAddress(place.display_name);
                    const parts = place.display_name.split(',').map(p => p.trim());
                    const city = parts[2] || parts[1] || '';
                    const stateZip = parts.slice(-3, -1).join(', ');
                    const display = `<strong style="color:#00FF00;">${parts[0]}</strong> <span style="color:#888;">${parts[1] ? parts[1] + ',' : ''}</span><br><span style="color:#00FFFF;font-size:0.85em;">${city}${stateZip ? ' · ' + stateZip : ''}</span>`;
                    return `<div class="suggestion-item" style="padding:10px;cursor:pointer;border-bottom:1px solid #030;line-height:1.4;" onclick="selectAddress('${place.display_name.replace(/'/g, "\\'").replace(/"/g, '&quot;')}', ${place.lat}, ${place.lon})">${display}</div>`;
                }).join('');
                el.style.display = 'block';
            } else {
                el.innerHTML = '<div style="padding:10px;color:#FF6666;">No results found — try adding city and state</div>';
                el.style.display = 'block';
            }
        } catch (err) {
            if (gen === acGeneration) {
                console.error('Autocomplete error:', err);
                el.style.display = 'none';
            }
        }
    }, 350);
}

function selectAddress(addr, lat, lon) {
    const shortAddr = formatShortAddress(addr);
    document.getElementById('addressInput').value = shortAddr;
    document.getElementById('addressSuggestions').style.display = 'none';
    loadPropertyReachData(shortAddr);
}

function formatShortAddress(fullAddress) {
    // Full OSM format: "925, South 3rd Street, Chickasha, Grady County, Oklahoma, 73018, United States"
    // We want: "925 S 3rd St, Chickasha, OK"
    const parts = fullAddress.split(',').map(p => p.trim());
    
    // Find state by looking for state names
    const stateNames = ['Alabama','Alaska','Arizona','Arkansas','California','Colorado','Connecticut','Delaware','Florida','Georgia','Hawaii','Idaho','Illinois','Indiana','Iowa','Kansas','Kentucky','Louisiana','Maine','Maryland','Massachusetts','Michigan','Minnesota','Mississippi','Missouri','Montana','Nebraska','Nevada','New Hampshire','New Jersey','New Mexico','New York','North Carolina','North Dakota','Ohio','Oklahoma','Oregon','Pennsylvania','Rhode Island','South Carolina','South Dakota','Tennessee','Texas','Utah','Vermont','Virginia','Washington','West Virginia','Wisconsin','Wyoming'];
    
    let state = '';
    let stateIdx = -1;
    for (let i = 1; i < parts.length; i++) {
        if (stateNames.includes(parts[i])) {
            state = parts[i];
            stateIdx = i;
            break;
        }
    }
    
    // City is the part before state (or before county if present)
    let city = '';
    if (stateIdx > 1) {
        city = parts[stateIdx - 1];
        // If it's "County", go back one more
        if (city.toLowerCase().includes('county') && stateIdx > 2) {
            city = parts[stateIdx - 2];
        }
    }
    
    // Street: parts[0] + parts[1] (number + street name)
    let street = parts[0] || '';
    if (parts[1] && !parts[1].toLowerCase().includes('county')) {
        street = parts[0] + ' ' + parts[1];
    }
    
    return `${street}, ${city}, ${state.substring(0, 2)}`;
}

// ============================================
// PROPERTY DATA LOADER
// ============================================

async function loadPropertyReachData(address) {
    const PROXY_URL = 'https://srv1336418.hstgr.cloud/?url=';
    const API_KEY = 'live_u9JyD3Hmp58wmEQEnyZ5GosDjDcXHH5SuUN';
    
    try {
        // Normalize street address (South -> S, Street -> St, etc)
        function normalizeStreet(addr) {
            return addr
                .replace(/\bSouth\b/g, 'S')
                .replace(/\bNorth\b/g, 'N')
                .replace(/\bEast\b/g, 'E')
                .replace(/\bWest\b/g, 'W')
                .replace(/\bStreet\b/g, 'St')
                .replace(/\bAvenue\b/g, 'Ave')
                .replace(/\bRoad\b/g, 'Rd')
                .replace(/\bDrive\b/g, 'Dr')
                .replace(/\bLane\b/g, 'Ln')
                .replace(/\bCourt\b/g, 'Ct')
                .replace(/\bPlace\b/g, 'Pl')
                .replace(/\bBoulevard\b/g, 'Blvd')
                .replace(/\bCircle\b/g, 'Cir')
                .replace(/\bTerrace\b/g, 'Ter');
        }
        
        // Parse address - handle both comma and space separated
        let streetAddress, city, state;
        
        if (address.includes(',')) {
            // Comma separated format: "street, city, state"
            const parts = address.split(",").map(s => s.trim());
            streetAddress = parts[0] || '';
            city = parts[1] || '';
            state = parts[2]?.split(' ')[0] || '';
            if (parts.length > 3) {
                city = parts[2] || '';
                state = parts[3] || '';
            }
        } else {
            // Space separated - need to find state abbreviation at end
            const parts = address.trim().split(' ');
            // Last 2 parts should be city, state (e.g., "Chickasha OK")
            // Or last 3 (e.g., "Chickasha Oklahoma")
            state = parts[parts.length - 1] || '';
            if (state.length > 2) {
                // Full state name, get abbreviation
                const stateMap = {
                    'Alabama':'AL','Alaska':'AK','Arizona':'AZ','Arkansas':'AR','California':'CA',
                    'Colorado':'CO','Connecticut':'CT','Delaware':'DE','Florida':'FL','Georgia':'GA',
                    'Hawaii':'HI','Idaho':'ID','Illinois':'IL','Indiana':'IN','Iowa':'IA',
                    'Kansas':'KS','Kentucky':'KY','Louisiana':'LA','Maine':'ME','Maryland':'MD',
                    'Massachusetts':'MA','Michigan':'MI','Minnesota':'MN','Mississippi':'MS','Missouri':'MO',
                    'Montana':'MT','Nebraska':'NE','Nevada':'NV','NewHampshire':'NH','NewJersey':'NJ',
                    'NewMexico':'NM','NewYork':'NY','NorthCarolina':'NC','NorthDakota':'ND','Ohio':'OH',
                    'Oklahoma':'OK','Oregon':'OR','Pennsylvania':'PA','RhodeIsland':'RI','SouthCarolina':'SC',
                    'SouthDakota':'SD','Tennessee':'TN','Texas':'TX','Utah':'UT','Vermont':'VT',
                    'Virginia':'VA','Washington':'WA','WestVirginia':'WV','Wisconsin':'WI','Wyoming':'WY'
                };
                state = stateMap[state] || state.substring(0, 2).toUpperCase();
            }
            city = parts[parts.length - 2] || '';
            // Street is everything before city
            streetAddress = parts.slice(0, parts.length - 2).join(' ');
        }
        
        
        // Normalize street address
        streetAddress = normalizeStreet(streetAddress);
        
        // Call PropertyReach - search by city/state first, then filter for matching street
        const url = PROXY_URL + encodeURIComponent('https://api.propertyreach.com/v1/search');
        const body = {
            target: { city, state: state?.toUpperCase() },
            filter: { streetAddress: streetAddress.split(' ')[0] },  // Filter by street number
            limit: 50
        };
        
        const resp = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'x-api-key': API_KEY
            },
            body: JSON.stringify(body)
        });
        
        if (!resp.ok) throw new Error('API error: ' + resp.status);
        
        const data = await resp.json();
        console.log('DEBUG: Parsed address:', streetAddress, city, state);
        console.log('DEBUG: streetAddress=' + streetAddress + ', city=' + city + ', state=' + state);
        console.log('PropertyReach response:', data);
        
        if (!data.properties || data.properties.length === 0) {
            throw new Error('No property found');
        }
        
        // Find the property that matches our street address
        let prop = null;
        const streetNum = (streetAddress.split(' ')[0] || '').toLowerCase();
        const streetName = (streetAddress.split(' ').slice(1).join(' ') || '').toLowerCase().replace(/\s+/g, '');
        
        console.log('Looking for streetNum:', streetNum, 'streetName:', streetName);
        
        for (let p of data.properties) {
            const pStreet = (p.streetAddress || '').toLowerCase();
            const pStreetNum = pStreet.split(' ')[0] || '';
            const pStreetName = pStreet.split(' ').slice(1).join(' ').replace(/\s+/g, '');
            
            // Match street number and street name
            if (pStreetNum === streetNum && pStreetName.includes(streetName)) {
                console.log('Found match:', p.streetAddress, p.city, p.estimatedValue, 'rent:', p.estimatedRentAmount, 'tax:', p.taxAmount);
                // Fetch full property details to get rent and tax
                const propUrl = PROXY_URL + encodeURIComponent('https://api.propertyreach.com/v1/property?streetAddress=' + encodeURIComponent(p.streetAddress) + '&city=' + encodeURIComponent(city) + '&state=' + encodeURIComponent(state));
                try {
                    const propResp = await fetch(propUrl);
                    if (propResp.ok) {
                        const propData = await propResp.json();
                        if (propData.property) {
                            console.log('Full property rent:', propData.property.estimatedRentAmount, 'tax:', propData.property.taxAmount);
                            p = propData.property;
                        }
                    }
                } catch(e) { console.log('Error:', e); }
                prop = p;
                break;
            }
        }
        
        // If no match, use first result
        if (!prop && data.properties.length > 0) {
            prop = data.properties[0];
            console.log('No exact match, using:', prop.streetAddress);
        }
        
        // Populate fields
        const _el = document.getElementById('arvInput'); if(_el) _el.value = prop.estimatedValue || '';

        // Set rent — use PropertyReach if available, else leave blank for manual entry
        document.getElementById('rentEstimate').value = prop.estimatedRentAmount || '';
        // rentEstimateDetail removed from DOM
        document.getElementById('sqft').value = prop.squareFeet || prop.livingSquareFeet || '';
        document.getElementById('yearBuilt').value = prop.yearBuilt || '';
        // Try to find bedrooms/bathrooms fields
        const bedsEl = document.getElementById('bedrooms');
        if (bedsEl) bedsEl.value = prop.bedrooms || '';
        const bathsEl = document.getElementById('bathrooms');
        if (bathsEl) bathsEl.value = prop.bathrooms || '';
        document.getElementById('monthlyTaxes').value = prop.taxAmount ? Math.round(prop.taxAmount/12) : '';
        document.getElementById('annualInsurance').value = Math.round((prop.squareFeet || 1500) * 0.50);
        document.getElementById('lastSalePrice').value = prop.lastSaleAmount || '';
        document.getElementById('lastSaleDate').value = prop.lastSaleDate || '';
        
    } catch(e) {
        console.error(e);
        alert('Error loading property data: ' + e.message);
    }
}
