document.addEventListener("DOMContentLoaded", function () {
  function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(";").shift();
    return "";
  }

  function ensureChatUi() {
    let toggle = document.getElementById("chat-toggle");
    let bot = document.getElementById("chatbot");

    if (!toggle) {
      toggle = document.createElement("div");
      toggle.id = "chat-toggle";
      toggle.textContent = "💬";
      document.body.appendChild(toggle);
    }

    if (!bot) {
      bot = document.createElement("div");
      bot.id = "chatbot";
      bot.style.display = "none";
      bot.style.flexDirection = "column";
      bot.innerHTML =
        '<div id="chat-header">Tamilverse Chat</div>' +
        '<div id="chat-body"></div>' +
        '<div id="chat-input">' +
        '<input type="text" id="chatText" placeholder="Ask travel questions...">' +
        '<button id="chat-send-btn">Send</button>' +
        "</div>";
      document.body.appendChild(bot);
    }

    // click blocking fix
    toggle.style.zIndex = "9999";
    toggle.style.pointerEvents = "auto";
    bot.style.zIndex = "9999";
    bot.style.pointerEvents = "auto";

    return { toggle, bot };
  }

  function appendMessage(type, text) {
    const chatBody = document.getElementById("chat-body");
    if (!chatBody) return;
    const div = document.createElement("div");
    div.className = type === "user" ? "user-msg" : "bot-msg";
    div.innerText = text;
    chatBody.appendChild(div);
    chatBody.scrollTop = chatBody.scrollHeight;
  }

  function toggleChat() {
    const bot = document.getElementById("chatbot");
    if (!bot) return;
    bot.style.display = bot.style.display === "flex" ? "none" : "flex";
    console.log("Chatbot opened");
  }

  async function sendMessage() {
    const input = document.getElementById("chatText");
    if (!input) return;
    const message = (input.value || "").trim();
    if (!message) return;

    appendMessage("user", message);
    input.value = "";

    try {
      const response = await fetch("/api/chatbot/", {
        method: "POST",
        credentials: "same-origin",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCookie("csrftoken"),
        },
        body: JSON.stringify({ message: message }),
      });
      const data = await response.json();
      appendMessage("bot", data.reply || "I could not answer right now.");
    } catch (error) {
      console.error("Chatbot API error:", error);
      appendMessage("bot", "Unable to connect to chatbot service.");
    }
  }

  const ui = ensureChatUi();
  window.toggleChat = toggleChat;
  window.sendMessage = sendMessage;

  ui.toggle.addEventListener("click", function (e) {
    e.preventDefault();
    toggleChat();
  });

  const sendBtn = document.getElementById("chat-send-btn") || document.querySelector("#chat-input button");
  if (sendBtn) {
    sendBtn.addEventListener("click", function (e) {
      e.preventDefault();
      sendMessage();
    });
  }

  const chatInput = document.getElementById("chatText");
  if (chatInput) {
    chatInput.addEventListener("keydown", function (e) {
      if (e.key === "Enter") {
        e.preventDefault();
        sendMessage();
      }
    });
  }
});
