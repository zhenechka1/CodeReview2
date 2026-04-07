import re
from collections import Counter


class SentimentAnalyzer:
    """Simple sentiment analyzer based on word lists."""

    def __init__(self):
        self.positive_words = {
            'good', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic',
            'love', 'happy', 'joy', 'perfect', 'beautiful', 'awesome',
            'best', 'brilliant', 'superb', 'outstanding'
        }

        self.negative_words = {
            'bad', 'terrible', 'awful', 'horrible', 'poor', 'worst',
            'hate', 'sad', 'disappointing', 'disgusting', 'annoying',
            'frustrating', 'boring', 'dreadful'
        }

        self.stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to',
            'for', 'of', 'with', 'is', 'was', 'are', 'be'
        }

    def clean_text(self, text: str) -> list[str]:
        """Clean and tokenize text."""
        text = text.lower()
        text = re.sub(r"[^\w\s]", "", text)
        return [word for word in text.split() if len(word) > 2]

    def analyze(self, text: str) -> tuple[str, float, int, int]:
        """Analyze sentiment of text."""
        words = self.clean_text(text)

        pos_count = sum(word in self.positive_words for word in words)
        neg_count = sum(word in self.negative_words for word in words)

        total = len(words)
        if total == 0:
            return "neutral", 0.0, pos_count, neg_count

        score = (pos_count - neg_count) / total * 100

        if score > 5:
            sentiment = "positive"
        elif score < -5:
            sentiment = "negative"
        else:
            sentiment = "neutral"

        return sentiment, score, pos_count, neg_count

    def word_frequency(self, text: str, top_n: int = 10):
        """Return most common words excluding stop words."""
        words = self.clean_text(text)
        filtered = [w for w in words if w not in self.stop_words]
        return Counter(filtered).most_common(top_n)

    def generate_ascii_cloud(self, word_freq, width: int = 60) -> str:
        """Generate simple ASCII word cloud."""
        if not word_freq:
            return "No words to display"

        max_freq = word_freq[0][1]
        cloud_words = []

        for word, freq in word_freq:
            size = int((freq / max_freq) * 3) + 1
            if size == 1:
                display = word
            elif size == 2:
                display = word.upper()
            else:
                display = f"**{word.upper()}**"
            cloud_words.append(display)

        lines, current_line, length = [], [], 0

        for word in cloud_words:
            word_len = len(word) + 2
            if length + word_len > width:
                lines.append("  ".join(current_line))
                current_line, length = [word], word_len
            else:
                current_line.append(word)
                length += word_len

        if current_line:
            lines.append("  ".join(current_line))

        return "\n".join(lines)


def main():
    analyzer = SentimentAnalyzer()

    print("Enter text (empty line to finish):")
    lines = []

    while True:
        line = input()
        if not line:
            break
        lines.append(line)

    text = "\n".join(lines).strip()

    if not text:
        print("No text entered.")
        return

    sentiment, score, pos, neg = analyzer.analyze(text)

    print(f"\nSentiment: {sentiment.upper()}")
    print(f"Score: {score:.2f}% | +{pos} | -{neg}")

    freq = analyzer.word_frequency(text)

    print("\nWord Cloud:")
    print(analyzer.generate_ascii_cloud(freq))

    print("\nTop Words:")
    for word, count in freq:
        print(f"{word:10} | {'█' * count} ({count})")


if __name__ == "__main__":
    main()
