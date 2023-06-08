# from flask import Flask, render_template, request, jsonify
# from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM

# app = Flask(__name__)

# def huggingFace(text, model_name):
#     if model_name == 'short':
#         tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
#         model = AutoModelForSeq2SeqLM.from_pretrained("bert-base-uncased")
#     elif model_name == 'long':
#         tokenizer = AutoTokenizer.from_pretrained("facebook/bart-base")
#         model = AutoModelForSeq2SeqLM.from_pretrained("facebook/bart-base")

#     summarizer = pipeline("summarization", tokenizer=tokenizer, model=model)

#     summary = summarizer(text, max_length=250, min_length=50, do_sample=False)[0]['summary_text']

#     return summary

# @app.route('/')
# def home():
#     return render_template('summary.html')

# @app.route('/summary', methods=['POST'])
# def summarize():
#     if request.method == 'POST':
#         article_text = request.json['articleText']
#         summary_length = request.json['summaryLength']

#         if summary_length == 'short':
#             summarized_text = huggingFace(article_text, 'short')
#         elif summary_length == 'long':
#             summarized_text = huggingFace(article_text, 'long')
#         else:
#             return jsonify({'error': 'Invalid summary length option'})

#         return jsonify({'summarized_text': summarized_text})

# if __name__ == '__main__':
#     app.run(debug=True)

from flask import Flask, render_template, request, jsonify
from transformers import pipeline

app = Flask(__name__)

def huggingFace(text, model_name):
    # Load the text summarization pipeline
    if model_name == 'short':
        summarizer = pipeline("summarization", model="bert-base-uncased")
    elif model_name == 'long':
        summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

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
        summary_length = request.json['summaryLength']

        if summary_length == 'short':
            summarized_text = huggingFace(article_text, 'short')
        elif summary_length == 'long':
            summarized_text = huggingFace(article_text, 'long')
        else:
            summarized_text = ''

        return jsonify({'summarized_text': summarized_text})

if __name__ == '__main__':
    app.run(debug=True)








# # from flask import Flask, render_template, request, jsonify
# # from transformers import pipeline

# # app = Flask(__name__)

# # def huggingFace(text):
# #     # Load the text summarization pipeline
# #     summarizer = pipeline("summarization")

# #     # Split the text into chunks of maximum 600 words
# #     max_words = 600
# #     chunks = [text[i:i+max_words] for i in range(0, len(text), max_words)]

# #     summaries = []
# #     # Process each chunk and generate a summary
# #     for chunk in chunks:
# #         summary = summarizer(chunk, max_length=250, min_length=50, do_sample=False)[0]["summary_text"]
# #         summaries.append(summary)

# #     # Combine the summaries into a single string
# #     combined_summary = " ".join(summaries)

# #     # Return the combined summary
# #     return combined_summary

# # @app.route('/')
# # def home():
# #     return render_template('summary.html')

# # @app.route('/summary', methods=['POST'])
# # def summary():
# #     if request.method == 'POST':
# #         article_text = request.json['articleText']
# #         summarized_text = huggingFace(article_text)
# #         return jsonify({'summarized_text': summarized_text})

# # if __name__ == '__main__':
# #     app.run(debug=True)



