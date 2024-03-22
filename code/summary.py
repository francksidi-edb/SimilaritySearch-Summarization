import time
from transformers import LEDTokenizer, LEDForConditionalGeneration

def main():
    start_time = time.time()

    # Sample text for summarization
    sample_text = """
    Jupiter is the fifth planet from the Sun and the largest in the Solar System.
    It is a gas giant with a mass one-thousandth that of the Sun, but two-and-a-half times that of all the other planets in the Solar System combined.
    Jupiter is one of the brightest objects visible to the naked eye in the night sky and has been known to ancient civilizations since before recorded history.
    It is named after the Roman god Jupiter.
    """

    # Load the LED model and tokenizer
    load_start_time = time.time()
    tokenizer = LEDTokenizer.from_pretrained('allenai/led-base-16384')
    model = LEDForConditionalGeneration.from_pretrained('allenai/led-base-16384')
    load_end_time = time.time()
    print(f"Model loading time: {load_end_time - load_start_time:.2f} seconds")

    # Tokenize and generate summary
    tokenize_start_time = time.time()
    inputs = tokenizer.encode(sample_text, return_tensors="pt", truncation=True, padding="max_length", max_length=16384)
    tokenize_end_time = time.time()
    print(f"Tokenization time: {tokenize_end_time - tokenize_start_time:.2f} seconds")

    generation_start_time = time.time()
    summary_ids = model.generate(inputs, num_beams=2, length_penalty=2.0, max_length=150, min_length=40, early_stopping=True)
    generation_end_time = time.time()
    print(f"Summary generation time: {generation_end_time - generation_start_time:.2f} seconds")

    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

    # Print the generated summary
    print("Generated Summary:")
    print(summary)

    total_end_time = time.time()
    print(f"Total execution time: {total_end_time - start_time:.2f} seconds")

if __name__ == "__main__":
    main()

