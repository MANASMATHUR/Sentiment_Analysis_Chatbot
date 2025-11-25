from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

class SentimentAnalyzer:
    def __init__(self):
        self.analyzer = SentimentIntensityAnalyzer()

    def analyze_text(self, text):
        if not text:
            return {"score": 0.0, "label": "Neutral"}

        scores = self.analyzer.polarity_scores(text)
        compound_score = scores['compound']

        if compound_score >= 0.05:
            label = "Positive"
        elif compound_score <= -0.05:
            label = "Negative"
        else:
            label = "Neutral"

        return {"score": compound_score, "label": label}

    def analyze_conversation(self, messages):
        if not messages:
            return {
                "score": 0.0,
                "label": "Neutral",
                "trend": "No data",
                "direction": "Neutral – no conversation recorded yet."
            }

        total_score = 0
        scores = []
        normalized_messages = self._normalize_messages(messages)
        
        for msg in normalized_messages:
            result = self.analyze_text(msg)
            total_score += result['score']
            scores.append(result['score'])

        if not scores:
            return {
                "score": 0.0,
                "label": "Neutral",
                "trend": "No data",
                "direction": "Neutral – no conversation recorded yet."
            }

        avg_score = total_score / len(scores)

        if avg_score >= 0.05:
            label = "Positive"
        elif avg_score <= -0.05:
            label = "Negative"
        else:
            label = "Neutral"
            
        trend = self.get_trend(scores)
        direction = self.describe_direction(label, trend)

        return {"score": avg_score, "label": label, "trend": trend, "direction": direction}

    def get_trend(self, scores):
        if len(scores) < 2:
            return "Stable"

        mid = len(scores) // 2
        first_half = scores[:mid]
        second_half = scores[mid:]
        
        avg_first = sum(first_half) / len(first_half) if first_half else 0
        avg_second = sum(second_half) / len(second_half) if second_half else 0
        
        diff = avg_second - avg_first
        
        if diff > 0.1:
            return "Improving"
        elif diff < -0.1:
            return "Declining"
        
        return "Stable"

    def describe_direction(self, label, trend):
        directions = {
            "Positive": "Positive – upbeat and optimistic exchange.",
            "Negative": "Negative – general dissatisfaction detected.",
            "Neutral": "Neutral – balanced or mixed sentiment overall."
        }

        description = directions.get(label, "Neutral – balanced or mixed sentiment overall.")

        if trend == "Improving":
            description += " Mood improved as the conversation progressed."
        elif trend == "Declining":
            description += " Mood declined as the conversation progressed."

        return description

    def _normalize_messages(self, messages):
        normalized = []
        for msg in messages:
            if isinstance(msg, str):
                normalized.append(msg)
            elif isinstance(msg, dict):
                content = msg.get("content")
                if content:
                    normalized.append(content)
        return normalized
