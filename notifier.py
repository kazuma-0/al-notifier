import requests, os
from discord_webhook import DiscordWebhook
from time import sleep as wait

userTOKEN = os.environ["userToken"]
userID = os.environ["userID"]
#userName = os.environ["userName"]
def headerReturn():
    return {
        "Authorization": "Bearer " + userTOKEN,
        "Content-Type": "application/json",
        "Accept": "application/json",
    }


def queryReturn(): #too lazy to add variables for username, should set it later.
    return {
        "query": """query{
            User(name:"kazuma"){ 
            unreadNotificationCount
        }
    }""",
    }


def sendWebhook(content):
    hook = DiscordWebhook(
        url=os.environ["webhookLink"], content=content, username="Anilist"
    )
    hook.execute()


currentCount = 0


def sendRequest(count):
    global currentCount
    requestObject = requests.post(
        "https://graphql.anilist.co", json=queryReturn(), headers=headerReturn()
    )  # object to recieve requests.
    presentCount = requestObject.json()["data"]["User"]["unreadNotificationCount"]
    if presentCount != currentCount:
        sendWebhook(
            f"<@!{userID}> You have {presentCount} unread notifications, {count}'th request."
        )
        currentCount = presentCount
    else:
        pass


count = 0
while True:
    count += 1
    sendRequest(count)
    wait(60)
