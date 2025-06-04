import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from slack_bolt import App

# Initialize a Web API client
slack_token = os.environ["SLACK_BOT_TOKEN"]
app = App(token=slack_token)

@app.message("hello")
def handle_message(body, say):
    user_id = body['event']['user']
    channel_id = body['event']['channel']
    try:
        response = f"Hello <@{user_id}>! How can I assist you today?"
        say(text=response, channel=channel_id)
    except SlackApiError as e:
        print(f"Error posting message: {e.response['error']}")

if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))