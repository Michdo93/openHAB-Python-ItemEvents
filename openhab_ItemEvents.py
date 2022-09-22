import requests
import json

class ItemEvent(object):
    def __init__(self, url:str, username:str = None, password:str = None):
        self.url:str = url
        self.username:str = username
        self.password:str = password
        self.session = requests.Session()
        
        if self.username is not None and self.password is not None:
            self.auth = (self.username, self.password)
            self.session.auth = self.auth
        else:
            self.auth = None
            self.session.auth = None

        self.__login()
        
    def __login(self):
        if self.url == "https://myopenhab.org" or self.url == "https://myopenhab.org/":
            self.url = "https://myopenhab.org"
            self.isCloud = True
            url = self.url
        else:
            if self.url[-1] == "/":
                self.url = self.url[:-1]
            self.isCloud = False
            url = self.url + "/rest"

        try:
            login_response = self.session.get(url, auth=self.auth, timeout=8)
            login_response.raise_for_status()

            if login_response.ok or login_response.status_code == 200:
                self.isLoggedIn = True
        except requests.exceptions.HTTPError as errh:
            print(errh)
        except requests.exceptions.ConnectionError as errc:
            print(errc)
        except requests.exceptions.Timeout as errt:
            print(errt)
        except requests.exceptions.RequestException as err:
            print(err)

    def __callURL(self, url:str):
        if self.username is not None and self.password is not None:
            return self.session.get(url, auth=self.auth, stream=True)
        else:
            return self.session.get(url, stream=True)

    def ItemEvent(self):
        return self.__callURL(self.url + f"/rest/events?topics=openhab/items")

    def ItemAddedEvent(self, itemName:str = "*"):
        return self.__callURL(self.url + f"/rest/events?topics=openhab/items/{itemName}/added")

    def ItemRemovedEvent(self, itemName:str = "*"):
        return self.__callURL(self.url + f"/rest/events?topics=openhab/items/{itemName}/removed")

    def ItemUpdatedEvent(self, itemName:str = "*"):
        return self.__callURL(self.url + f"/rest/events?topics=openhab/items/{itemName}/updated")

    def ItemCommandEvent(self, itemName:str = "*"):
        return self.__callURL(self.url + f"/rest/events?topics=openhab/items/{itemName}/command")

    def ItemStateEvent(self, itemName:str = "*"):
        return self.__callURL(self.url + f"/rest/events?topics=openhab/items/{itemName}/state")

    def ItemStatePredictedEvent(self, itemName:str = "*"):
        return self.__callURL(self.url + f"/rest/events?topics=openhab/items/{itemName}/statepredicted")

    def ItemStateChangedEvent(self, itemName:str = "*"):
        return self.__callURL(self.url + f"/rest/events?topics=openhab/items/{itemName}/statechanged")

    def GroupItemStateChangedEvent(self, itemName:str, memberName:str):
        return self.__callURL(self.url + f"/rest/events?topics=openhab/items/{itemName}/{memberName}/statechanged")

# Main function.
if __name__ == "__main__":
    item_event = ItemEvent("http://<your_ip>:8080")
    #item_event = ItemEvent("https://myopenhab.org", "<your_email>@<your_provider>", "<password>")
    response = item_event.ItemEvent()
    
    with response as events:
        for line in events.iter_lines():
            line = line.decode()

            if "data" in line:
                line = line.replace("data: ", "")

                try:
                    data = json.loads(line)
                    print(data)
                except json.decoder.JSONDecodeError:
                    print("Event could not be converted to JSON")
