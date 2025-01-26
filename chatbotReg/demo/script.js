const input = document.querySelector("footer input");
const button = document.querySelector("footer button");
const chatContent = document.querySelector(".chat-content");

button.addEventListener("click", () => {
  const userMessage = input.value.trim();
  if (userMessage) {
    addMessage("User", userMessage);
    input.value = "";

    setTimeout(() => {
      addMessage("Assistant", "This is a response from the chatbot.");
    }, 1000);
  }
});

function addMessage(sender, text) {
  const message = document.createElement("div");
  message.classList.add("chat-message");
  if (sender === "Assistant") message.classList.add("assistant");
  message.innerHTML = `<p><strong>${sender}:</strong> ${text}</p>`;
  chatContent.appendChild(message);
  chatContent.scrollTop = chatContent.scrollHeight;
}
