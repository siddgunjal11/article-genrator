import os
from flask import Flask, render_template, request, jsonify
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/generate', methods=['POST'])
def generate():
    if request.method == 'POST':
        # Get the API key from environment variable
        api_key = os.getenv("OPENAI_API_KEY")

        # Initialize the LLM with the new API key
        llm = OpenAI(api_key=api_key, model="gpt-3.5-turbo", temperature=0.3)
        prompt_template = PromptTemplate.from_template("Generate a blog on title {title}")
        chain = LLMChain(llm=llm, prompt=prompt_template)

        data = request.get_json()
        title = data.get('title')

        try:
            output = chain.run({"title": title})
            return jsonify({"output": output})
        except OpenAI.error.RateLimitError:
            return jsonify({"error": "API rate limit exceeded. Please try again later."}), 429

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81)



