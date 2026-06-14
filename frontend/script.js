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

// Dynamic range slider display updates
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
    const resultsContent = document.getElementById('results-content');
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

            // Hide Empty State and Show Results
            emptyState.style.display = 'none';
            resultsContent.style.display = 'block';

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
