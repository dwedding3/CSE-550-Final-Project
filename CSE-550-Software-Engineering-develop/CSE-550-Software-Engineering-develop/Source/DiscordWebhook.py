from discord_webhook import DiscordWebhook,DiscordEmbed

class DiscordWebHook:
    webhookURL=None
    def __init__(self,URL,userName,content):
        self.webhookURL = DiscordWebhook(url=URL,username=userName,content=content)
        self.webhookURL.execute()

        


