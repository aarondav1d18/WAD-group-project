// Wait for the DOM to load before executing scripts
document.addEventListener("DOMContentLoaded", () => {
    // Attach event listeners for search and filter inputs
    document.getElementById("search-input").addEventListener("input", renderQuizzes);
    document.getElementById("category-filter").addEventListener("change", renderQuizzes);
    document.getElementById("sort-filter").addEventListener("change", renderQuizzes);
  
    // Close popup event
    document.querySelector(".close-btn").addEventListener("click", () => {
      document.getElementById("quiz-popup").classList.remove("show");
    });
  
    // Populate category filter options based on available quiz categories
    populateCategoryFilter();
  
    // Initial render of quizzes
    renderQuizzes();
  });
  
  // Function to generate star rating HTML
  function generateStars(rating) {
    let stars = "";
    for (let i = 0; i < 5; i++) {
      if (i < Math.floor(rating)) {
        stars += `<span class="star full">★</span>`;
      } else if (i < rating) {
        stars += `<span class="star half">★</span>`;
      } else {
        stars += `<span class="star">☆</span>`;
      }
    }
    return stars;
  }
  
  // Function to open the quiz popup modal
  function openPopup(quiz) {
    const popup = document.getElementById("quiz-popup");
    document.getElementById("quiz-title").innerText = quiz.title;
    document.getElementById("quiz-image").src = quiz.image;
    popup.classList.add("show");
  }
  
  // Render quizzes based on search, category, and sort filters
  function renderQuizzes() {
    const container = document.getElementById("quiz-container");
    container.innerHTML = "";
  
    const searchValue = document.getElementById("search-input").value.toLowerCase();
    const selectedCategory = document.getElementById("category-filter").value;
    const sortBy = document.getElementById("sort-filter").value;
  
    // Update the heading based on the selected category
    const heading = document.getElementById("quizzes-heading");
    if (selectedCategory === "all") {
      heading.textContent = "All Quizzes";
    } else {
      heading.textContent = `${selectedCategory} Quizzes`;
    }
  
    // Filter and sort as before
    let filteredQuizzes = quizzes.filter(quiz => {
      const matchesSearch = quiz.title.toLowerCase().includes(searchValue);
      const matchesCategory =
        selectedCategory === "all" ||
        (quiz.category && quiz.category.toLowerCase() === selectedCategory.toLowerCase());
      return matchesSearch && matchesCategory;
    });
  
    // Sort by rating or date
    if (sortBy === "top") {
      filteredQuizzes.sort((a, b) => b.rating - a.rating);
    } else if (sortBy === "newest") {
      filteredQuizzes.sort((a, b) => new Date(b.creation_date) - new Date(a.creation_date));
    }
  
    // Create quiz cards
    filteredQuizzes.forEach(quiz => {
      let quizCard = document.createElement("div");
      quizCard.classList.add("quiz-card");
      quizCard.innerHTML = `
        <img src="${quiz.image}" alt="${quiz.title}" style="width: 100%; height: auto; border-radius: 5px;">
        <p style="color: white; font-weight: bold;">${quiz.title}</p>
        <div class="star-rating">${generateStars(quiz.rating)}</div>
      `;
      quizCard.addEventListener("click", () => openPopup(quiz));
      container.appendChild(quizCard);
    });
  }
  
  
  // Populate the category filter dropdown with unique categories from the quiz list
  function populateCategoryFilter() {
    const categorySet = new Set();
    quizzes.forEach(quiz => {
      if (quiz.category) {
        categorySet.add(quiz.category);
      }
    });
  
    const categoryFilter = document.getElementById("category-filter");
    // Add an option for each unique category
    categorySet.forEach(category => {
      const option = document.createElement("option");
      option.value = category;
      option.textContent = category;
      categoryFilter.appendChild(option);
    });
  }
  