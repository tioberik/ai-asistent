import os, shelve, time
from openai import OpenAI
from flask import request
from flask_restful import Resource
from dotenv import load_dotenv


load_dotenv()
KEY = os.getenv("OPEN_AI_API_KEY")
client = OpenAI(api_key=KEY)


# --------------------------------------------------------------
# Thread management
# --------------------------------------------------------------
def check_if_thread_exists(nastavnik_id):
    with shelve.open("./db/threads_db") as threads_shelf:
        return threads_shelf.get(nastavnik_id, None)


def store_thread(nastavnik_id, thread_id):
    with shelve.open("./db/threads_db", writeback=True) as threads_shelf:
        threads_shelf[nastavnik_id] = thread_id


# --------------------------------------------------------------
# Run assistant
# --------------------------------------------------------------
def run_assistant(thread, message_body):
    # Retrieve the Assistant
    assistant = client.beta.assistants.retrieve(os.getenv("OPENAI_ASSISTANT_ID"))

    # Run the assistant
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id,
    )

    # Wait for completion
    while run.status != "completed":
        # Be nice to the API
        time.sleep(0.5)
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)

    # Retrieve the Messages
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    new_message = messages.data[0].content[0].text.value

    response = new_message

    # Save response with question in "responses.csv"
    import pandas as pd
    qa = pd.DataFrame([{'question': message_body, 'answer': repr(response),  'feedback': 'NaN'}])
    qa.to_csv('responses.csv', mode='a', header=False, index=False)


    # Retrieve answer in JSON
    return {
        "success": True,
        "response": response
    }


class AssistantApi(Resource):
    def post(self):
        try:
            data = request.json

            nastavnik_id = data.get('nastavnik_id')
            name = data.get('name')
            message_body = data.get('message_body')

            # Check if there is already a thread_id for the nastavnik_id
            thread_id = check_if_thread_exists(nastavnik_id)

            # If a thread doesn't exist, create one and store it
            if thread_id is None:
                thread = client.beta.threads.create()
                store_thread(nastavnik_id, thread.id)
                thread_id = thread.id

            # Otherwise, retrieve the existing thread
            else:
                thread = client.beta.threads.retrieve(thread_id)

            # Add message to thread
            message = client.beta.threads.messages.create(
                thread_id=thread_id,
                role="user",
                content=message_body,
            )

            # Run the assistant and get the new message
            new_message = run_assistant(thread, message_body)
            return new_message

        # error handling
        except Exception as a:
            a = str(a)
            #  Handle exception
            print(a)
            return {
                "success": False,
                "error": {
                    "statusCode": 500,
                    "message": "Something went wrong!",
                    "errorMessage": a,
                },
            }
