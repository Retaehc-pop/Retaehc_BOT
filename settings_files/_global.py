import os

SETTINGS_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SETTINGS_DIR)
DATA_DIR = os.path.join(ROOT_DIR, 'data')


DISCORD_BOT_TOKEN = "BOTTOKEN"

REDDIT_APP_ID = "APPID"
REDDIT_APP_SECRET = "APPID"

REDDIT_ENABLED_MEME_SUBREDDITS = [
    'funny',
    'memes',
]
REDDIT_ENABLED_NSFW_SUBREDDITS = [
    'wtf'
]

MODERATOR_ROLE_NAME = "Moderator"
