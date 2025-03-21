// Open popup function with smooth animation
function openPopup(quiz) {
    const popup = document.getElementById("quiz-popup");
    document.getElementById("quiz-title").innerText = quiz.title;
    document.getElementById("quiz-image").src = staticImagePath + quiz.image;
    popup.classList.add("show"); // Show with animation
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
