# test_lemmatizer.py

from utils.lemmatizer import lemmatize_sentence  # Assuming lemmatize_sentence function is defined in a file named lemmatizer.py

def test_lemmatize_sentence():
    # Define test cases with input sentences and expected output lemmatized sentences
    test_cases = [
        ("apples", "apple"),
        ("lemons", "lemon"),
        ("limes", "lime"),
        ("bananas", "banana"),
        ("chopped tomatoes", "chopped tomato"),
        ("potatoes", "potato"),
        ("onions", "onion"),
        ("carrots", "carrot"),
        ("preserved lemons", "preserved lemon")
        # Add more test cases as needed
    ]
    
    # Iterate through test cases and assert the lemmatized output
    for input_sentence, expected_output in test_cases:
        assert lemmatize_sentence(input_sentence) == expected_output