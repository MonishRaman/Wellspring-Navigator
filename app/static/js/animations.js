document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("diagnosis-form");
    const questions = document.querySelectorAll(".question");
    const nextBtn = document.querySelector(".next-btn");
    const submitBtn = document.querySelector(".submit-btn");
    const progressBar = document.querySelector(".progress");
    let currentStep = 0;

    // Show the first question
    questions[currentStep].classList.add("active");

    // Handle "Next" button click
    nextBtn.addEventListener("click", () => {
        const inputs = questions[currentStep].querySelectorAll("input");
        const answered = Array.from(inputs).some(input => input.checked);

        if (!answered) {
            alert("Please select an option before proceeding.");
            return;
        }

        // Hide current question and show the next one
        questions[currentStep].classList.remove("active");
        currentStep++;

        if (currentStep < questions.length) {
            questions[currentStep].classList.add("active");
            progressBar.style.width = `${(currentStep / questions.length) * 100}%`;
        }

        // If it's the last question, show the submit button
        if (currentStep === questions.length - 1) {
            nextBtn.style.display = "none";
            submitBtn.style.display = "block";
        }
    });

    // Alert on form submission
    form.addEventListener("submit", () => {
        alert("Submitting your responses... Stay positive! 😊");
    });
});