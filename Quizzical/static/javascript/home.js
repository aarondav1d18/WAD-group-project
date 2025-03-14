// Just visualising the quizzes to adjust the layout
const educationalQuizzes = [
    { title: "Math Quiz", image: "/static/images/img1.jpg", rating: 1.5 },
    { title: "History Quiz", image: "/static/images/img2.jpg", rating: 2.5 },
    { title: "Science Quiz", image: "/static/images/img3.jpg", rating: 3.5 },
    { title: "Compsci Quiz", image: "/static/images/img1.jpg", rating: 4.5 },
    { title: "Buissness Quiz", image: "/static/images/img2.jpg", rating: 5 },
    { title: "English Quiz", image: "/static/images/img3.jpg", rating: 1 },
    { title: "test Quiz", image: "/static/images/img1.jpg" , rating: 2},
    { title: "tes1 Quiz", image: "/static/images/img2.jpg", rating: 3 },
    { title: "test2 Quiz", image: "/static/images/img3.jpg", rating: 4 },
    { title: "test3 Quiz", image: "/static/images/img1.jpg", rating: 5 },
    { title: "tes12 Quiz", image: "/static/images/img2.jpg", rating: 6 },
    { title: "test22 Quiz", image: "/static/images/img3.jpg", rating: 2.5 }
];

const funQuizzes = [
    { title: "Movie Trivia", image: "/static/images/img4.jpg", rating: 1.5 },
    { title: "Music Quiz", image: "/static/images/img5.jpg", rating: 1.5 },
    { title: "Sports Quiz", image: "/static/images/img6.jpg", rating: 1.5 }
];

function generateStars(rating) {
    let stars = "";
    for (let i = 0; i < 5; i++) {
        if (i < Math.floor(rating)) {
            stars += `<span class="star full"></span>`; // Full star
        } else if (i < rating) {
            stars += `<span class="star half"></span>`; // Half star
        } else {
            stars += `<span class="star"></span>`; // Empty star
        }
    }
    return stars;
}

function loadQuizzes(category, containerId) {
    const container = document.getElementById(containerId);
    if (!container) {
        console.error(`Container with ID '${containerId}' not found.`);
        return;
    }

    category.forEach(quiz => {
        let quizCard = document.createElement("div");
        quizCard.classList.add("quiz-card");

        quizCard.innerHTML = `
            <img src="${quiz.image}" alt="${quiz.title}" style="width: 100%; height: auto; border-radius: 5px;">
            <p>${quiz.title}</p>
            <div class="star-rating">${generateStars(quiz.rating)}</div>
        `;

        container.appendChild(quizCard);
    });
}

document.addEventListener("DOMContentLoaded", () => {
    loadQuizzes(educationalQuizzes, "educational-quizzes");
    loadQuizzes(funQuizzes, "fun-quizzes");
});
