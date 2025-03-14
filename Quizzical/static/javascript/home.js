// Just visualising the quizzes to adjust the layout
const educationalQuizzes = [
    { title: "Math Quiz", image: "/static/images/img1.jpg" },
    { title: "History Quiz", image: "/static/images/img2.jpg" },
    { title: "Science Quiz", image: "/static/images/img3.jpg" },
    { title: "Compsci Quiz", image: "/static/images/img1.jpg" },
    { title: "Buissness Quiz", image: "/static/images/img2.jpg" },
    { title: "English Quiz", image: "/static/images/img3.jpg" },
    { title: "test Quiz", image: "/static/images/img1.jpg" },
    { title: "tes1 Quiz", image: "/static/images/img2.jpg" },
    { title: "test2 Quiz", image: "/static/images/img3.jpg" }
];

const funQuizzes = [
    { title: "Movie Trivia", image: "/static/images/img4.jpg" },
    { title: "Music Quiz", image: "/static/images/img5.jpg" },
    { title: "Sports Quiz", image: "/static/images/img6.jpg" }
];

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
        `;
        container.appendChild(quizCard);
    });
}

document.addEventListener("DOMContentLoaded", () => {
    loadQuizzes(educationalQuizzes, "educational-quizzes");
    loadQuizzes(funQuizzes, "fun-quizzes");
});
