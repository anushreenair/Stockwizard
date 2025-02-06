const apiKey = '4e500e83c0cc47988318c670f04214cd'; // Replace with your NewsAPI key

document.addEventListener('DOMContentLoaded', () => {
    fetchNews();
});

function fetchNews(query = 'stock market') {
    const url = `https://newsapi.org/v2/everything?q=${query}&apiKey=${apiKey}`;

    fetch(url)
        .then(response => response.json())
        .then(data => {
            const newsContainer = document.getElementById('news-container');
            newsContainer.innerHTML = '';

            data.articles.forEach(article => {
                const newsCard = document.createElement('div');
                newsCard.className = 'card mb-3';
                newsCard.innerHTML = `
                    <div class="row g-0">
                        <div class="col-md-4">
                            <img src="${article.urlToImage}" class="img-fluid rounded-start" alt="${article.title}">
                        </div>
                        <div class="col-md-8">
                            <div class="card-body">
                                <h5 class="card-title">${article.title}</h5>
                                <p class="card-text">${article.description}</p>
                                <p class="card-text"><small class="text-muted">Published on ${new Date(article.publishedAt).toLocaleDateString()}</small></p>
                                <a href="${article.url}" target="_blank" class="btn btn-primary">Read more</a>
                            </div>
                        </div>
                    </div>
                `;
                newsContainer.appendChild(newsCard);
            });
        })
        .catch(error => console.error('Error fetching news:', error));
}

function searchNews() {
    const query = document.getElementById('search-input').value;
    fetchNews(query);
}
