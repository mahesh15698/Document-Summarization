from flask import Flask, render_template, request, jsonify
from transformers import pipeline

app = Flask(__name__)

def huggingFace(text):
    # Load the text summarization pipeline
    summarizer = pipeline("summarization")

    # Split the text into chunks of maximum 600 words
    max_words = 600
    chunks = [text[i:i+max_words] for i in range(0, len(text), max_words)]

    summaries = []
    # Process each chunk and generate a summary
    for chunk in chunks:
        summary = summarizer(chunk, max_length=250, min_length=50, do_sample=False)[0]["summary_text"]
        summaries.append(summary)

    # Combine the summaries into a single string
    combined_summary = " ".join(summaries)

    # Return the combined summary
    return combined_summary

@app.route('/')
def home():
    return render_template('summary.html')

@app.route('/summary', methods=['POST'])
def summary():
    if request.method == 'POST':
        article_text = request.json['articleText']
        summarized_text = huggingFace(article_text)
        return jsonify({'summarized_text': summarized_text})

if __name__ == '__main__':
    app.run(debug=True)



