// Handle file upload
document.getElementById('file-upload').addEventListener('change', async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    const status = document.getElementById('upload-status');
    status.textContent = "🔄 Uploading and processing file...";

    const formData = new FormData();
    formData.append('file', file);

    try {
        const res = await fetch('http://127.0.0.1:5000/upload', {
            method: 'POST',
            body: formData
        });

        const data = await res.json();

        if (res.ok) {
            status.textContent = "✅ File uploaded!";
        } else {
            status.textContent = "❌ Error: " + (data.error || "Unknown error");
        }

    } catch (err) {
        status.textContent = "❌ Network error";
        console.error('Upload error:', err);
    }
});

// Handle user questions
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
