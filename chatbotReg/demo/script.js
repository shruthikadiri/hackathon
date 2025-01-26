const input = document.querySelector("footer input");
const button = document.querySelector("footer button");
const chatContent = document.querySelector(".chat-content");

// Function to add a message to the chat
function addMessage(sender, text) {
  const message = document.createElement("div");
  message.classList.add("chat-message");
  if (sender === "Assistant") message.classList.add("assistant");
  message.innerHTML = `<p><strong>${sender}:</strong> ${text}</p>`;
  chatContent.appendChild(message);
  chatContent.scrollTop = chatContent.scrollHeight; // Scroll to the latest message
}

// Function to handle sending messages
function sendMessage() {
  const userMessage = input.value.trim();
  if (userMessage) {
    addMessage("User", userMessage);
    input.value = ""; // Clear the input field

    // Simulate a chatbot response with a delay
    setTimeout(() => {
      addMessage("Assistant", "This is a response from the chatbot.");
    }, 1000);
  }
}

// Fetch greeting message from your API and display it
function fetchGreeting() {
  fetch("https://jsonplaceholder.typicode.com/users") // Your API endpoint
    .then((response) => {
      if (! response.ok) {
        throw new Error("Failed to fetch greeting message");
      }
      console.log("success");
      
      return response.json();
    })
    .then((data) => {
        console.log("API Response:", data);
      if (data && data.message) {
        addMessage("Assistant", data.message); // Add greeting from the API
      } else {
        addMessage("Assistant", "Hello! How can I assist you today?"); // Fallback greeting
      }
    })
    .catch((error) => {
      console.error("Error fetching greeting message:", error);
      addMessage("Assistant", "Hello! How can I assist you today?"); // Fallback greeting on error
    });
}

// Event listener for the "Send" button
button.addEventListener("click", () => {
  sendMessage();
});

// Event listener for the "Enter" key
input.addEventListener("keypress", (e) => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault(); // Prevent default form submission
    sendMessage();
  }
});

// Clear initial messages and load greeting when the page loads
window.addEventListener("DOMContentLoaded", () => {
  chatContent.innerHTML = ""; // Clear any pre-existing messages in the UI
  fetchGreeting(); // Fetch and display the greeting message
});
