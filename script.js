const chatBox = document.getElementById('chat-box');
const userInput = document.getElementById('user-input');

function sendMessage() {
    const message = userInput.value.trim();
    if (message === '') return;

    displayMessage('user', message);
    userInput.value = '';

    // Send message to backend API
    fetch('/api/query', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: message })
    })
    .then(response => response.json())
    .then(data => {
        displayMessage('bot', data.message);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function displayMessage(sender, message) {
    const messageElement = document.createElement('div');
    messageElement.classList.add(sender === 'user' ? 'user-message' : 'bot-message');
    messageElement.innerText = message;
    chatBox.appendChild(messageElement);
    chatBox.scrollTop = chatBox.scrollHeight;
}

// Function to send query to backend and handle response
async function sendQueryToBackend(query) {
    try {
        const response = await fetch('/query', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ query: query })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const responseData = await response.json();
        displayResponse(responseData.response);
    } catch (error) {
        console.error('Error:', error);
        displayResponse('An error occurred while processing your request.');
    }
}

// Function to display response on the webpage
function displayResponse(response) {
    const responseContainer = document.getElementById('response-container');
    responseContainer.textContent = response;
}

// Event listener for form submission
document.getElementById('query-form').addEventListener('submit', function(event) {
    event.preventDefault(); 

    const queryInput = document.getElementById('query-input');
    const query = queryInput.value.trim();

    if (query !== '') {
        sendQueryToBackend(query);
    } else {
        displayResponse('Please enter a query.');
    }

    queryInput.value = ''; 
});
