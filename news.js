<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>StockWizard - News</title>
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark">
        <div class="container-fluid">
            <a class="navbar-brand" href="cssss.html">
                <img src="images/std.png" alt="StockWizard Logo" width="40" height="40" class="d-inline-block align-text-top">
                StockWizard
            </a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav me-auto">
                    <li class="nav-item">
                        <a class="nav-link" href="cssss.html">Home</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link active" aria-current="page" href="#">News</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="portfolio.html">Portfolio</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="#" onclick="showLoginForm()">Sign In</a>
                    </li>
                </ul>
                <div class="form-check form-switch text-white">
                    <input class="form-check-input" type="checkbox" id="themeSwitch" onclick="toggleTheme()">
                    <label class="form-check-label" for="themeSwitch">Dark Mode</label>
                </div>
            </div>
        </div>
    </nav>

    <header class="text-white text-center py-3">
        <h1>StockWizard News</h1>
        <p>Get the latest news and updates in the stock market</p>
    </header>

    <div class="container mt-4">
        <div class="input-group mb-3">
            <input type="text" class="form-control" placeholder="Search news..." id="search-input">
            <button class="btn btn-primary" type="button" onclick="searchNews()">Search</button>
        </div>
        <div class="card">
            <div class="card-header bg-primary text-white">
                Latest Market News
            </div>
            <div class="card-body" id="news-container">
                <!-- News articles will be injected here by JavaScript -->
            </div>
        </div>
    </div>

    <footer class="bg-primary text-white text-center py-3 mt-4">
        <p>&copy; 2024 StockWizard. All rights reserved.</p>
    </footer>

    <!-- Bootstrap JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/js/bootstrap.bundle.min.js"></script>
    <script src="news.js"></script>
    <script>
        function showLoginForm() {
            document.getElementById('loginForm').style.display = 'block';
        }

        function hideLoginForm() {
            document.getElementById('loginForm').style.display = 'none';
        }

        function toggleTheme() {
            document.body.classList.toggle('dark-theme');
        }
    </script>
</body>
</html>
