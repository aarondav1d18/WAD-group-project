let question_number = 0;
let correct_answers = 0;

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
    document.getElementById('question-text').textContent = "You Got " + correct_answers + " Answers Correct!";

    const againButton = document.createElement("button");
    againButton.textContent = "Try Again";
    againButton.classList.add("again");
    againButton.addEventListener("click", function(){
        location.reload();
    })

    const saveButton = document.createElement("button");
    if (authenticated){
        saveButton.textContent = "Save Quiz";
        saveButton.addEventListener("click", () => {
            saveQuiz(quiz.id);
        })
    }
    else {
        saveButton.textContent = "Log In to Save Quiz";
        saveButton.addEventListener("click", () => {
            window.location.href = "/Quizzical/login/";
        })
    }
    saveButton.classList.add("again");
    document.getElementById('button-container').appendChild(againButton);
    document.getElementById('button-container').appendChild(saveButton);
}

function shuffle(array) {
    return array.sort(() => Math.random() - 0.5);
}

function saveQuiz(quizId) {
    console.log("Saving quiz with ID:", quizId);
    // TODO: implement an actual save, e.g. via fetch() or AJAX to your Django endpoint
}

document.addEventListener("DOMContentLoaded", function(){
    load_initial();
})