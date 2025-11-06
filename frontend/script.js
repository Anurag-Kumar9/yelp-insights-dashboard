document.addEventListener('DOMContentLoaded', () => {
    const searchBtn = document.getElementById('search-button');
    const predictBtn = document.getElementById('predict-button');
    const spinner = document.getElementById('spinner');
    const resultsContainer = document.getElementById('results-container');
    const restaurantInput = document.getElementById('restaurant-id-input');
    const reviewInput = document.getElementById('review-text-input');

    // Human-readable cluster names for K-Means clusters
    const clusterNames = {
        0: "Low-Activity Harsh Rater",
        1: "Active Balanced Reviewer",
        2: "Elite Power User",
        3: "Super Elite Critic",
        4: "Happy Casual"
    };

    // Utility functions
    function showSpinner() {
        spinner.style.display = 'flex';
    }

    function hideSpinner() {
        spinner.style.display = 'none';
    }

    function showResults() {
        resultsContainer.style.display = 'block';
        // Smooth scroll to results
        setTimeout(() => {
            resultsContainer.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }, 100);
    }

    function hideResults() {
        resultsContainer.style.display = 'none';
    }

    function showError(message) {
        // Create a custom styled alert
        const errorDiv = document.createElement('div');
        errorDiv.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: linear-gradient(135deg, rgba(239, 68, 68, 0.95), rgba(220, 38, 38, 0.95));
            color: white;
            padding: 1rem 1.5rem;
            border-radius: 12px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            z-index: 1000;
            max-width: 400px;
            animation: slideIn 0.3s ease;
        `;
        errorDiv.innerHTML = `
            <div style="display: flex; align-items: center; gap: 0.75rem;">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" style="flex-shrink: 0;">
                    <circle cx="12" cy="12" r="10" stroke="white" stroke-width="2"/>
                    <path d="M12 8v4M12 16h.01" stroke="white" stroke-width="2" stroke-linecap="round"/>
                </svg>
                <div>
                    <strong style="display: block; margin-bottom: 0.25rem;">Error</strong>
                    <span style="font-size: 0.9rem;">${message}</span>
                </div>
            </div>
        `;
        document.body.appendChild(errorDiv);
        setTimeout(() => {
            errorDiv.style.animation = 'slideOut 0.3s ease';
            setTimeout(() => errorDiv.remove(), 300);
        }, 4000);
    }

    function animateValue(element, start, end, duration) {
        const range = end - start;
        const increment = range / (duration / 16);
        let current = start;

        const timer = setInterval(() => {
            current += increment;
            if ((increment > 0 && current >= end) || (increment < 0 && current <= end)) {
                current = end;
                clearInterval(timer);
            }
            element.textContent = (current * 100).toFixed(1) + '%';
        }, 16);
    }

    // Add Enter key support for search
    restaurantInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            searchBtn.click();
        }
    });

    // Search button handler
    searchBtn.addEventListener('click', async () => {
        const restaurantId = restaurantInput.value.trim();

        if (!restaurantId) {
            showError('Please enter a Restaurant Business ID');
            restaurantInput.focus();
            return;
        }

        showSpinner();
        hideResults();

        try {
            const res = await fetch(`/restaurant/${restaurantId}`);

            if (!res.ok) {
                const errorText = await res.text();
                throw new Error(errorText || 'Restaurant not found');
            }

            const data = await res.json();

            // Update restaurant name
            document.getElementById('restaurant-name').textContent =
                data.restaurant_name || 'Unknown Restaurant';

            // Animate positivity score
            const positivityElement = document.getElementById('positivity-score');
            const positivityBar = document.getElementById('positivity-bar');

            if (typeof data.positivity_score === 'number') {
                animateValue(positivityElement, 0, data.positivity_score, 1000);
                setTimeout(() => {
                    positivityBar.style.width = (data.positivity_score * 100) + '%';
                }, 200);
            } else {
                positivityElement.textContent = 'N/A';
                positivityBar.style.width = '0%';
            }

            // Populate positive keywords with animation
            const positiveList = document.getElementById('positive-keywords-list');
            positiveList.innerHTML = '';
            (data.positive_keywords || []).forEach((word, index) => {
                const li = document.createElement('li');
                li.textContent = word;
                li.style.opacity = '0';
                li.style.transform = 'translateX(-20px)';
                positiveList.appendChild(li);

                setTimeout(() => {
                    li.style.transition = 'all 0.3s ease';
                    li.style.opacity = '1';
                    li.style.transform = 'translateX(0)';
                }, index * 50);
            });

            // Populate negative keywords with animation
            const negativeList = document.getElementById('negative-keywords-list');
            negativeList.innerHTML = '';
            (data.negative_keywords || []).forEach((word, index) => {
                const li = document.createElement('li');
                li.textContent = word;
                li.style.opacity = '0';
                li.style.transform = 'translateX(-20px)';
                negativeList.appendChild(li);

                setTimeout(() => {
                    li.style.transition = 'all 0.3s ease';
                    li.style.opacity = '1';
                    li.style.transform = 'translateX(0)';
                }, index * 50);
            });

            // Populate clusters table with animation
            const tbody = document.querySelector('#cluster-table tbody');
            tbody.innerHTML = '';

            (data.customer_archetypes || []).forEach((row, index) => {
                const tr = document.createElement('tr');
                tr.style.opacity = '0';
                tr.style.transform = 'translateY(10px)';

                const tdType = document.createElement('td');
                const label = row.type;
                tdType.textContent = clusterNames.hasOwnProperty(label)
                    ? clusterNames[label]
                    : `Cluster ${label}`;

                const tdCount = document.createElement('td');
                tdCount.textContent = row.count;
                tdCount.style.fontWeight = '600';

                tr.appendChild(tdType);
                tr.appendChild(tdCount);
                tbody.appendChild(tr);

                setTimeout(() => {
                    tr.style.transition = 'all 0.3s ease';
                    tr.style.opacity = '1';
                    tr.style.transform = 'translateY(0)';
                }, index * 50);
            });

            hideSpinner();
            showResults();

        } catch (err) {
            hideSpinner();
            showError(err.message || 'Failed to fetch restaurant data');
        }
    });

    // Predict button handler
    predictBtn.addEventListener('click', async () => {
        const reviewText = reviewInput.value.trim();

        if (!reviewText) {
            showError('Please enter review text to predict rating');
            reviewInput.focus();
            return;
        }

        // Show loading state on button
        const originalContent = predictBtn.innerHTML;
        predictBtn.disabled = true;
        predictBtn.innerHTML = `
            <div style="width: 18px; height: 18px; border: 2px solid currentColor; border-top-color: transparent; border-radius: 50%; animation: spin 1s linear infinite;"></div>
            <span>Predicting...</span>
        `;

        const predictionResult = document.getElementById('prediction-result');
        predictionResult.textContent = '';

        try {
            const res = await fetch('/predict_star', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ text: reviewText })
            });

            if (!res.ok) {
                const errorText = await res.text();
                throw new Error(errorText || 'Prediction failed');
            }

            const data = await res.json();

            // Display result with animation
            const stars = '⭐'.repeat(Math.round(data.predicted_star));
            const confidence = Math.round(data.confidence * 100);

            predictionResult.style.opacity = '0';
            predictionResult.innerHTML = `
                <div style="display: flex; flex-direction: column; gap: 0.5rem; align-items: center;">
                    <div style="font-size: 2rem;">${stars}</div>
                    <div style="font-size: 1.25rem; font-weight: 700;">
                        ${data.predicted_star} Stars
                    </div>
                    <div style="font-size: 0.9rem; opacity: 0.8;">
                        Confidence: ${confidence}%
                    </div>
                </div>
            `;

            setTimeout(() => {
                predictionResult.style.transition = 'opacity 0.3s ease';
                predictionResult.style.opacity = '1';
            }, 100);

        } catch (err) {
            showError(err.message || 'Failed to predict rating');
        } finally {
            predictBtn.disabled = false;
            predictBtn.innerHTML = originalContent;
        }
    });

    // Add CSS animations dynamically
    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideIn {
            from {
                transform: translateX(400px);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
            }
        }
        
        @keyframes slideOut {
            from {
                transform: translateX(0);
                opacity: 1;
            }
            to {
                transform: translateX(400px);
                opacity: 0;
            }
        }
    `;
    document.head.appendChild(style);
});
