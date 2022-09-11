import sseclient
import json

class ItemEvent(object):
    def __init__(self, url:str, username:str = None, password:str = None):
        if url == "https://myopenhab.org" or url == "https://myopenhab.org/":
            self.url = "https://myopenhab.org"
        self.url:str = url
        self.username:str = username
        self.password:str = password

    def __callURL(self, url:str):
        if self.username is not None and self.password is not None:
            return sseclient.SSEClient(url, auth=(self.username, self.password))
        else:
            return sseclient.SSEClient(url)

    def allEvents(self):
        return self.__callURL(self.url + f"/rest/events?topics=openhab/items")

    def ItemAddedEvent(self, itemName:str):
        return self.__callURL(self.url + f"/rest/events?topics=openhab/items/{itemName}/added")

    def ItemRemovedEvent(self, itemName:str):
        return self.__callURL(self.url + f"/rest/events?topics=openhab/items/{itemName}/removed")

    def ItemUpdatedEvent(self, itemName:str):
        return self.__callURL(self.url + f"/rest/events?topics=openhab/items/{itemName}/updated")

    def ItemCommandEvent(self, itemName:str):
        return self.__callURL(self.url + f"/rest/events?topics=openhab/items/{itemName}/command")

    def ItemStateEvent(self, itemName:str):
        return self.__callURL(self.url + f"/rest/events?topics=openhab/items/{itemName}/state")

    def ItemStatePredictedEvent(self, itemName:str):
        return self.__callURL(self.url + f"/rest/events?topics=openhab/items/{itemName}/statepredicted")

    def ItemStateChangedEvent(self, itemName:str):
        return self.__callURL(self.url + f"/rest/events?topics=openhab/items/{itemName}/statechanged")

    def GroupItemStateChangedEvent(self, itemName:str, memberName:str):
        return self.__callURL(self.url + f"/rest/events?topics=openhab/items/{itemName}/{memberName}/statechanged")

# Main function.
if __name__ == "__main__":
    #item_event = ItemEvent("http://<your_ip>:8080")
    item_event = ItemEvent("https://myopenhab.org", "<your_email>@<your_provider>", "<password>")
    events =  item_event.allEvents()

    for event in events:
        try:
            print(json.loads(event.data))
        except json.decoder.JSONDecodeError:
            print("Event could not be converted to JSON")
