// Helper: Format numbers with commas
function formatCurrency(val) {
    const value = Math.round(val);
    const prefix = value >= 0 ? '+' : '';
    return prefix + '$' + value.toLocaleString('en-US');
}

// Adjust Counter Values (Bedrooms / Bathrooms)
function adjustValue(inputId, increment) {
    const input = document.getElementById(inputId);
    const min = parseFloat(input.getAttribute('min'));
    const max = parseFloat(input.getAttribute('max'));
    let currentValue = parseFloat(input.value);
    
    let newValue = currentValue + increment;
    if (newValue >= min && newValue <= max) {
        // Handle float vs int formatting
        if (inputId === 'bathrooms') {
            input.value = newValue.toFixed(1);
        } else {
            input.value = Math.round(newValue);
        }
    }
}

// Global Tab State and Variables
let activeTab = 'valuation';
let modelMetadata = null;
let chartInstance = null;

// Tab Switcher Lógica (Exposta Globalmente)
function switchTab(tabId) {
    const emptyState = document.getElementById('empty-state');
    const valuationContent = document.getElementById('tab-valuation');
    const priceVal = document.getElementById('price-val');
    
    // Update active tab button
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
        if (btn.getAttribute('onclick').includes(tabId)) {
            btn.classList.add('active');
        }
    });

    // Hide all tab content
    document.querySelectorAll('.tab-content').forEach(content => {
        content.style.display = 'none';
    });

    activeTab = tabId;

    if (tabId === 'valuation') {
        const rawPriceText = priceVal.textContent.replace(/,/g, '');
        const currentPriceVal = parseFloat(rawPriceText);
        if (!currentPriceVal || currentPriceVal === 0) {
            emptyState.style.display = 'flex';
        } else {
            emptyState.style.display = 'block';
            valuationContent.style.display = 'block';
        }
    } else {
        emptyState.style.display = 'none';
        const targetTab = document.getElementById('tab-' + tabId);
        if (targetTab) {
            targetTab.style.display = 'block';
        }
    }
}
window.switchTab = switchTab;

// Dynamic range slider display updates and setup
document.addEventListener('DOMContentLoaded', () => {
    const sqftSlider = document.getElementById('sqft_living');
    const sqftVal = document.getElementById('sqft-val');
    sqftSlider.addEventListener('input', (e) => {
        sqftVal.textContent = parseInt(e.target.value).toLocaleString('en-US');
    });

    const ageSlider = document.getElementById('age_years');
    const ageVal = document.getElementById('age-val');
    ageSlider.addEventListener('input', (e) => {
        ageVal.textContent = e.target.value;
    });

    const distSlider = document.getElementById('distance_to_center_km');
    const distVal = document.getElementById('dist-val');
    distSlider.addEventListener('input', (e) => {
        distVal.textContent = parseFloat(e.target.value).toFixed(1);
    });

    // Form Submission
    const form = document.getElementById('predictor-form');
    const btnPredict = document.getElementById('btn-predict');
    const btnLoader = btnPredict.querySelector('.btn-loader');
    const emptyState = document.getElementById('empty-state');
    const valuationContent = document.getElementById('tab-valuation');
    const priceVal = document.getElementById('price-val');
    
    // Breakdown DOM references
    const bdSize = document.getElementById('bd-size');
    const bdRooms = document.getElementById('bd-rooms');
    const bdAge = document.getElementById('bd-age');
    const bdDist = document.getElementById('bd-dist');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        // UI Loading State
        btnPredict.disabled = true;
        btnLoader.style.display = 'inline-block';
        btnPredict.querySelector('span').textContent = 'Estimating...';

        // Gather Inputs
        const payload = {
            sqft_living: parseInt(sqftSlider.value),
            bedrooms: parseInt(document.getElementById('bedrooms').value),
            bathrooms: parseFloat(document.getElementById('bathrooms').value),
            age_years: parseInt(ageSlider.value),
            distance_to_center_km: parseFloat(distSlider.value)
        };

        try {
            const response = await fetch('/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(payload)
            });

            if (!response.ok) {
                const errData = await response.json();
                throw new Error(errData.error || 'Server error occurred.');
            }

            const data = await response.json();

            // Handle showing correct valuation tab structure
            if (activeTab === 'valuation') {
                emptyState.style.display = 'none';
                valuationContent.style.display = 'block';
            }

            // Animate Price Valuation Count-Up
            const startPrice = 0;
            const endPrice = data.price;
            animatePrice(priceVal, startPrice, endPrice, 800);

            // Populate Breakdown Values
            bdSize.textContent = formatCurrency(data.breakdown.size_contribution);
            bdRooms.textContent = formatCurrency(data.breakdown.rooms_contribution);
            bdAge.textContent = formatCurrency(data.breakdown.age_depreciation);
            bdDist.textContent = formatCurrency(data.breakdown.location_effect);

            // Fix styling classes according to values
            toggleContributionClass(bdSize, data.breakdown.size_contribution);
            toggleContributionClass(bdRooms, data.breakdown.rooms_contribution);
            toggleContributionClass(bdAge, data.breakdown.age_depreciation);
            toggleContributionClass(bdDist, data.breakdown.location_effect);

        } catch (error) {
            console.error(error);
            alert('Valuation Failed: ' + error.message);
        } finally {
            // Restore UI State
            btnPredict.disabled = false;
            btnLoader.style.display = 'none';
            btnPredict.querySelector('span').textContent = 'Estimate Value';
        }
    });

    // Load Model metadata on initial load
    loadModelInfo();
});

// Helper: Toggle positive/negative CSS classes for styling
function toggleContributionClass(element, value) {
    if (value >= 0) {
        element.classList.remove('negative');
        element.classList.add('positive');
    } else {
        element.classList.remove('positive');
        element.classList.add('negative');
    }
}

// Animate Price Text counting up
function animatePrice(obj, start, end, duration) {
    const range = end - start;
    let current = start;
    const steps = 30;
    const increment = range / steps;
    const stepTime = Math.abs(Math.floor(duration / steps));
    let stepCount = 0;

    const timer = setInterval(() => {
        current += increment;
        stepCount++;
        
        if (stepCount >= steps) {
            current = end;
            clearInterval(timer);
        }
        
        obj.textContent = Math.round(current).toLocaleString('en-US');
    }, stepTime);
}

// Fetch model metadata and populate tables/charts
async function loadModelInfo() {
    try {
        const response = await fetch('/model_info');
        if (!response.ok) throw new Error('Failed to load model metadata.');
        modelMetadata = await response.json();
        
        populateMetricsTable(modelMetadata.metrics);
        renderImportanceChart(modelMetadata.feature_importances);
        generateInsightText(modelMetadata.feature_importances);
    } catch (err) {
        console.error('Error loading model metadata:', err);
        document.getElementById('insight-text').textContent = 'Could not load model explainability insights. Make sure model_metadata.json is generated.';
    }
}

// Populate model metrics comparison table
function populateMetricsTable(metrics) {
    const lr = metrics['Linear Regression'];
    const rf = metrics['Random Forest'];
    
    document.getElementById('m-lr-r2').textContent = lr.R2.toFixed(4);
    document.getElementById('m-rf-r2').textContent = rf.R2.toFixed(4);
    
    document.getElementById('m-lr-cvr2').textContent = lr.CV_R2_Mean.toFixed(4);
    document.getElementById('m-rf-cvr2').textContent = rf.CV_R2_Mean.toFixed(4);
    
    document.getElementById('m-lr-mae').textContent = '$' + Math.round(lr.MAE).toLocaleString();
    document.getElementById('m-rf-mae').textContent = '$' + Math.round(rf.MAE).toLocaleString();
    
    document.getElementById('m-lr-rmse').textContent = '$' + Math.round(lr.RMSE).toLocaleString();
    document.getElementById('m-rf-rmse').textContent = '$' + Math.round(rf.RMSE).toLocaleString();
    
    document.getElementById('m-lr-mape').textContent = lr.MAPE.toFixed(2) + '%';
    document.getElementById('m-rf-mape').textContent = rf.MAPE.toFixed(2) + '%';
}

// Render dynamic Chart.js Feature Importances Chart
function renderImportanceChart(importances) {
    const ctx = document.getElementById('importance-chart').getContext('2d');
    
    // Feature translations for labels
    const labelMap = {
        'sqft_living': 'Living Area (sqft)',
        'distance_to_center_km': 'Distance to Center (km)',
        'bedrooms': 'Bedrooms',
        'bathrooms': 'Bathrooms',
        'age_years': 'Property Age'
    };

    // Sort features by importance
    const sortedFeatures = Object.entries(importances).sort((a, b) => b[1] - a[1]);
    const labels = sortedFeatures.map(item => labelMap[item[0]] || item[0]);
    const data = sortedFeatures.map(item => item[1]);

    if (chartInstance) {
        chartInstance.destroy();
    }

    chartInstance = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                data: data,
                backgroundColor: 'rgba(0, 242, 254, 0.25)',
                borderColor: '#00f2fe',
                borderWidth: 1.5,
                borderRadius: 8,
                hoverBackgroundColor: 'rgba(0, 242, 254, 0.45)'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return `Importance: ${(context.raw * 100).toFixed(1)}%`;
                        }
                    }
                }
            },
            scales: {
                x: {
                    grid: { display: false },
                    ticks: { color: '#9ca3af', font: { family: 'Outfit', size: 11 } }
                },
                y: {
                    grid: { color: 'rgba(255, 255, 255, 0.05)' },
                    ticks: { 
                        color: '#9ca3af', 
                        font: { family: 'Outfit', size: 10 },
                        callback: function(value) {
                            return (value * 100).toFixed(0) + '%';
                        }
                    }
                }
            }
        }
    });
}

// Generate model explainability insights text
function generateInsightText(importances) {
    let topFeature = '';
    let topVal = 0;
    for (const [key, val] of Object.entries(importances)) {
        if (val > topVal) {
            topVal = val;
            topFeature = key;
        }
    }
    
    const featureNamesEN = {
        'sqft_living': 'Living Area (sqft_living)',
        'distance_to_center_km': 'Distance to Center (distance_to_center_km)',
        'bedrooms': 'Number of Bedrooms (bedrooms)',
        'bathrooms': 'Number of Bathrooms (bathrooms)',
        'age_years': 'Property Age (age_years)'
    };
    
    const topName = featureNamesEN[topFeature] || topFeature;
    document.getElementById('insight-text').innerHTML = `The most influential feature in the price prediction model is <strong>${topName}</strong>, driving <strong>${(topVal * 100).toFixed(1)}%</strong> of the model's decisions. Living space and location factors combined account for over 75% of the Random Forest's pricing formula.`;
}
