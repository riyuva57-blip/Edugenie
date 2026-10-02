const form = document.getElementById('edu-form');
const task = document.getElementById('task');
const text = document.getElementById('input-text');
const options = document.getElementById('options');
const level = document.getElementById('level');
const weeks = document.getElementById('weeks');
const result = document.getElementById('result');
const status = document.getElementById('status');
const submit = document.getElementById('submit-btn');
const counter = document.getElementById('counter');

function updateUI() {
  options.classList.toggle('hidden', task.value !== 'learn');
  const placeholders = {
    qa: 'e.g. Which is the largest ocean?',
    explain: 'e.g. Explain the Pythagorean theorem for a beginner.',
    quiz: 'Paste a topic or passage for a 3-question quiz.',
    summarize: 'Paste an educational passage to summarize.',
    learn: 'e.g. SQL'
  };
  text.placeholder = placeholders[task.value];
}

task.addEventListener('change', updateUI);
text.addEventListener('input', () => { counter.textContent = `${text.value.length.toLocaleString()} / 30,000`; });
updateUI();

function escapeHtml(value) {
  return String(value).replace(/[&<>'"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[c]));
}

function renderQuiz(questions) {
  result.innerHTML = `<h2>Quiz</h2>` + questions.map((q, i) => `
    <article class="quiz-item">
      <strong>${i + 1}. ${escapeHtml(q.question)}</strong>
      ${q.options.map((opt, j) => `<label class="quiz-option"><input type="radio" name="q${i}" value="${escapeHtml(opt)}"> ${escapeHtml(opt)}</label>`).join('')}
      <button type="button" class="check-answer" data-index="${i}">Check answer</button>
      <div class="answer" id="answer-${i}"></div>
    </article>`).join('');

  result.querySelectorAll('.check-answer').forEach(button => {
    button.addEventListener('click', () => {
      const i = Number(button.dataset.index);
      const selected = result.querySelector(`input[name="q${i}"]:checked`);
      const answerBox = document.getElementById(`answer-${i}`);
      if (!selected) { answerBox.textContent = 'Choose an option first.'; return; }
      const q = questions[i];
      const correct = selected.value === q.correct_answer;
      answerBox.textContent = correct ? 'Correct!' : `Not quite. Correct answer: ${q.correct_answer}${q.explanation ? ` — ${q.explanation}` : ''}`;
    });
  });
}

form.addEventListener('submit', async (event) => {
  event.preventDefault();
  const value = text.value.trim();
  if (!value) { status.textContent = 'Enter some text first.'; return; }

  const endpoint = task.value === 'learn' ? '/learn/recommendations' : `/${task.value}`;
  const body = task.value === 'learn' ? { text: value, level: level.value, weeks: Number(weeks.value) } : { text: value };

  submit.disabled = true;
  status.textContent = 'Thinking…';
  result.classList.add('hidden');
  result.innerHTML = '';

  try {
    const response = await fetch(endpoint, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) });
    const data = await response.json();
    if (!response.ok) throw new Error(data.detail || 'Request failed.');
    if (task.value === 'quiz') renderQuiz(data.questions);
    else result.textContent = data.result;
    result.classList.remove('hidden');
    status.textContent = 'Done.';
  } catch (error) {
    status.textContent = `Error: ${error.message}`;
  } finally {
    submit.disabled = false;
  }
});