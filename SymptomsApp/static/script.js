const chatbotToggler = document.querySelector(".chatbot-toggler");
const closeBtn = document.querySelector(".close-btn");
const chatbox = document.querySelector(".chatbox");
const chatInput = document.querySelector(".chat-input textarea");
const sendChatBtn = document.querySelector(".chat-input span");

let userMessage = null; // Variable to store user's message
const inputInitHeight = chatInput.scrollHeight;


const createChatLi = (message, className) => {
  // Create a chat <li> element with passed message and className
  const chatLi = document.createElement("li");
  chatLi.classList.add("chat", `${className}`);
  let chatContent = className === "outgoing" ? `<p></p>` : `<span class="material-symbols-outlined">smart_toy</span><p></p>`;
  chatLi.innerHTML = chatContent;
  chatLi.querySelector("p").textContent = message;
  return chatLi; // return chat <li> element
}

const generateResponse = async (chatElement) => {
  const messageElement = chatElement.querySelector("p");
  
  // Create AbortController for timeout
  const controller = new AbortController();
  const timeoutId = setTimeout(() => {
    controller.abort();
  }, 120000); // 2 minute timeout

  try {
    // Update message to show processing
    messageElement.textContent = "Processing your symptoms...";
    
    const API_URL = "http://127.0.0.1:8000/ChatData?" + new URLSearchParams({"mytext": userMessage}).toString();
    
    const response = await fetch(API_URL, {
      method: "GET",
      signal: controller.signal,
      headers: {
        'Content-Type': 'application/json',
      }
    });
    
    clearTimeout(timeoutId);
    
    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`Server error: ${response.status} - ${errorText}`);
    }
    
    const data = await response.text();
    
    // Check if response is empty or invalid
    if (!data || data.trim() === '') {
      throw new Error("Empty response from server");
    }
    
    // Update the message element with the response
    messageElement.textContent = data;
    
  } catch (error) {
    clearTimeout(timeoutId);
    
    // Handle different types of errors
    messageElement.classList.add("error");
    
    if (error.name === 'AbortError') {
      messageElement.textContent = "Request timed out. Please try again with a shorter question.";
    } else if (error.message.includes('Failed to fetch')) {
      messageElement.textContent = "Connection error. Please check if the server is running.";
    } else if (error.message.includes('Server error')) {
      messageElement.textContent = "Server error occurred. Please try again later.";
    } else {
      messageElement.textContent = `Error: ${error.message}`;
    }
    
    console.error('Chat error:', error);
  } finally {
    chatbox.scrollTo(0, chatbox.scrollHeight);
  }
}

const handleChat = () => {
  userMessage = chatInput.value.trim(); // Get user entered message and remove extra whitespace
  if (!userMessage) return;

  // Clear the input textarea and set its height to default
  chatInput.value = "";
  chatInput.style.height = `${inputInitHeight}px`;

  // Append the user's message to the chatbox
  chatbox.appendChild(createChatLi(userMessage, "outgoing"));
  chatbox.scrollTo(0, chatbox.scrollHeight);

  setTimeout(() => {
    // Display "Thinking..." message while waiting for the response
    const incomingChatLi = createChatLi("Thinking...", "incoming");
    chatbox.appendChild(incomingChatLi);
    chatbox.scrollTo(0, chatbox.scrollHeight);
    generateResponse(incomingChatLi);
  }, 600);
}

chatInput.addEventListener("input", () => {
  // Adjust the height of the input textarea based on its content
  chatInput.style.height = `${inputInitHeight}px`;
  chatInput.style.height = `${chatInput.scrollHeight}px`;
});

chatInput.addEventListener("keydown", (e) => {
  // If Enter key is pressed without Shift key and the window 
  // width is greater than 800px, handle the chat
  if (e.key === "Enter" && !e.shiftKey && window.innerWidth > 800) {
    e.preventDefault();
    handleChat();
  }
});

sendChatBtn.addEventListener("click", handleChat);
closeBtn.addEventListener("click", () => document.body.classList.remove("show-chatbot"));
chatbotToggler.addEventListener("click", () => document.body.classList.toggle("show-chatbot"));