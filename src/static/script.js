document.addEventListener('DOMContentLoaded', () => {
    const chatBox = document.getElementById('chat-box');
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');
    const endChatBtn = document.getElementById('end-chat-btn');
    const themeToggle = document.getElementById('theme-toggle');
    const chartToggleBtn = document.getElementById('chart-toggle-btn');
    const chartPanel = document.getElementById('chart-panel');
    const closeChartBtn = document.getElementById('close-chart-btn');
    const modal = document.getElementById('summary-modal');
    const closeModalBtn = document.getElementById('close-modal-btn');

    const ctx = document.getElementById('sentimentChart').getContext('2d');
    const sentimentChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Sentiment Score',
                data: [],
                borderColor: '#4f46e5',
                backgroundColor: 'rgba(79, 70, 229, 0.1)',
                tension: 0.4,
                fill: true
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: false,
                    min: -1,
                    max: 1,
                    grid: { color: 'rgba(0, 0, 0, 0.1)' }
                },
                x: {
                    grid: { display: false }
                }
            },
            plugins: {
                legend: { display: false }
            }
        }
    });

    let messageCount = 0;

    themeToggle.addEventListener('click', () => {
        document.body.classList.toggle('dark-mode');
        const isDark = document.body.classList.contains('dark-mode');
        themeToggle.textContent = isDark ? '☀️' : '🌙';

        sentimentChart.options.scales.y.grid.color = isDark ? 'rgba(255, 255, 255, 0.1)' : 'rgba(0, 0, 0, 0.1)';
        sentimentChart.update();
    });

    chartToggleBtn.addEventListener('click', () => {
        chartPanel.classList.toggle('hidden');
        chartToggleBtn.textContent = chartPanel.classList.contains('hidden') ? '📈 Trend' : 'Hide Trend';
    });

    closeChartBtn.addEventListener('click', () => {
        chartPanel.classList.add('hidden');
        chartToggleBtn.textContent = '📈 Trend';
    });

    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendMessage();
    });

    sendBtn.addEventListener('click', sendMessage);

    endChatBtn.addEventListener('click', async () => {
        const response = await fetch('/summary');
        const data = await response.json();

        document.getElementById('summary-sentiment').textContent = data.label;
        document.getElementById('summary-direction').textContent = data.direction;
        document.getElementById('summary-trend').textContent = data.trend;
        document.getElementById('summary-score').textContent = data.score.toFixed(2);

        modal.classList.remove('hidden');
    });

    closeModalBtn.addEventListener('click', () => {
        modal.classList.add('hidden');
        location.reload();
    });

    async function sendMessage() {
        const text = userInput.value.trim();
        if (!text) return;

        addMessage(text, 'user');
        userInput.value = '';

        const typingIndicator = showTypingIndicator();

        try {
            await new Promise(r => setTimeout(r, 800));

            const response = await fetch('/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: text })
            });

            const data = await response.json();

            typingIndicator.remove();

            const sentimentText = `Sentiment: ${data.sentiment.label} (${data.sentiment.score.toFixed(2)})`;
            addMessage(data.response, 'bot', sentimentText);

            messageCount++;
            sentimentChart.data.labels.push(messageCount);
            sentimentChart.data.datasets[0].data.push(data.sentiment.score);
            sentimentChart.update();

        } catch (error) {
            console.error('Error:', error);
            typingIndicator.remove();
            addMessage("Sorry, something went wrong.", 'bot');
        }
    }

    function addMessage(text, role, sentiment = null) {
        const div = document.createElement('div');
        div.classList.add('message', role === 'user' ? 'user-message' : 'bot-message');

        const content = document.createElement('div');
        content.textContent = text;
        div.appendChild(content);

        if (sentiment) {
            const sentimentSpan = document.createElement('span');
            sentimentSpan.classList.add('sentiment-tag');
            sentimentSpan.textContent = sentiment;
            div.appendChild(sentimentSpan);
        }

        chatBox.appendChild(div);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    function showTypingIndicator() {
        const div = document.createElement('div');
        div.classList.add('typing-indicator');
        div.innerHTML = '<div class="dot"></div><div class="dot"></div><div class="dot"></div>';
        chatBox.appendChild(div);
        chatBox.scrollTop = chatBox.scrollHeight;
        return div;
    }
});
