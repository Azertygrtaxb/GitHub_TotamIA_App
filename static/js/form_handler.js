const questions = ['location', 'activity', 'difficulty', 'distance', 'landscape', 'email'];
let currentQuestion = 0;

function showQuestion(index) {
    questions.forEach((q, i) => {
        const element = document.getElementById(q);
        element.classList.toggle('hidden', i !== index);
    });

    // Show/hide navigation buttons
    const submitBtn = document.getElementById('submit-btn');
    const nextBtn = document.getElementById('next-btn');

    // On the last question (email), show only Previous and Submit buttons
    if (index === questions.length - 1) {
        submitBtn.classList.remove('hidden');
        nextBtn.classList.add('hidden');
    } else {
        submitBtn.classList.add('hidden');
        nextBtn.classList.remove('hidden');
    }
}

function startQuestionnaire() {
    document.getElementById('welcome-screen').classList.add('hidden');
    document.getElementById('trail-form').classList.remove('hidden');
    currentQuestion = 0;
    showQuestion(currentQuestion);
}

function nextQuestion() {
    const currentElement = document.getElementById(questions[currentQuestion]);
    const input = currentElement.querySelector('select, input');

    if (!input.value) {
        alert('Veuillez répondre à la question avant de continuer.');
        return;
    }

    if (currentQuestion < questions.length - 1) {
        currentQuestion++;
        showQuestion(currentQuestion);
    }
}

function previousQuestion() {
    if (currentQuestion > 0) {
        currentQuestion--;
        showQuestion(currentQuestion);
    }
}

// Form submission handler
document.getElementById('trail-form').addEventListener('submit', function(e) {
    e.preventDefault();

    // Validate all fields before submission
    let isValid = true;
    questions.forEach(q => {
        const input = document.getElementById(q).querySelector('select, input');
        if (!input.value) {
            isValid = false;
        }
    });

    if (!isValid) {
        alert('Veuillez remplir tous les champs avant d\'envoyer.');
        return;
    }

    const submitBtn = document.getElementById('submit-btn');
    submitBtn.disabled = true;
    submitBtn.textContent = 'Envoi en cours...';

    const formData = new FormData(this);
    fetch('/submit', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        submitBtn.disabled = false;
        submitBtn.textContent = 'Envoyer';

        if (data.success) {
            window.location.href = '/success';
        } else if (data.redirect) {
            window.location.href = data.redirect;
        } else {
            alert(data.error || 'Une erreur est survenue. Veuillez réessayer.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        submitBtn.disabled = false;
        submitBtn.textContent = 'Envoyer';
        alert('Une erreur est survenue. Veuillez réessayer.');
    });
});