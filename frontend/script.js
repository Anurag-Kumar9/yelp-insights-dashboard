document.addEventListener('DOMContentLoaded', () => {
    const searchBtn = document.getElementById('search-button');
    const predictBtn = document.getElementById('predict-button');
    const spinner = document.getElementById('spinner');
    const resultsContainer = document.getElementById('results-container');
    
    function showSpinner() {
        spinner.style.display = 'flex';
    }
    function hideSpinner() {
        spinner.style.display = 'none';
    }

    searchBtn.addEventListener('click', async () => {
        const restaurantId = document.getElementById('restaurant-id-input').value.trim();
        if (!restaurantId) {
            alert('Please enter a Restaurant ID.');
            return;
        }
        showSpinner();
        resultsContainer.style.display = 'none';

        try {
            const res = await fetch(`/restaurant/${restaurantId}`);
            if (!res.ok) {
                throw new Error(await res.text() || res.statusText);
            }
            const data = await res.json();

            document.getElementById('restaurant-name').textContent = data.restaurant_name || '';
            document.getElementById('positivity-score').textContent = data.positivity_score != null ? data.positivity_score : '';

            // Populate positive keywords
            const positiveList = document.getElementById('positive-keywords-list');
            positiveList.innerHTML = '';
            (data.positive_keywords || []).forEach(word => {
                const li = document.createElement('li');
                li.textContent = word;
                positiveList.appendChild(li);
            });
            // Populate negative keywords
            const negativeList = document.getElementById('negative-keywords-list');
            negativeList.innerHTML = '';
            (data.negative_keywords || []).forEach(word => {
                const li = document.createElement('li');
                li.textContent = word;
                negativeList.appendChild(li);
            });
            // Populate clusters table
            const tbody = document.querySelector('#cluster-table tbody');
            tbody.innerHTML = '';
            (data.customer_archetypes || []).forEach(row => {
                const tr = document.createElement('tr');
                const tdType = document.createElement('td');
                tdType.textContent = row.type;
                const tdCount = document.createElement('td');
                tdCount.textContent = row.count;
                tr.appendChild(tdType);
                tr.appendChild(tdCount);
                tbody.appendChild(tr);
            });

            hideSpinner();
            resultsContainer.style.display = 'flex';
        } catch (err) {
            hideSpinner();
            alert('Error: ' + err.message);
        }
    });

    predictBtn.addEventListener('click', async () => {
        const reviewText = document.getElementById('review-text-input').value.trim();
        if (!reviewText) {
            alert('Please enter review text.');
            return;
        }
        showSpinner();
        document.getElementById('prediction-result').textContent = '';
        try {
            const res = await fetch('/predict_star', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ text: reviewText })
            });
            if (!res.ok) {
                throw new Error(await res.text() || res.statusText);
            }
            const data = await res.json();
            document.getElementById('prediction-result').textContent =
                `Predicted Stars: ${data.predicted_star} (Confidence: ${Math.round(data.confidence * 100)}%)`;
            hideSpinner();
        } catch (err) {
            hideSpinner();
            alert('Error: ' + err.message);
        }
    });
});
