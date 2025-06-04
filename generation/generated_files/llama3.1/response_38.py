import os
import logging
from slack import WebClient, MessagePayload, Attachment
from slack.errors import SlackApiError

SLACK_API_TOKEN = os.environ.get('SLACK_API_TOKEN')
client = WebClient(token=SLACK_API_TOKEN)

def handle_message(event):
    channel = event['channel']
    message = event['text']

    # Post automated response to the same channel
    attachment = Attachment(
        title='Hello from Python!',
        text='You said: {}'.format(message),
        color='#36a64f'
    )
    payload = MessagePayload(text='Welcome to our channel!', attachments=[attachment])
    try:
        client.chat_postMessage(channel=channel, message=payload)
    except SlackApiError as e:
        print(f'Slack API error occurred while posting message: {e}')

def listen_for_messages():
    # Listen for messages in a specific channel
    incoming_webhook_url = 'https://example.com/slack-webhook'
    client.listen(incoming_webhook_url, on_message=handle_message)

if __name__ == '__main__':
    listen_for_messages()