function load_initial(){
    document.getElementById('quiz-title').textContent = quiz.name;

    const nextButton = document.getElementById('next-btn');
    nextButton.addEventListener("click", function (){
        displayQuestion(quiz.answers[question_number]);
        this.disabled = true;
    })
    nextButton.disabled = true

    displayQuestion(quiz.answers[question_number])
}

function displayQuestion(answers){
    if (quiz.questions[question_number]){
        document.getElementById('question-text').textContent = quiz.questions[question_number];
        document.querySelectorAll(".answer-option").forEach(button => {
            button.disabled = false;
        })

        const answersContainer = document.getElementById('button-container');
        answersContainer.innerHTML = "";

        answers = shuffle(answers);

        answers.forEach((answer, index) => {
            const answerButton = document.createElement("button");
            answerButton.textContent = answer[0];
            answerButton.classList.add("answer-option");
            answerButton.dataset.correct = answer[1];
            answerButton.addEventListener("click", checkAnswer);
            answersContainer.appendChild(answerButton);
        });
        question_number += 1;
    }
    else {
        endQuiz();
    }
}

function checkAnswer(event) {
    const isCorrect = event.target.dataset.correct === "true";
    let selected = event.target;
    if (isCorrect) {
        selected.style.background = "green";
        correct_answers += 1;
    } else {
        selected.style.background = "red";
    }
    document.getElementById('next-btn').disabled = false;
    document.querySelectorAll(".answer-option").forEach(button => {
        button.disabled = true;
    })
    //displayQuestion(quiz.answers[question_number])
}

function endQuiz(){
    document.getElementById('button-container').innerHTML = "";
    document.getElementById('question-text').textContent = "";
    alert(correct_answers + " Answered Correctly");

    const againButton = document.createElement("button");
    againButton.textContent = "Try Again";
    againButton.classList.add("again");
    againButton.addEventListener("click", function(){
        location.reload();
    })
    document.getElementById('button-container').appendChild(againButton);
}

function shuffle(array) {
    return array.sort(() => Math.random() - 0.5);
}

document.addEventListener("DOMContentLoaded", function(){
    load_initial();
})