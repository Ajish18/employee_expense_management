console.log("AI Assistant Loaded");
let chatPanel = null;
window.addEventListener("load", () => {

    const btn = document.createElement("button");

    btn.innerHTML = "💬";

    btn.style.position = "fixed";
    btn.style.bottom = "20px";
    btn.style.right = "20px";
    btn.style.width = "60px";
    btn.style.height = "60px";
    btn.style.borderRadius = "50%";
    btn.style.fontSize = "24px";
    btn.style.zIndex = "9999";
    btn.style.cursor = "pointer";

    btn.addEventListener("click", () => {

        if (chatPanel) {
            chatPanel.remove();
            chatPanel = null;
            return;
        }

        chatPanel = document.createElement("div");

        chatPanel.style.position = "fixed";
        chatPanel.style.bottom = "90px";
        chatPanel.style.right = "20px";
        chatPanel.style.width = "350px";
        chatPanel.style.height = "500px";

        chatPanel.style.background = "white";
        chatPanel.style.border = "1px solid #ddd";
        chatPanel.style.borderRadius = "10px";

        chatPanel.style.zIndex = "9999";

        chatPanel.innerHTML = `
            <div style="
                padding:10px;
                font-weight:bold;
                border-bottom:1px solid #ddd;
            ">
                ETEMS AI Assistant
            </div>

            <div
                id="chat-messages"
                style="
                    padding:10px;
                    height:380px;
                    overflow-y:auto;
                "
            >
                <div>
                    Hello ${frappe.session.user} 👋
                </div>
            </div>

            <div style="
                padding:10px;
                border-top:1px solid #ddd;
                display:flex;
                gap:5px;
            ">
                <input
                    id="chat-input"
                    type="text"
                    placeholder="Type message..."
                    style="flex:1; padding:8px;"
                />

                <button id="send-btn">
                    Send
                </button>
            </div>
        `;
        document.body.appendChild(chatPanel);
        const messages = document.getElementById("chat-messages");
        const input = document.getElementById("chat-input");
        const sendBtn = document.getElementById("send-btn");
        sendBtn.addEventListener("click", () => {

            const userMessage = input.value;

            if (!userMessage.trim()) {
                return;
            }

            messages.innerHTML += `
                <div style="
                    text-align:right;
                    margin:10px 0;
                ">
                    You: ${userMessage}
                </div>
            `;

            frappe.call({
                method: "etems.api.ask_ai",
                args: {
                    message: userMessage
                }
            }).then(r => {

                messages.innerHTML += `
                    <div style="
                        display:flex;
                        justify-content:flex-start;
                        margin:10px 0;
                    ">
                        <div style="
                            background:#f1f1f1;
                            padding:8px 12px;
                            border-radius:10px;
                            max-width:70%;
                        ">
                            ${r.message}
                        </div>
                    </div>
                `;
            });
            input.value = "";
        });
    });
    document.body.appendChild(btn);

});