# Smile Bot
A bot for discord that tracks "smile" reactions.

## Usage
Put your bot token in `.env` like
```bash
#.env
TOKEN=<BOT_TOKEN>
```

### Docker
```
docker build -t jordanbertasso/smile-bot .
docker run -it jordanbertasso/smile-bot
```

### Python
```
pip install -r requirements.txt
python -m bot
```
