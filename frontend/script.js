
const API_BASE_URL = 'http://localhost:8000';

const chatForm = document.getElementById('chat-form');
const messageInput = document.getElementById('message-input');
const chatContainer = document.getElementById('chat-container');

let lastBotResponse = null; // Store the last response for feedback

async function submitQuery(question) {
  const params = new URLSearchParams();
  params.append('question', question);

  const response = await fetch(`${API_BASE_URL}/query`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: params,
  });

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }
  return response.json();
}

async function submitFeedback(feedbackData) {
  const response = await fetch(`${API_BASE_URL}/feedback`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(feedbackData),
  });

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }
  return response.json();
}

chatForm.addEventListener('submit', async (event) => {
  event.preventDefault();
  const userMessage = messageInput.value.trim();
  if (!userMessage) return;

  appendMessage(userMessage, 'user');
  messageInput.value = '';
  
  // Show typing indicator
  const typingIndicator = appendMessage('Печатает...', 'bot');

  try {
    const data = await submitQuery(userMessage);
    lastBotResponse = data; // Save for feedback
    
    // Remove typing indicator and show final message
    chatContainer.removeChild(typingIndicator);
    appendMessage(data.answer, 'bot', data.sources);

  } catch (error) {
    console.error('Ошибка:', error);
    chatContainer.removeChild(typingIndicator);
    appendMessage('Произошла ошибка. Пожалуйста, попробуйте позже.', 'error');
  }
});

function appendMessage(text, sender, sources = []) {
  const messageElement = document.createElement('div');
  messageElement.classList.add('message', `${sender}-message`);
  
  const textElement = document.createElement('p');
  textElement.innerText = text;
  messageElement.appendChild(textElement);

  if (sources.length > 0) {
    const sourcesContainer = document.createElement('div');
    sourcesContainer.classList.add('sources');
    sourcesContainer.innerHTML = '<strong>Источники:</strong>';
    sources.forEach(source => {
        const sourceEl = document.createElement('p');
        sourceEl.innerText = `- ${source.name}`;
        sourcesContainer.appendChild(sourceEl);
    });
    messageElement.appendChild(sourcesContainer);
  }
  
  // Add feedback buttons for bot messages
  if (sender === 'bot') {
      const feedbackContainer = document.createElement('div');
      feedbackContainer.classList.add('feedback');
      
      const likeButton = document.createElement('button');
      likeButton.innerText = '👍';
      likeButton.onclick = () => handleFeedback(5);
      
      const dislikeButton = document.createElement('button');
      dislikeButton.innerText = '👎';
      dislikeButton.onclick = () => handleFeedback(1);
      
      feedbackContainer.appendChild(likeButton);
      feedbackContainer.appendChild(dislikeButton);
      messageElement.appendChild(feedbackContainer);
  }

  chatContainer.appendChild(messageElement);
  chatContainer.scrollTop = chatContainer.scrollHeight;
  return messageElement;
}

function handleFeedback(rating) {
    if (!lastBotResponse) return;

    console.log(`Feedback received: ${rating}`);
    
    const feedbackData = {
        id: lastBotResponse.sources.length > 0 ? lastBotResponse.sources[0].id + Date.now() : Date.now().toString(),
        user_id: 'anonymous',
        question: lastBotResponse.question || 'Unknown',
        answer: lastBotResponse.answer,
        rating: rating,
        comment: rating === 5 ? 'Good answer' : 'Bad answer',
        retrieved_docs: lastBotResponse.sources
    };

    submitFeedback(feedbackData)
        .then(() => {
            console.log('Feedback submitted successfully');
            alert('Спасибо за ваш отзыв!');
        })
        .catch(error => {
            console.error('Failed to submit feedback:', error);
            alert('Не удалось отправить отзыв.');
        });
}
