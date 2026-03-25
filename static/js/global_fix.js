(() => {
  "use strict";

  console.log("Global fix loaded");

  const translateState = {
    originalHTML: null,
    isTranslated: false,
  };

  function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(";").shift();
    return "";
  }

  function normalizeText(value) {
    return (value || "").toLowerCase().trim();
  }

  function isTranslateTarget(el) {
    if (!el) return false;
    const text = normalizeText(el.textContent);
    if (text.includes("translate")) return true;
    const cls = normalizeText(el.className || "");
    return cls.includes("translate");
  }

  function isFloatingBottomRight(el) {
    if (!el || !(el instanceof HTMLElement)) return false;
    const style = window.getComputedStyle(el);
    if (style.position !== "fixed") return false;
    const right = parseFloat(style.right || "9999");
    const bottom = parseFloat(style.bottom || "9999");
    const w = parseFloat(style.width || "0");
    const h = parseFloat(style.height || "0");
    return right <= 60 && bottom <= 120 && w <= 80 && h <= 80;
  }

  function isChatbotTarget(el) {
    if (!el) return false;
    if (el.closest && el.closest("#global-fix-chatbox")) return false;
    const cls = normalizeText(el.className || "");
    const id = normalizeText(el.id || "");
    const text = normalizeText(el.textContent || "");
    if (id.includes("chat-toggle") || id === "chat-toggle") return true;
    if (id.includes("chat") && !id.includes("global-fix")) return true;
    if (cls.includes("chatbot") || cls.includes("chat-toggle")) return true;
    if (text === "💬" || text.includes("chat")) return true;
    return isFloatingBottomRight(el);
  }

  function getTargetLanguage() {
    const byId = document.getElementById("translate-language");
    if (byId && byId.value) return byId.value;
    const voice = document.querySelector(".voice-controls");
    if (voice) {
      const sel = voice.querySelector("select");
      if (sel && sel.value) return sel.value;
    }
    return "ta";
  }

  function runTranslate() {
    if (translateState.isTranslated && translateState.originalHTML !== null) {
      document.body.innerHTML = translateState.originalHTML;
      translateState.isTranslated = false;
      console.log("Translate: restored original page HTML");
      return;
    }

    const content = document.body.innerText;
    const target_language = getTargetLanguage();

    console.log("Translate API called", { length: content.length, target_language });

    fetch("/api/translate/", {
      method: "POST",
      credentials: "same-origin",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCookie("csrftoken"),
      },
      body: JSON.stringify({
        text: content,
        target_language: target_language,
      }),
    })
      .then(function (res) {
        if (!res.ok) throw new Error("HTTP " + res.status);
        return res.json();
      })
      .then(function (data) {
        console.log("Translate API response", data);
        if (data.translated_text) {
          if (translateState.originalHTML === null) {
            translateState.originalHTML = document.body.innerHTML;
          }
          document.body.innerText = data.translated_text;
          translateState.isTranslated = true;
        } else {
          console.warn("Translate: no translated_text in response", data);
        }
      })
      .catch(function (err) {
        console.error("Translate API error:", err);
      });
  }

  let chatboxCreated = false;

  function ensureChatbox() {
    let box = document.getElementById("global-fix-chatbox");
    if (box) return box;

    box = document.createElement("div");
    box.id = "global-fix-chatbox";
    box.style.position = "fixed";
    box.style.right = "20px";
    box.style.bottom = "95px";
    box.style.width = "320px";
    box.style.height = "380px";
    box.style.background = "rgba(0,0,0,0.85)";
    box.style.backdropFilter = "blur(8px)";
    box.style.borderRadius = "12px";
    box.style.boxShadow = "0 10px 30px rgba(0,0,0,0.4)";
    box.style.display = "none";
    box.style.flexDirection = "column";
    box.style.zIndex = "10000";
    box.style.pointerEvents = "auto";
    box.innerHTML =
      '<div style="padding:10px 12px;color:#fff;font-weight:600;border-bottom:1px solid rgba(255,255,255,0.2);">Tamilverse Chat</div>' +
      '<div id="global-fix-chat-messages" style="flex:1;overflow:auto;padding:10px;color:#fff;font-size:14px;"></div>' +
      '<div style="display:flex;border-top:1px solid rgba(255,255,255,0.2);">' +
      '<input id="global-fix-chat-input" type="text" placeholder="Ask something..." style="flex:1;padding:10px;border:none;outline:none;">' +
      '<button type="button" id="global-fix-chat-send" style="padding:10px 12px;border:none;background:#e3b46b;cursor:pointer;">Send</button>' +
      "</div>";
    document.body.appendChild(box);
    chatboxCreated = true;
    return box;
  }

  function showChatbox() {
    const box = ensureChatbox();
    box.style.display = "flex";
    console.log("Chatbot opened");
  }

  function toggleChatbox() {
    const box = ensureChatbox();
    if (box.style.display === "none" || !box.style.display) {
      box.style.display = "flex";
      console.log("Chatbot opened");
    } else {
      box.style.display = "none";
    }
  }

  function appendChatMessage(kind, text) {
    const wrap = document.getElementById("global-fix-chat-messages");
    if (!wrap) return;
    const row = document.createElement("div");
    row.style.marginBottom = "8px";
    row.style.display = "flex";
    row.style.justifyContent = kind === "user" ? "flex-end" : "flex-start";
    const bubble = document.createElement("div");
    bubble.textContent = text;
    bubble.style.maxWidth = "80%";
    bubble.style.padding = "8px 10px";
    bubble.style.borderRadius = "10px";
    bubble.style.whiteSpace = "pre-wrap";
    bubble.style.background = kind === "user" ? "#d9a441" : "#3b6f6b";
    bubble.style.color = kind === "user" ? "#000" : "#fff";
    row.appendChild(bubble);
    wrap.appendChild(row);
    wrap.scrollTop = wrap.scrollHeight;
  }

  function sendChatMessage() {
    const input = document.getElementById("global-fix-chat-input");
    if (!input) return;
    const userMessage = (input.value || "").trim();
    if (!userMessage) return;
    input.value = "";
    appendChatMessage("user", userMessage);

    console.log("Chatbot API called", { messageLength: userMessage.length });

    fetch("/api/chatbot/", {
      method: "POST",
      credentials: "same-origin",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCookie("csrftoken"),
      },
      body: JSON.stringify({ message: userMessage }),
    })
      .then(function (res) {
        if (!res.ok) throw new Error("HTTP " + res.status);
        return res.json();
      })
      .then(function (data) {
        appendChatMessage("bot", data.reply || "No response");
      })
      .catch(function (err) {
        console.error("Chatbot API error:", err);
        appendChatMessage("bot", "Server error, try again");
      });
  }

  document.addEventListener("click", function (e) {
    const target = e.target;
    if (!target || !target.closest) return;

    if (target.closest("#global-fix-chatbox")) {
      if (target.id === "global-fix-chat-send" || target.closest("#global-fix-chat-send")) {
        e.preventDefault();
        e.stopPropagation();
        sendChatMessage();
      }
      return;
    }

    if (isTranslateTarget(target)) {
      console.log("Translate clicked");
      e.preventDefault();
      e.stopPropagation();
      runTranslate();
      return;
    }

    if (target.id === "global-fix-chat-send") {
      e.preventDefault();
      sendChatMessage();
      return;
    }

    if (isChatbotTarget(target)) {
      console.log("Chatbot clicked");
      e.preventDefault();
      e.stopPropagation();
      toggleChatbox();
      return;
    }
  });

  document.addEventListener("keydown", function (e) {
    if (e.key === "Enter" && e.target && e.target.id === "global-fix-chat-input") {
      e.preventDefault();
      sendChatMessage();
    }
  });

  setTimeout(function () {
    document.querySelectorAll("*").forEach(function (el) {
      el.style.pointerEvents = "auto";
    });
  }, 1000);
})();
