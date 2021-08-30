import os

SETTINGS_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SETTINGS_DIR)
DATA_DIR = os.path.join(ROOT_DIR, 'data')


DISCORD_BOT_TOKEN = "ODY2MTg0Nzg5ODExMzk2NjQ5.YPO3cg.tjbcL28Jw_g_TT7hhA_fsAMSfyY"

REDDIT_APP_ID = "BU7hiKqPsykKA92llIH1OQ"
REDDIT_APP_SECRET = "qmLjnJ6m5gceOogoiRQR2byc3ehr1w"

REDDIT_ENABLED_MEME_SUBREDDITS = [
    'funny',
    'memes',
]
REDDIT_ENABLED_NSFW_SUBREDDITS = [
    'wtf'
]

MODERATOR_ROLE_NAME = "Moderator"
