// Get modal elements
const openFormButton = document.getElementById('open-login-form');
const modal = document.getElementById('login-modal');
const closeModalButton = document.querySelector('.close');

// Show the modal when the login/register button is clicked
openFormButton.addEventListener('click', (e) => {
  e.preventDefault();
  modal.style.display = 'flex';
});

// Hide the modal when the close button is clicked
closeModalButton.addEventListener('click', () => {
  modal.style.display = 'none';
});

// Hide the modal when clicking outside the modal content
window.addEventListener('click', (e) => {
  if (e.target === modal) {
    modal.style.display = 'none';
  }
});

const apiKey = 'your_actual_api_key'; // Replace with your actual API key
const newsContainer = document.getElementById('news-container');

fetch(`https://newsapi.org/v2/top-headlines?category=business&apiKey=${apiKey}`)
  .then(response => response.json())
  .then(data => {
    data.articles.forEach(article => {
      const newsItem = document.createElement('div');
      newsItem.className = 'mb-3';
      newsItem.innerHTML = `
        <a href="${article.url}" class="text-decoration-none" target="_blank">
          <h5 class="card-title">${article.title}</h5>
          <p class="card-text">${article.description}</p>
        </a>
      `;
      newsContainer.appendChild(newsItem);
    });
  })
  .catch(error => console.error('Error fetching news:', error));

document.addEventListener('DOMContentLoaded', () => {
    const apiKey = 'your_actual_api_key'; // Replace with your actual API key
    const tickerElement = document.querySelector('.ticker');

    async function fetchStockData() {
        try {
            const response = await fetch(`https://finnhub.io/api/v1/quote?symbol=AAPL&token=${apiKey}`);
            const data = await response.json();

            tickerElement.innerHTML = ''; // Clear previous ticker items

            const stockSymbols = ['AAPL', 'GOOG', 'MSFT', 'AMZN', 'TSLA', 'META', 'NFLX', 'NVDA', 
                                  'AMD', 'INTC', 'ADBE', 'ORCL', 'PYPL', 'CSCO', 'IBM', 'QCOM', 
                                  'BABA', 'V', 'MA', 'DIS', 'WMT', 'JPM', 'BAC', 'PEP'];

            const requests = stockSymbols.map(symbol => fetch(`https://finnhub.io/api/v1/quote?symbol=${symbol}&token=${apiKey}`));
            const responses = await Promise.all(requests);

            responses.forEach(async (response, index) => {
                const data = await response.json();
                const { c: currentPrice, d: change, dp: percentChange } = data;
                const symbol = stockSymbols[index];

                const stockItem = document.createElement('span');
                stockItem.className = change >= 0 ? 'stock-movement-up' : 'stock-movement-down';
                stockItem.innerHTML = `${symbol}: $${currentPrice.toFixed(2)} ${change >= 0 ? '▲' : '▼'} ${percentChange.toFixed(2)}% | `;
                tickerElement.appendChild(stockItem);
            });
        } catch (error) {
            console.error('Error fetching stock data:', error);
            tickerElement.textContent = 'Error fetching stock data.';
        }
    }

    fetchStockData();
    setInterval(fetchStockData, 60000); // Update every 60 seconds
});



