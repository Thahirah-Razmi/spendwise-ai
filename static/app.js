const chat = document.getElementById("chat");
const messageInput = document.getElementById("message");


function addMessage(text, type) {

    const message = document.createElement("div");

    message.className = `message ${type}`;

    message.textContent = text;

    chat.appendChild(message);

    chat.scrollTop = chat.scrollHeight;
}


async function sendMessage() {

    const message = messageInput.value.trim();

    if (!message) {
        return;
    }

    addMessage(message, "user");

    messageInput.value = "";

    addMessage("Thinking...", "assistant");

    try {

        const response = await fetch("/api/chat", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                message: message
            })

        });

        const data = await response.json();

        const messages =
            document.querySelectorAll(".assistant");

        messages[messages.length - 1].remove();

        addMessage(
            data.response,
            "assistant"
        );

        if (data.tool_call) {

            console.log(
                "Tool executed:",
                data.tool_call
            );
        }

    } catch (error) {

        const messages =
            document.querySelectorAll(".assistant");

        messages[messages.length - 1].remove();

        addMessage(
            "Something went wrong.",
            "assistant"
        );

        console.error(error);
    }
}


function useExample(text) {

    messageInput.value = text;

    messageInput.focus();
}


messageInput.addEventListener(
    "keydown",
    event => {

        if (event.key === "Enter") {
            sendMessage();
        }

    }
);