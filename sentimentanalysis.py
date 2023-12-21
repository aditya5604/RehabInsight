def tokenize(comment):
    return comment.split()  # Basic tokenization by splitting on spaces

def calculate_sentiment_score(tokens, positive_set, negative_set):
    # Count positive and negative occurrences
    positive_count = sum(1 for token in tokens if token in positive_set)
    negative_count = sum(1 for token in tokens if token in negative_set)

    # Calculate sentiment score
    overall_score = (positive_count - negative_count) / len(tokens) if len(tokens) > 0 else 0.0

    # Classify the sentiment as positive, neutral, or negative
    if overall_score > 0.05:
        sentiment = "Positive"
    elif -0.05 < overall_score < 0.05:
        sentiment = "Neutral"
    else:
        sentiment = "Negative"

    # Return the sentiment result
    return sentiment

def read_words_from_file(file_path):
    with open(file_path, 'r') as file:
        return {word.strip().lower() for word in file.readlines()}

def read_ngrams_from_file(file_path):
    with open(file_path, 'r') as file:
        return {tuple(line.strip().lower().split()) for line in file.readlines()}

def perform_sentiment_analysis(comment, positive_unigrams, negative_unigrams,
                               positive_bigrams, negative_bigrams,
                               positive_trigrams, negative_trigrams):
    # Tokenize the comment into unigrams, bigrams, and trigrams
    unigrams = tokenize(comment)
    bigrams = list(zip(unigrams, unigrams[1:]))
    trigrams = list(zip(unigrams, unigrams[1:], unigrams[2:]))

    # Calculate unigram, bigram, and trigram sentiment scores
    unigram_sentiment = calculate_sentiment_score(unigrams, positive_unigrams, negative_unigrams)
    bigram_sentiment = calculate_sentiment_score(bigrams, positive_bigrams, negative_bigrams)
    trigram_sentiment = calculate_sentiment_score(trigrams, positive_trigrams, negative_trigrams)

    # Combine the scores for an overall sentiment
    overall_sentiment = (unigram_sentiment, bigram_sentiment, trigram_sentiment)

    return overall_sentiment
