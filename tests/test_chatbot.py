import pytest
from src.chatbot import Chatbot

@pytest.fixture
def bot():
    return Chatbot()

def test_process_input_stores_history(bot):
    user_input = "Hello"
    bot.process_input(user_input)
    assert len(bot.history) == 2 # 1 user msg, 1 bot response
    assert bot.history[0]['role'] == "user"
    assert bot.history[0]['content'] == "Hello"
    assert bot.history[1]['role'] == "bot"

def test_process_input_returns_sentiment(bot):
    user_input = "I am sad"
    result = bot.process_input(user_input)
    assert 'sentiment' in result
    assert result['sentiment']['label'] == "Negative"

def test_get_conversation_summary(bot):
    bot.process_input("Good job")
    bot.process_input("Bad job")
    summary = bot.get_conversation_summary()
    assert 'label' in summary
    assert 'trend' in summary
    assert 'direction' in summary
