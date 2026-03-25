import os
import glob

directories = [
    r"c:\Users\Admin\Desktop\Tamilverse_app\templates\auth",
    r"c:\Users\Admin\Desktop\Tamilverse_app\templates\pages"
]

fetch_code = """fetch("/api/chatbot/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ message: msg })
  })
  .then(res => res.json())
  .then(data => {
    const botDiv = document.createElement("div");
    botDiv.className = "bot-msg";
    botDiv.innerText = data.reply;
    chatBody.appendChild(botDiv);
    chatBody.scrollTop = chatBody.scrollHeight;
  })
  .catch(() => {
    const botDiv = document.createElement("div");
    botDiv.className = "bot-msg";
    botDiv.innerText = "⚠️ Server error. Try again.";
    chatBody.appendChild(botDiv);
  });"""

for directory in directories:
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".html"):
                filepath = os.path.join(root, file)
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()

                fn_idx = content.find("function sendMessage()")
                if fn_idx == -1:
                    continue
                
                if 'fetch("/api/chatbot/' in content[fn_idx:]:
                    print(f"Skipping {filepath} - already has fetch")
                    continue
                
                input_idx = content.find('input.value = "";', fn_idx)
                if input_idx == -1:
                    continue
                    
                timeout_idx = content.find('setTimeout(() => {', input_idx)
                if timeout_idx == -1:
                    continue
                    
                end_idx = content.find('}, 600);', timeout_idx)
                if end_idx == -1:
                    # the indent might be different or no 600?
                    end_idx = content.find('});', timeout_idx)
                    if end_idx != -1:
                         end_idx += len('});')
                else:
                    end_idx += len('}, 600);')
                
                if end_idx != -1:
                    comment_idx = content.rfind('// Dummy bot reply', input_idx, timeout_idx)
                    replace_start = comment_idx if comment_idx != -1 else timeout_idx
                    
                    new_content = content[:replace_start] + fetch_code + content[end_idx:]
                    
                    with open(filepath, "w", encoding="utf-8") as f:
                        f.write(new_content)
                    print(f"Fixed {filepath}")
                else:
                    print(f"Could not find end of timeout in {filepath}")
