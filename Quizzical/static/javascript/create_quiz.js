window.onload = function() {
    let nextNewSlideIndex = 1;

    document.getElementById("create-new-slide").addEventListener("click", function() {
        const slidesList = document.getElementById("slides-list");

        const newSlide = document.createElement("li");
        newSlide.id = `slide_${nextNewSlideIndex}`;
        slidesList.appendChild(newSlide);
        newSlide.innerHTML = `
        <h3>Question ${nextNewSlideIndex + 1}</h3>

        <div class="form-entry">
            <label for="question">Question:</label>
            <input type="text" name="question_${nextNewSlideIndex}" placeholder="Enter a question" />
        </div>

        <div class="form-entry">
            <label for="image-upload">Upload an Image:</label>
            <input type="file" name="image_${nextNewSlideIndex}" accept="image/*">
        </div>

        <div class="form-entry">
            <label for="answer1">Answer 1:</label>
            <input type="text" name="answer1_${nextNewSlideIndex}" placeholder="Enter the first answer" />
            <input type="checkbox" name="is-answer1_${nextNewSlideIndex}" value="yes">
        </div>

        <div class="form-entry">
            <label for="answer2">Answer 2:</label>
            <input type="text" name="answer2_${nextNewSlideIndex}" placeholder="Enter the second answer" />
            <input type="checkbox" name="is-answer2_${nextNewSlideIndex}" value="no">
        </div>

        <div class="form-entry">
            <label for="answer3">Answer 3:</label>
            <input type="text" name="answer3_${nextNewSlideIndex}" placeholder="Enter the third answer" />
            <input type="checkbox" name="is-answer3_${nextNewSlideIndex}" value="no">
        </div>

        <div class="form-entry">
            <label for="answer4">Answer 4:</label>
            <input type="text" name="answer4_${nextNewSlideIndex}" placeholder="Enter the fourth answer" />
            <input type="checkbox" name="is-answer4_${nextNewSlideIndex}" value="no">
        </div>

        <button type="button" class="remove-slide">Remove Slide</button>`;

        nextNewSlideIndex++;

        document.getElementById("slides-list").addEventListener("click", function(event) {
            if (event.target && event.target.classList.contains("remove-slide")) {
                const removedSlide = event.target.closest("li");
                removedSlide.remove();

                // Ensure nextNewSlideIndex never goes negative
                nextNewSlideIndex = Math.max(1, nextNewSlideIndex - 1);

                // Re-index remaining slides
                const slides = document.querySelectorAll("#slides-list li");
                slides.forEach((slide, newIndex) => {
                    slide.id = `slide_${newIndex}`;

                    // Update question title
                    const title = slide.querySelector("h3");
                    if (title) title.innerText = `Question ${newIndex + 1}`;

                    // Update all form elements inside slide
                    slide.querySelectorAll("input, label, textarea, select").forEach((element) => {
                        if (element.name) {
                            element.name = element.name.replace(/\d+$/, newIndex);
                        }
                        if (element.id) {
                            element.id = element.id.replace(/\d+$/, newIndex);
                        }
                        if (element.htmlFor) {
                            element.htmlFor = element.htmlFor.replace(/\d+$/, newIndex);
                        }
                    });
                });
            }
        });
    });
}