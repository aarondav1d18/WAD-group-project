// Open popup function with smooth animation
function openPopup(quiz) {
  const popup = document.getElementById("quiz-popup");
  document.getElementById("quiz-title").innerText = quiz.title;
  document.getElementById("quiz-image").src = staticImagePath + quiz.image;
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
      const isSaved = quiz.saved_by_user;
    
      newSaveButton.textContent = isSaved ? "Unsave Quiz" : "Save Quiz";
    
      newSaveButton.addEventListener("click", () => {
        toggleSaveQuiz(quiz.id, (updatedStatus) => {
          quiz.saved_by_user = updatedStatus === "saved";
          newSaveButton.textContent = quiz.saved_by_user ? "Unsave Quiz" : "Save Quiz";
          document.getElementById("quiz-popup").classList.remove("show");
        });
      });
    } else {
      // If the user is NOT logged in
      newSaveButton.textContent = "Log In to Save Quiz";
      newSaveButton.addEventListener("click", () => {
        // Redirect user to login page
        window.location.href = "/Quizzical/login/";
      });
    }
  }
}

function saveQuiz(quizId) {
  fetch('save-quiz/', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json',
      },
      body: JSON.stringify({ quiz_id: quizId })
  })
  .then(response => response.json())
  .then(data => {
      if (data.success) {
        document.getElementById("quiz-popup").classList.remove("show");
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
            <img src="${staticImagePath}${quiz.image}" alt="${quiz.title}" style="width: 100%; height: auto; border-radius: 5px;">
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
