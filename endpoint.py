from fastapi import FastAPI, Form
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from src.main import generate_meme
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
slack_client = WebClient(token=SLACK_BOT_TOKEN)

@app.post("/")
async def meme_slash_command(
    text: str = Form(...),
    response_url: str = Form(...),
    channel_id: str = Form(...)
):
    try:
        # Réponse immédiate à Slack
        slack_client.chat_postMessage(
            channel=channel_id,
            text="🎭 Génération du mème en cours..."
        )

        # Génération du mème
        meme_path = generate_meme(text)

        # Upload du fichier via Slack SDK v2
        try:
            slack_client.files_upload_v2(
                channel=channel_id,
                initial_comment=f"🎭 Mème généré pour: *{text}*",
                file=meme_path
            )
        except SlackApiError as e:
            error = e.response["error"]
            print(f"Erreur Slack API: {e.response}")
            if error == "not_in_channel":
                slack_client.chat_postEphemeral(
                    channel=channel_id,
                    text="❌ Je ne suis pas dans ce canal. Utilisez `/invite @MemeMachine` pour m'y ajouter.",
                    user=os.environ.get("SLACK_USER_ID", "")
                )
            else:
                slack_client.chat_postMessage(
                    channel=channel_id,
                    text=f"❌ Erreur lors de l'envoi du mème: {error}"
                )
            return {"text": ""}

        # Confirmation
        slack_client.chat_postMessage(
            channel=channel_id,
            text="✅ Mème généré avec succès !"
        )
        return {"text": ""}

    except Exception as e:
        print(f"Erreur générale: {str(e)}")
        slack_client.chat_postMessage(
            channel=channel_id,
            text=f"❌ Erreur lors de la génération du mème: {str(e)}"
        )
        return {"text": ""}
