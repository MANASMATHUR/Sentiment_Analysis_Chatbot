from src.analyzer import SentimentAnalyzer

class Chatbot:
    def __init__(self):
        self.analyzer = SentimentAnalyzer()
        self.history = []
        self.user_messages = []

    def process_input(self, user_input):
        sentiment_result = self.analyzer.analyze_text(user_input)
        
        self.history.append({"role": "user", "content": user_input})
        self.user_messages.append(user_input)
        
        response_text = self.generate_response(user_input, sentiment_result['label'])
        self.history.append({"role": "bot", "content": response_text})
        
        return {
            "response": response_text,
            "sentiment": sentiment_result
        }

    def generate_response(self, user_input, sentiment_label):
        if sentiment_label == "Negative":
            return "I'm sorry to hear that. I'll do my best to help."
        elif sentiment_label == "Positive":
            return "That's great to hear! How else can I assist you?"
        
        return "I understand. Please tell me more."

    def get_conversation_summary(self):
        return self.analyzer.analyze_conversation(self.history)
