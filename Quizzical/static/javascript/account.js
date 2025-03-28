function renderQuizzes(quizzes) {
  const container = document.getElementById("quiz-container");
  container.innerHTML = "";

  quizzes.forEach(quiz => {
    let quizCard = document.createElement("div");
    quizCard.classList.add("quiz-card");
    quizCard.innerHTML = `
      <img src="${quiz.image}" alt="${quiz.title}" style="width: 100%; height: auto; border-radius: 5px;">
      <p style="color: white; font-weight: bold;">${quiz.title}</p>
      <div class="star-rating">${generateStars(quiz.rating)}</div>
    `;
    quizCard.addEventListener("click", () => window.location.href=`/Quizzical/quiz/${quiz.name}/`);
    container.appendChild(quizCard);
  });
}

function renderUserInfo(){
    const container = document.getElementById("quiz-container");
    container.innerHTML = "";

    container.innerHTML = `
        <div id="user_info">
        <p class="user-info-text">Username: ${quizzes.userInfo.username}</p>
        <p class="user-info-text">Email: ${quizzes.userInfo.email}</p>
        </div>
    `;
}

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

document.addEventListener("DOMContentLoaded", () => {
    renderUserInfo();
    document.getElementById("user-info").addEventListener("click", renderUserInfo);
    document.getElementById("fav").addEventListener("click", () => {renderQuizzes(quizzes.saved)});
    document.getElementById("created").addEventListener("click", () => {renderQuizzes(quizzes.myQuizzes)});
})