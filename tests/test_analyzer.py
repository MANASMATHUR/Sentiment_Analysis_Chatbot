import pytest
from src.analyzer import SentimentAnalyzer

@pytest.fixture
def analyzer():
    return SentimentAnalyzer()

def test_analyze_text_positive(analyzer):
    result = analyzer.analyze_text("I love this service!")
    assert result['label'] == "Positive"
    assert result['score'] > 0.05

def test_analyze_text_negative(analyzer):
    result = analyzer.analyze_text("This is terrible.")
    assert result['label'] == "Negative"
    assert result['score'] < -0.05

def test_analyze_text_neutral(analyzer):
    result = analyzer.analyze_text("The sky is blue.")
    # Neutral range is -0.05 to 0.05. "The sky is blue" is usually neutral.
    assert result['label'] == "Neutral"

def test_analyze_conversation_trend_improving(analyzer):
    messages = ["This is bad", "This is okay", "This is great"]
    # Scores roughly: -neg, 0, +pos. Trend should be improving.
    result = analyzer.analyze_conversation(messages)
    assert result['trend'] == "Improving"

def test_analyze_conversation_trend_declining(analyzer):
    messages = ["This is great", "This is okay", "This is bad"]
    result = analyzer.analyze_conversation(messages)
    assert result['trend'] == "Declining"

def test_analyze_conversation_empty(analyzer):
    result = analyzer.analyze_conversation([])
    assert result['label'] == "Neutral"
    assert result['score'] == 0.0
    assert "Neutral" in result['direction']

def test_analyze_conversation_direction_positive(analyzer):
    messages = ["I am thrilled", "This is fantastic"]
    result = analyzer.analyze_conversation(messages)
    assert result['label'] == "Positive"
    assert "Positive" in result['direction']

def test_analyze_conversation_accepts_history_objects(analyzer):
    history = [
        {"role": "user", "content": "This is awesome"},
        {"role": "bot", "content": "Glad to hear that!"},
        {"role": "user", "content": "Still awesome"}
    ]
    result = analyzer.analyze_conversation(history)
    assert result['label'] in {"Positive", "Neutral"}  # bot response should not break parsing
    assert 'direction' in result
