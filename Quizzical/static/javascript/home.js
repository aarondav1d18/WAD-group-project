// Open popup function with smooth animation
function openPopup(quiz) {
  const popup = document.getElementById("quiz-popup");
  document.getElementById("quiz-title").innerText = quiz.title;
  document.getElementById("quiz-image").src = quiz.image;
  popup.classList.add("show");

  // START BUTTON logic
  {
    const oldStartBtn = document.querySelector(".start-btn");
    const newStartBtn = oldStartBtn.cloneNode(true);
    oldStartBtn.parentNode.replaceChild(newStartBtn, oldStartBtn);

    newStartBtn.textContent = "Start Quiz";
    newStartBtn.addEventListener("click", () => {
      window.location.href = `/Quizzical/quiz/`;
    });
  }

  // SAVE BUTTON logic
  {
    const oldSaveBtn = document.querySelector(".save-btn");
    const newSaveBtn = oldSaveBtn.cloneNode(true);
    oldSaveBtn.parentNode.replaceChild(newSaveBtn, oldSaveBtn);

    if (authenticated) {
      newSaveBtn.textContent = "Save Quiz";
      newSaveBtn.addEventListener("click", () => {
        saveQuiz(quiz.id);
      });
    } else {
      newSaveBtn.textContent = "Log In to Save Quiz";
      newSaveBtn.addEventListener("click", () => {
        window.location.href = "/Quizzical/login/";
      });
    }
  }

  // If the user is authenticated, render the rating widget.
  if (authenticated) {
    renderUserRating(quiz);
  }
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


function saveQuiz(quizId) {
    console.log("Saving quiz with ID:", quizId);
    // TODO: implement an actual save, e.g. via fetch() or AJAX to your Django endpoint
}

// Close popup function with animation
document.querySelector(".close-btn").addEventListener("click", () => {
    const popup = document.getElementById("quiz-popup");
    popup.classList.remove("show"); // Hide with animation
});

// Generate star ratings dynamically
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

// Load quizzes dynamically from Django context
function loadQuizzes(category, containerId) {
    const container = document.getElementById(containerId);
    if (!container || !quizzes[category]) return;

    quizzes[category].forEach(quiz => {
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

// Load quizzes from Django data when the page loads
document.addEventListener("DOMContentLoaded", () => {
    loadQuizzes("educational", "educational-quizzes");
    loadQuizzes("fun", "fun-quizzes");
});
