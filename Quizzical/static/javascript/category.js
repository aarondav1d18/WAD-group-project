// Wait for the DOM to load before executing scripts
document.addEventListener("DOMContentLoaded", () => {
  document.getElementById("search-input").addEventListener("input", renderQuizzes);
  document.getElementById("category-filter").addEventListener("change", renderQuizzes);
  document.getElementById("sort-filter").addEventListener("change", renderQuizzes);

  // Close popup event
  document.querySelector(".close-btn").addEventListener("click", () => {
    document.getElementById("quiz-popup").classList.remove("show");
  });

  populateCategoryFilter();
  renderQuizzes();
});

// Attach event listener to the start button inside the popup (if not already attached)
// document.querySelectorAll('.start-btn').forEach(button => {
//   button.addEventListener('click', function(event) {
//       const quizId = this.getAttribute('data-quiz-id');
//       window.location.href = `/quiz/${quizId}/`; 
//   });
// });

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
  document.getElementById("quiz-image").src = staticImagePath + quiz.image;
  // Set the quiz id on the start button for redirection
  document.querySelector(".start-btn").setAttribute("data-quiz-id", quiz.id);
  popup.classList.add("show");
}

// Render quizzes based on search, category, and sort filters
function renderQuizzes() {
  const container = document.getElementById("quiz-container");
  container.innerHTML = "";

  const searchValue = document.getElementById("search-input").value.toLowerCase();
  const selectedCategory = document.getElementById("category-filter").value;
  const sortBy = document.getElementById("sort-filter").value;

  const heading = document.getElementById("quizzes-heading");
  heading.textContent = selectedCategory === "all" ? "All Quizzes" : `${selectedCategory} Quizzes`;

  let filteredQuizzes = quizzes.filter(quiz => {
    const matchesSearch = quiz.title.toLowerCase().includes(searchValue);
    const matchesCategory = selectedCategory === "all" ||
      (quiz.category && quiz.category.toLowerCase() === selectedCategory.toLowerCase());
    return matchesSearch && matchesCategory;
  });

  if (sortBy === "top") {
    filteredQuizzes.sort((a, b) => b.rating - a.rating);
  } else if (sortBy === "newest") {
    filteredQuizzes.sort((a, b) => new Date(b.creation_date) - new Date(a.creation_date));
  }

  filteredQuizzes.forEach(quiz => {
    let quizCard = document.createElement("div");
    quizCard.classList.add("quiz-card");
    console.log(staticImagePath + quiz.image)
    quizCard.innerHTML = `
      <img src="${staticImagePath}${quiz.image}" alt="${quiz.title}" style="width: 100%; height: auto; border-radius: 5px;">
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
  categorySet.forEach(category => {
    const option = document.createElement("option");
    option.value = category;
    option.textContent = category;
    categoryFilter.appendChild(option);
  });
}
