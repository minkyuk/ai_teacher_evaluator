import openai
import time

GPT_MODEL = "text-davinci-003"

# Teacher Role
def give_feedback(question, response, api_key):
    openai.api_key = api_key

    find_problem_prompt = f"Identify factual and grammatical errors or incomplete sentences in the response: {response} \
                            regarding a question: {question}."
    suggestion_prompt = f" After evaluating the response, suggest a response with improvement."

    try:
        feedback = openai.Completion.create(
            engine=GPT_MODEL,
            prompt=find_problem_prompt,
            max_tokens=1000,
        )
        return feedback.choices[0].text.strip()

    except openai.error.RateLimitError as e:

   	    # Handle rate limit error by waiting and retrying
        retry_after_seconds = int(e.headers.get("Retry-After", 10))
        time.sleep(retry_after_seconds)
        return give_feedback(question, response, api_key)  # Retry the API call


# Evaluator Role
def evaluate_feedback(question, response, feedback, api_key):
    openai.api_key = api_key

    evaluation_prompt = f"Assess the reasonability and fact-check on the feedback: \
                      {feedback} to the following response: {response}, \
                      to the question: {question}?"
    quality_evaluation_prompt = f"Assess the reasonability critifically and fact-check of the feedback: {feedback} \
                                  on the reponse: {response} regarding the question: {question}"
    generic_evaluation_prompt = f"is the feedback: {response} appropriate and correct for the response: {response} \
                                  regarding question: {question}?"
    suggestion_prompt = f" Give one improved suggestion for the feedback."
    try:
        evaluation = openai.Completion.create(
            engine=GPT_MODEL,
            prompt=generic_evaluation_prompt,
            max_tokens=1000,
        )
        suggestion = openai.Completion.create(
            engine=GPT_MODEL,
            prompt=generic_evaluation_prompt+suggestion_prompt,
            max_tokens=1000,
        )
        return evaluation.choices[0].text.strip(), suggestion.choices[0].text.strip()

    except openai.error.RateLimitError as e:

        # Handle rate limit error by waiting and retrying
        retry_after_seconds = int(e.headers.get("Retry-After", 10))
        time.sleep(retry_after_seconds)
        return evaluate_feedback(question, response, feedback, api_key)  # Retry the API call


# Student Role
def ask_question(question, api_key):
    openai.api_key = api_key
    my_question = question

    bug_added_prompt = f"Have an incorrect response to question: '{my_question}', \
    			by change the response to include inaccurate facts, or to fail to directly answer the question, \
                or to use incomplete sentences."

    try:
        # Generate a response from ChatGPT
        response = openai.Completion.create(
            engine=GPT_MODEL,
            prompt=bug_added_prompt,
            max_tokens=1500,
        )

        # Extract and return the answer from the response
        response = response.choices[0].text.strip()
        return response
    
    except openai.error.RateLimitError as e:

        # Handle rate limit error by waiting and retrying
        retry_after_seconds = int(e.headers.get("Retry-After", 10))
        time.sleep(retry_after_seconds)
        return ask_question(question, api_key)  # Retry the API call

