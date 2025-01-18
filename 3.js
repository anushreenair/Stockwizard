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

const apiKey = '4e500e83c0cc47988318c670f04214cd';
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
