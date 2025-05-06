document.getElementById('send-button').addEventListener('click', async () => {
    const userInput = document.getElementById('user-input').value.trim();
    if (!userInput) return;

    appendMessage(userInput, 'user');

    try {
        const response = await fetch('http://127.0.0.1:5000/ask', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ question: userInput })
        });

        if (!response.ok) {
            const errorData = await response.json();
            appendMessage('Error: ' + (errorData.error || 'Unknown error'), 'bot');
            return;
        }

        const data = await response.json();
        appendMessage(data.answer, 'bot');

    } catch (error) {
        appendMessage('Network or URL error: ' + error.message, 'bot');
        console.error('Fetch error:', error);
    }

    document.getElementById('user-input').value = '';
});

function appendMessage(message, sender) {
    const chatWindow = document.getElementById('chat-window');

    const messageElement = document.createElement('div');
    messageElement.classList.add('message');
    if (sender === 'user') {
        messageElement.classList.add('user-message');
        messageElement.textContent = message;
    } else if (sender === 'bot') {
        messageElement.classList.add('bot-message');
        messageElement.textContent = message;
    }

    chatWindow.appendChild(messageElement);
    chatWindow.scrollTop = chatWindow.scrollHeight;
}
