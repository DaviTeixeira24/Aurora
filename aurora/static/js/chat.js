const chatHistory = document.getElementById("chat-history");
const userInput = document.getElementById("user-input");
const sendButton = document.getElementById("send-button");
const voiceToggle = document.getElementById("voice-toggle");

let conversationHistory = [
  { role: "system", content: "Você é um assistente atencioso." },
];
let voiceEnabled = true;

sendButton.addEventListener("click", sendMessage);
userInput.addEventListener("keypress", function (e) {
  if (e.key === "Enter") {
    sendMessage();
  }
});

voiceToggle.addEventListener("click", function () {
  voiceEnabled = !voiceEnabled;
  if (voiceEnabled) {
    voiceToggle.textContent = "Voz: Ligada";
    voiceToggle.classList.remove("off");
  } else {
    voiceToggle.textContent = "Voz: Desligada";
    voiceToggle.classList.add("off");
  }
});

function sendMessage() {
  const message = userInput.value.trim();
  if (message) {
    appendMessage("Você", message, "user-message");
    userInput.value = "";

    axios
      .post("/chat", {
        user_input: message,
        conversation_history: conversationHistory,
        voice_enabled: voiceEnabled,
      })
      .then(function (response) {
        const assistantResponse = response.data.response;
        appendMessage("Aurora", assistantResponse, "assistant-message");
        conversationHistory = response.data.conversation_history;

        if (voiceEnabled && response.data.audio_file) {
          const audio = new Audio(`/stream-audio/${response.data.audio_file}`);
          audio.play();
        }
      })
      .catch(function (error) {
        console.error("Erro:", error);
        appendMessage(
          "Erro",
          "Ocorreu um erro ao processar sua solicitação.",
          "assistant-message"
        );
      });
  }
}

function appendMessage(sender, message, className) {
  const messageElement = document.createElement("div");
  messageElement.className = `message ${className}`;

  if (className === "assistant-message") {
    messageElement.innerHTML = `
      <img src="/static/images/LogoAurora.png" alt="Assistente" class="profile-pic">
      <div class="message-content">
        <strong>${sender}:</strong> ${message}
      </div>
    `;
  } else {
    messageElement.innerHTML = `${message}`;
  }

  chatHistory.appendChild(messageElement);
  chatHistory.scrollTop = chatHistory.scrollHeight;
}

/*function appendMessage(sender, message, className) {
  const messageElement = document.createElement("div");
  messageElement.className = `message ${className}`;
  messageElement.innerHTML = `<strong>${sender}:</strong> ${message}`;
  chatHistory.appendChild(messageElement);
  chatHistory.scrollTop = chatHistory.scrollHeight;
}*/
