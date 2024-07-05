<!-- src/components/Chat.vue -->
<script>
export default {
    data() {
        return {
            messages: [],
            userInput: ''
        };
    },
    methods: {
        sendMessage() {
            if (this.userInput.trim() !== '') {
                this.messages.push({ text: this.userInput, sender: 'user' });
                this.userInput = '';
                this.$nextTick(() => {
                    this.scrollToBottom();
                });
                this.getGptResponse();
            }
        },
        getGptResponse() {
            // 模拟 ChatGPT 的回复
            setTimeout(() => {
                const gptReply = 'This is a GPT response!';
                this.messages.push({ text: gptReply, sender: 'gpt' });
                this.$nextTick(() => {
                    this.scrollToBottom();
                });
            }, 1000);
        },
        scrollToBottom() {
            const chatBox = this.$refs.chatBox;
            chatBox.scrollTop = chatBox.scrollHeight;
        }
    }
};
</script>

<template>
    <Card style="height: 75vh; width: 60%; overflow: hidden; position: relative">
        <template #title>
            <div class="card-title">Chat with AI</div>
        </template>
        <template #content>
            <div class="chat-container">
                <div class="chat-box" ref="chatBox">
                    <div style="width: 40vh" v-for="(message, index) in messages" :key="index" :class="['message', message.sender]">
                        <span>{{ message.text }}</span>
                    </div>
                </div>
                <div class="input-box">
                    <input type="text" v-model="userInput" @keyup.enter="sendMessage" placeholder="Type a message..." />
                    <button @click="sendMessage">Send</button>
                </div>
            </div>
        </template>
    </Card>
</template>

<style scoped>
.chat-container {
    display: flex;
    flex-direction: column;
    height: 100%;
    position: relative;
}

.card-title {
    position: sticky;
    top: 0;
    background-color: white;
    padding: 10px;
    border-bottom: 1px solid #ccc;
    z-index: 1;
}

.chat-box {
    flex-grow: 1;
    overflow-y: auto;
    padding-top: 10px; /* Ensure messages are not hidden behind the title */
    margin-bottom: 60px; /* Space for the input box */
    height: 50vh;
    display: flex;
    flex-direction: column;
}

.message {
    max-width: 60%;
    margin: 5px;
    padding: 10px;
    border-radius: 10px;
}

.message.user {
    align-self: flex-end;
    background-color: #d1e7dd;
}

.message.gpt {
    align-self: flex-start;
    background-color: #f8d7da;
}

.input-box {
    display: flex;
    align-items: center;
    padding: 10px;
    border-top: 1px solid #ccc;
    background-color: #fff;
    position: sticky;
    bottom: 0;
    z-index: 1;
}

input[type='text'] {
    flex-grow: 1;
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 5px;
    box-sizing: border-box;
}

button {
    margin-left: 10px;
    padding: 10px;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
}
</style>
