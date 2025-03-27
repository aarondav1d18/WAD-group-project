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

  document.querySelector(".start-btn").addEventListener("click", () => {
    window.location.href = `/Quizzical/quiz/`;
  });

  // Grab the .save-btn in the popup
  const oldSaveButton = document.querySelector(".save-btn");
  // Clone it to remove old event listeners (if the popup opens multiple times)
  const newSaveButton = oldSaveButton.cloneNode(true);
  oldSaveButton.parentNode.replaceChild(newSaveButton, oldSaveButton);

  // Decide what happens when the user clicks .save-btn
  if (authenticated) {
    // If the user is logged in
    newSaveButton.textContent = "Save Quiz";
    newSaveButton.addEventListener("click", () => {
      // Call a function that saves this quiz, e.g. via AJAX
      saveQuiz(quiz.id);
    });
  } else {
    // If the user is NOT logged in
    newSaveButton.textContent = "Log In to Save Quiz";
    newSaveButton.addEventListener("click", () => {
      // Redirect user to login page
      window.location.href = "/Quizzical/login/";
    });
  }

  // Finally, show the popup
  popup.classList.add("show");
}

function saveQuiz(quizId) {
  fetch('/Quizzical/save-quiz/', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json',
      },
      body: JSON.stringify({ quiz_id: quizId })
  })
  .then(response => response.json())
  .then(data => {
      document.getElementById("quiz-popup").classList.remove("show");
      if (data.success) {
          alert("Quiz saved!");
      } else {
          alert("Failed to save quiz: " + data.message);
      }
  })
  .catch(error => {
      console.error('Error saving quiz:', error);
  });
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
