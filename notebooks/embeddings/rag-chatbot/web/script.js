document.getElementById('sendButton').addEventListener('click', sendMessage);
document.getElementById('message').addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
        sendMessage();
    }
});

async function sendMessage() {
    const url = document.getElementById('url').value;
    const message = document.getElementById('message').value;

    if (!url || !message) {
        alert('Please enter both URL and message.');
        return;
    }

    const chatHistory = document.getElementById('chatHistory');

    // Display user message
    const userMessageElement = document.createElement('div');
    userMessageElement.classList.add('message', 'user');
    userMessageElement.textContent = message;
    chatHistory.appendChild(userMessageElement);

    // Send the message to the server
    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ question: message })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();

        // Display server response
        const serverMessageElement = document.createElement('div');
        serverMessageElement.classList.add('message', 'server');
        serverMessageElement.textContent = data.answer;
        chatHistory.appendChild(serverMessageElement);
    } catch (error) {
        console.error('Error:', error);
        alert('Failed to send message. Check console for details.');
    }

    // Clear the message input
    document.getElementById('message').value = '';
}
