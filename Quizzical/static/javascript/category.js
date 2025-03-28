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
  document.getElementById("quiz-image").src = quiz.image;

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
    const isSaved = quiz.saved_by_user;
  
    newSaveButton.textContent = isSaved ? "Unsave Quiz" : "Save Quiz";
  
    newSaveButton.addEventListener("click", () => {
      toggleSaveQuiz(quiz.id, (updatedStatus) => {
        quiz.saved_by_user = updatedStatus === "saved";
        newSaveButton.textContent = quiz.saved_by_user ? "Unsave Quiz" : "Save Quiz";
      });
    });
    renderUserRating(quiz);
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


// Generate the rating widget for the user to rate the quiz.
function renderUserRating(quiz) {
  const ratingContainer = document.getElementById("quiz-user-rating");
  // If the user has already rated, use that value; otherwise, start at 0.
  const currentRating = quiz.user_rating || 0;
  let ratingHTML = "<p>Rate this quiz:</p>";

  // Create 5 stars; each star is clickable.
  for (let i = 1; i <= 5; i++) {
    if (i <= currentRating) {
      ratingHTML += `<span class="star clickable full" data-value="${i}">★</span>`;
    } else {
      ratingHTML += `<span class="star clickable" data-value="${i}">☆</span>`;
    }
  }
  ratingContainer.innerHTML = ratingHTML;

  // Add click listeners to stars.
  const stars = ratingContainer.querySelectorAll(".star.clickable");
  stars.forEach(star => {
    star.addEventListener("click", function () {
      const ratingValue = parseInt(this.getAttribute("data-value"));
      submitRating(quiz.id, ratingValue);
      // Optionally update the widget immediately
      renderUserRating({ ...quiz, user_rating: ratingValue });
    });
  });
}

// Submit the rating to the server
function submitRating(quizId, ratingValue) {
  fetch("/Quizzical/rate_quiz/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      quiz_id: quizId,
      rating: parseInt(ratingValue),
    })
  })
  .then(response => response.json())
  .then(data => {
    if (data.success) {
      alert("Rating saved!");
      window.location.reload(); // Refresh the page
    } else {
      alert("Failed to save rating: " + data.error);
    }
  })
  .catch(error => console.error("Error:", error));
}

// Simple example of a saveQuiz function
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

function toggleSaveQuiz(quizId, callback) {
  fetch('/Quizzical/save-quiz/', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json',
      },
      body: JSON.stringify({ quiz_id: quizId })
  })
  .then(response => response.json())
  .then(data => {
      if (data.success) {
          callback(data.action); // "saved" or "unsaved"
      } else {
          alert("Error: " + data.message);
      }
  })
  .catch(error => {
      console.error('Error toggling quiz save:', error);
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
  categorySet.forEach(category => {
    const option = document.createElement("option");
    option.value = category;
    option.textContent = category;
    categoryFilter.appendChild(option);
  });
}
