(function () {
  "use strict";

  function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(";").shift();
    return "";
  }

  function qs(sel, root) {
    return (root || document).querySelector(sel);
  }

  function qsa(sel, root) {
    return Array.from((root || document).querySelectorAll(sel));
  }


  function getMainContentRoot() {
    return (
      qs(".page") ||
      qs("main") ||
      qs("section") ||
      document.body
    );
  }

  function collectTextNodes(root) {
    const nodes = [];
    const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, {
      acceptNode: function (node) {
        if (!node || !node.nodeValue) return NodeFilter.FILTER_REJECT;
        const text = node.nodeValue.trim();
        if (!text) return NodeFilter.FILTER_REJECT;
        const parent = node.parentElement;
        if (!parent) return NodeFilter.FILTER_REJECT;
        if (parent.closest(".navbar")) return NodeFilter.FILTER_REJECT;
        if (parent.closest("#chatbot")) return NodeFilter.FILTER_REJECT;
        const tag = parent.tagName;
        if (tag === "SCRIPT" || tag === "STYLE" || tag === "NOSCRIPT") return NodeFilter.FILTER_REJECT;
        return NodeFilter.FILTER_ACCEPT;
      },
    });
    let current;
    while ((current = walker.nextNode())) {
      nodes.push(current);
    }
    return nodes;
  }


  function ensureChatUI() {
    let toggle = qs("#chat-toggle");
    let bot = qs("#chatbot");
    if (!toggle) {
      toggle = document.createElement("div");
      toggle.id = "chat-toggle";
      toggle.textContent = "💬";
      document.body.appendChild(toggle);
    }
    if (!bot) {
      bot = document.createElement("div");
      bot.id = "chatbot";
      bot.innerHTML =
        '<div id="chat-header">Tamilverse Chat</div>' +
        '<div id="chat-body"></div>' +
        '<div id="chat-input"><input type="text" id="chatText" placeholder="Ask travel questions..."><button id="chat-send-btn">Send</button></div>';
      document.body.appendChild(bot);
    }
    return { toggle, bot };
  }

  async function sendChatMessage() {
    const input = qs("#chatText");
    const body = qs("#chat-body");
    if (!input || !body) return;
    const msg = (input.value || "").trim();
    if (!msg) return;

    const userDiv = document.createElement("div");
    userDiv.className = "user-msg";
    userDiv.innerText = msg;
    body.appendChild(userDiv);
    input.value = "";

    try {
      const response = await fetch("/api/chatbot/", {
        method: "POST",
        credentials: "same-origin",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCookie("csrftoken"),
        },
        body: JSON.stringify({ message: msg }),
      });
      const data = await response.json();
      const botDiv = document.createElement("div");
      botDiv.className = "bot-msg";
      botDiv.innerText = data.reply || "Sorry, I could not generate a response.";
      body.appendChild(botDiv);
      body.scrollTop = body.scrollHeight;
    } catch (err) {
      const botDiv = document.createElement("div");
      botDiv.className = "bot-msg";
      botDiv.innerText = "Unable to connect to chatbot right now.";
      body.appendChild(botDiv);
      body.scrollTop = body.scrollHeight;
      console.error("Chatbot error:", err);
    }
  }

  function attachChatbotHandler() {
    const ui = ensureChatUI();
    window.toggleChat = function () {
      const bot = qs("#chatbot");
      if (!bot) return;
      bot.style.display = bot.style.display === "flex" ? "none" : "flex";
    };
    window.sendMessage = sendChatMessage;

    ui.toggle.addEventListener("click", window.toggleChat);
    const sendBtn = qs("#chat-send-btn") || qsa("#chat-input button")[0];
    if (sendBtn) {
      if (sendBtn.id === "chat-send-btn" || !sendBtn.getAttribute("onclick")) {
        sendBtn.addEventListener("click", function (e) {
          e.preventDefault();
          sendChatMessage();
        });
      }
    }
    const input = qs("#chatText");
    if (input) {
      input.addEventListener("keydown", function (e) {
        if (e.key === "Enter") {
          e.preventDefault();
          sendChatMessage();
        }
      });
    }
  }

  function init() {
    attachChatbotHandler();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
