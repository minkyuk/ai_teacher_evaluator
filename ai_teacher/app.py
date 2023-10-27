from flask import Flask, request, render_template
from questions import questions
from process import ask_question, evaluate_feedback, give_feedback
import time
app = Flask(__name__)

api_key = None

def process_sentence(sentence):
    # Add your sentence processing logic here
    return sentence.upper()

@app.route('/', methods=['GET', 'POST'])
def index():

    global api_key

    if request.method == 'POST':
    	if 'openAI_api_key' in request.form:
    		api_key = request.form.get('openAI_api_key')
    		return render_template('index.html', questions=questions)
    	else:
            selected_sentence = request.form.get('sentence')
            student_response = ask_question(selected_sentence, api_key)
            teacher_feedback = give_feedback(selected_sentence, student_response, api_key)
            feedback_evaluation, suggestion = evaluate_feedback(selected_sentence, student_response, teacher_feedback, api_key)

            return render_template('index.html',
            	                    questions=questions,
            	                    selected_sentence=selected_sentence,
                                    student_response=student_response,
                                    teacher_feedback=teacher_feedback,
                                    feedback_evaluation=feedback_evaluation,
                                    suggestion=suggestion
                                    )
    else:
        return render_template('index.html', questions=questions)

if __name__ == '__main__':
    app.run(debug=True)