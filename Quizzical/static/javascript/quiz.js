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
    if (correct_answers === 1){
        document.getElementById('question-text').textContent = "You Got " + correct_answers + " Answer Correct!";
    }
    else {
        document.getElementById('question-text').textContent = "You Got " + correct_answers + " Answers Correct!";
    }


    const againButton = document.createElement("button");
    againButton.textContent = "Try Again";
    againButton.classList.add("again");
    againButton.addEventListener("click", function(){
        location.reload();
    })

    const saveButton = document.createElement("button");
    if (authenticated){
        const isSaved = quiz.saved_by_user;

        if (isSaved) {
            saveButton.textContent = "Unsave Quiz";
        }
        else {
            saveButton.textContent = "Save Quiz";
        }

        saveButton.addEventListener("click", () => {
            toggleSaveQuiz(quiz.quizID, (updatedStatus) => {
                quiz.saved_by_user = updatedStatus === "saved";
                saveButton.textContent = quiz.saved_by_user ? "Unsave Quiz" : "Save Quiz";
            });
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

document.addEventListener("DOMContentLoaded", function(){
    load_initial();
})