import os
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Temporary in-memory log to save user feedback responses
feedback_log = []

# Mock AI engine to return a response based on the engineered prompt structure
def mock_ai_response(engineered_prompt, user_input=""):
    """
    Simulates an AI model processing a specifically designed prompt frame.
    In a real app, you would pass this string directly to `openai.ChatCompletion`.
    """
    if "FACTUAL_QA" in engineered_prompt:
        if "france" in user_input.lower():
            return "The capital of France is Paris. It is famous for the Eiffel Tower and art museums."
        return f"[Factual Answer Mode] Here is information regarding your query: '{user_input}'."
        
    elif "SUMMARIZE" in engineered_prompt:
        clean_text = user_input[:40] if len(user_input) > 40 else user_input
        return f"[Summary Engine] Key Insight: This text addresses context surrounding '{clean_text}...'"
        
    elif "CREATIVE" in engineered_prompt:
        return f"[Creative AI] Once upon a time, an amazing journey began with: '{user_input}'. The end."
        
    return "Feature selected, but no prompt logic matched."

@app.route('/', methods=['GET', 'POST'])
def index():
    response_text = None
    selected_prompt = None
    
    if request.method == 'POST':
        # Grab variables submitted via the HTML front-end form
        function_type = request.form.get('function_type')
        prompt_style = request.form.get('prompt_style')
        user_raw_input = request.form.get('user_input', '')
        
        # 2. Prompt Design Requirement: Constructing 3 variations for 3 functions
        if function_type == "qa":
            if prompt_style == "short":
                selected_prompt = f"SYSTEM: Answer directly.\nUSER: {user_raw_input} [TAG: FACTUAL_QA]"
            elif prompt_style == "detailed":
                selected_prompt = f"SYSTEM: You are a scholar. Provide context, history, and definitions.\nUSER: {user_raw_input} [TAG: FACTUAL_QA]"
            else:
                selected_prompt = f"SYSTEM: Bullet-point facts only.\nUSER: {user_raw_input} [TAG: FACTUAL_QA]"
                
        elif function_type == "summary":
            if prompt_style == "short":
                selected_prompt = f"SYSTEM: Condense into one short line.\nUSER: {user_raw_input} [TAG: SUMMARIZE]"
            elif prompt_style == "detailed":
                selected_prompt = f"SYSTEM: Breakdown using main claims, arguments, and summaries.\nUSER: {user_raw_input} [TAG: SUMMARIZE]"
            else:
                selected_prompt = f"SYSTEM: Explain like I am 5 years old.\nUSER: {user_raw_input} [TAG: SUMMARIZE]"
                
        elif function_type == "creative":
            if prompt_style == "short":
                selected_prompt = f"SYSTEM: Write a whimsical poem.\nUSER: {user_raw_input} [TAG: CREATIVE]"
            elif prompt_style == "detailed":
                selected_prompt = f"SYSTEM: Write a gothic horror story setting.\nUSER: {user_raw_input} [TAG: CREATIVE]"
            else:
                selected_prompt = f"SYSTEM: Generate a fast-paced screenplay scene.\nUSER: {user_raw_input} [TAG: CREATIVE]"
        
        # Query our prompt processor
        if selected_prompt:
            response_text = mock_ai_response(selected_prompt, user_raw_input)
            
    return render_template('index.html', response_text=response_text, selected_prompt=selected_prompt)

@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    # 4. Feedback Loop requirement managed dynamically via JavaScript fetch
    data = request.get_json() or {}
    helpful = data.get('helpful')
    prompt_used = data.get('prompt')
    
    log_entry = {"prompt": prompt_used, "helpful": helpful}
    feedback_log.append(log_entry)
    print(f"[FEEDBACK LOGGED]: {log_entry}") # Visible in hosting platform live server console
    
    return jsonify({"status": "success", "message": "Feedback recorded!"})

if __name__ == '__main__':
    app.run(debug=True)
