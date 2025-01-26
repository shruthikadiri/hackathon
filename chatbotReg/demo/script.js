const input = document.querySelector("footer input");
const button = document.querySelector("footer button");
const chatContent = document.querySelector(".chat-content");

let conversationId = null;
let currentStep = "start";
let userResponses = {}; // To store user inputs for preview

// Function to add a message to the chat UI
function addMessage(sender, text) {
  const message = document.createElement("div");
  message.classList.add("chat-message");
  if (sender === "Assistant") message.classList.add("assistant");
  message.innerHTML = `<p><strong>${sender}:</strong> ${text}</p>`;
  chatContent.appendChild(message);
  chatContent.scrollTop = chatContent.scrollHeight; // Auto-scroll to latest message
}

// Function to start the chatbot conversation
function startChatbot() {
  fetch("https://chain-bot-production.up.railway.app/start", {
    method: "POST",
    headers: {
      "Accept": "application/json"
    },
    body: ""  // No body needed for start request
  })
    .then(response => {
      if (!response.ok) {
        throw new Error("Failed to start chatbot.");
      }
      return response.json();
    })
    .then(data => {
      conversationId = data.conversation_id;
      console.log("Chatbot started with ID:", conversationId);
      addMessage("Assistant", "Chatbot started. Please enter your details.");
    })
    .catch(error => {
      console.error("Error starting chatbot:", error);
      addMessage("Assistant", "Chatbot failed to start. Please try again.");
    });
}

// Function to handle the chatbot conversation process
function processChatbot(userInput) {
  if (!conversationId) {
    addMessage("Assistant", "Please wait for chatbot to start.");
    return;
  }

  userResponses[currentStep] = userInput; // Store user input for preview

  fetch("https://chain-bot-production.up.railway.app/process", {
    method: "POST",
    headers: {
      "Accept": "application/json",
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      "conversation_id": conversationId,
      "current_step": currentStep,
      "user_input": userInput
    })
  })
    .then(response => {
      if (!response.ok) {
        throw new Error("Error processing chatbot request.");
      }
      return response.json();
    })
    .then(data => {
      addMessage("Assistant", data.next_step_message);

      if (data.next_step === "confirmation") {
        showPreview(); // Show user-entered data before confirmation
        addMessage("Assistant", "Please type 'yes' to confirm.");
        currentStep = "confirmation";
      } else if (data.next_step === "completed") {
        registerDataToMongoDB(); // Save data to MongoDB
        addMessage("Assistant", "Thank you! Your registration is complete.");
        return; // Stop further processing
      } else {
        currentStep = data.next_step;
      }
    })
    .catch(error => {
      console.error("Error in chatbot process:", error);
      addMessage("Assistant", "Something went wrong. Please try again.");
    });
}

// Function to display a preview of entered data before confirmation
function showPreview() {
  let previewMessage = "<p><strong>Preview your details:</strong></p><ul>";
  for (const key in userResponses) {
    previewMessage += `<p><strong>${key}:</strong> ${userResponses[key]}</p>`;
  }
  // previewMessage += "</ul>";
  addMessage("Assistant", previewMessage);
}

// Function to register data to MongoDB
function registerDataToMongoDB() {
  fetch("http://127.0.0.1:8000/api/register/", {
    method: "POST",
    headers: {
      "Accept": "application/json",
      "Content-Type": "application/json"
    },
    mode: "cors",
    body: JSON.stringify(userResponses)
  })
    .then(response => {
      if (!response.ok) {
        throw new Error("Failed to save data to MongoDB");
      }
      return response.json();
    })
    .then(data => {
      console.log("Data saved to MongoDB:", data);
    })
    .catch(error => {
      console.error("Error saving data to MongoDB:", error);
    });
}

// Function to handle sending user messages
function sendMessage() {    
  const userMessage = input.value.trim();
  if (userMessage) {
    addMessage("User", userMessage);
    input.value = ""; // Clear input field

    if (currentStep === "confirmation" && userMessage.toLowerCase() === "yes") {
      addMessage("Assistant", "Thank you! Your registration is confirmed.");
      registerDataToMongoDB(); // Call MongoDB save function
      return; // Terminate process
    }

    processChatbot(userMessage);
  }
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

// Start the chatbot when the page loads
window.addEventListener("DOMContentLoaded", () => {
  chatContent.innerHTML = ""; // Clear chat UI
  startChatbot();
});
