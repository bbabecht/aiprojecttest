document.addEventListener('DOMContentLoaded', () => {
    const promptInput = document.getElementById('prompt-input');
    const sendButton = document.getElementById('send-button');
    const responseArea = document.getElementById('response-area');

    // Function to add a message to the chat box
    function addMessage(text, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', sender);
        messageDiv.textContent = text;
        responseArea.appendChild(messageDiv);
        responseArea.scrollTop = responseArea.scrollHeight; // Scroll to bottom
    }

    sendButton.addEventListener('click', async () => {
        const promptText = promptInput.value.trim();

        if (promptText) {
            addMessage(promptText, 'user-message'); // Display user's prompt
            promptInput.value = ''; // Clear input field

            try {
                const response = await fetch('/api/prompt', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ prompt: promptText }),
                });

                if (!response.ok) {
                    const errorData = await response.json().catch(() => ({ error: 'Failed to parse error response' }));
                    throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
                }

                const data = await response.json();

                if (data.error) {
                    addMessage(`Error: ${data.error}`, 'agent-message');
                } else {
                    addMessage(data.response, 'agent-message');
                }

            } catch (error) {
                console.error('Error sending prompt:', error);
                addMessage(`Error: Could not reach the backend. ${error.message}`, 'agent-message');
            }
        }
    });

    promptInput.addEventListener('keypress', (event) => {
        if (event.key === 'Enter') {
            sendButton.click();
        }
    });
});
