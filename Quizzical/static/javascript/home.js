// These are placeholders to test the animations and visuals will change for database integration
const educationalQuizzes = [
    { title: "Math Quiz", image: "/static/images/img1.jpg", rating: 1.5 },
    { title: "History Quiz", image: "/static/images/img2.jpg", rating: 2.5 },
    { title: "Science Quiz", image: "/static/images/img3.jpg", rating: 3.5 },
    { title: "Compsci Quiz", image: "/static/images/img1.jpg", rating: 4.5 },
    { title: "Business Quiz", image: "/static/images/img2.jpg", rating: 5 },
    { title: "English Quiz", image: "/static/images/img3.jpg", rating: 1 }
];

const funQuizzes = [
    { title: "Movie Trivia", image: "/static/images/img4.jpg", rating: 1.5 },
    { title: "Music Quiz", image: "/static/images/img5.jpg", rating: 2.5 },
    { title: "Sports Quiz", image: "/static/images/img6.jpg", rating: 3.5 }
];

// Open popup function with smooth animation
function openPopup(quiz) {
    const popup = document.getElementById("quiz-popup");
    document.getElementById("quiz-title").innerText = quiz.title;
    document.getElementById("quiz-image").src = quiz.image;

    popup.classList.add("show"); // Add class for animation
}

// Close popup function with smooth animation
document.querySelector(".close-btn").addEventListener("click", () => {
    const popup = document.getElementById("quiz-popup");
    popup.classList.remove("show"); // Remove class to trigger fade-out
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

// Load quizzes into their respective sections
function loadQuizzes(category, containerId) {
    const container = document.getElementById(containerId);
    if (!container) return;

    category.forEach(quiz => {
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

// Load quizzes on page load
document.addEventListener("DOMContentLoaded", () => {
    loadQuizzes(educationalQuizzes, "educational-quizzes");
    loadQuizzes(funQuizzes, "fun-quizzes");
});