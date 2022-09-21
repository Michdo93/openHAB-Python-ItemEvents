# openHAB Python ItemEvents
A simple program for accessing the ItemEvents of openHAB by using the server-sent events from the openHAB REST API. Whether via the cloud or locally.

`Server-Sent Events` (`SSE`) is a server push technology enabling a client to receive automatic updates from a server via an `HTTP` connection, and describes how servers can initiate data transmission towards clients once an initial client connection has been established. They are commonly used to send message updates or continuous data streams to a browser client and designed to enhance native, cross-browser streaming through a `JavaScript API` called `EventSource`, through which a client requests a particular `URL` in order to receive an event stream. The `EventSource API` is standardized as part of `HTML5` by the `WHATWG`. The mime type for `SSE` is `text/event-stream`.

The openHAB Item Events can only received by using `SSE`!

https://github.com/Michdo93/openHAB-Python-ItemEvents

You can get more informations about the [ItemEvents here](https://www.openhab.org/docs/developer/utils/events.html#item-events).

To test the ItemEvents, you can play around a bit using [CRUD](https://github.com/Michdo93/openhab_python_crud).

## Preparation

You have to install following before you can use this python script:

```
python3 -m pip install sseclient
```

## Installation

Go to your path where you want to have the python file:

```
cd /path/to/file
wget https://raw.githubusercontent.com/Michdo93/openHAB-Python-ItemEvents/main/openhab_ItemEvents.py
sudo chmod +x openhab_ItemEvents.py
```

## Usage


The `<base_url>` could be the ip address plus port of your local openHAB instance (`<ip_address>:<port>`) or `myopenhab.org`. Of course if you are using `http` on your local instance you have to replace `https` with `http`.

|  Event | 	Description | 	URL | 
|:-------------:| :-----:| :-----:|
| ItemAddedEvent |	An item has been added to the item registry. |	curl "https://<base_url>/rest/events?topics=openhab/items/{itemName}/added" |
| ItemRemovedEvent |	An item has been removed from the item registry. | curl	"https://<base_url>/rest/events?topics=openhab/items/{itemName}/removed" |
| ItemUpdatedEvent |	An item has been updated in the item registry. |	curl "https://<base_url>/rest/events?topics=openhab/items/{itemName}/updated" |
| ItemCommandEvent |	A command is sent to an item via a channel. |	curl "https://<base_url>/rest/events?topics=openhab/items/{itemName}/command" |
| ItemStateEvent |	The state of an item is updated. |	curl "https://<base_url>/rest/events?topics=openhab/items/{itemName}/state" |
| ItemStatePredictedEvent |	The state of an item predicted to be updated. |	curl "https://<base_url>/rest/events?topics=openhab/items/{itemName}/statepredicted" |
| ItemStateChangedEvent |	The state of an item has changed. |	curl "https://<base_url>/rest/events?topics=openhab/items/{itemName}/statechanged" |
| GroupItemStateChangedEvent |	The state of a group item has changed through a member. |	curl "https://<base_url>/rest/events?topics=openhab/items/{itemName}/{memberName}/statechanged" |

### Create connection to the openHAB Cloud (as example myopenhab.org)

If you want to create a connection to the `openHAB Cloud` you have to run:

```
item_event = ItemEvent("https://myopenhab.org", "<your_email>@<your_provider>", "<email_password>")
```

Please make sure to replace `<your_email>@<your_provider>` with your email address and `<email_password>` with your password that you used for your openHAB Cloud account.

### Create connection to your local openHAB instance

If you want to create a connection to your local `openHAB` instance you have to replace `<username>` and `<password>` with the username and password of your local openHAB account:

```
item_event = ItemEvent("http://<your_ip>:8080", "<username>", "<password>")
```

Maybe there is no username and password needed:

```
item_event = ItemEvent("http://<your_ip>:8080")
```

### Retrieving all Item Events

You can retrieve all `Events` from all `Items` by using:

```
events =  item_event.ItemEvent()
```

You will get a `list` of `dictionaries` (`dict`) in `JSON` format. So you have to loop through it:

```
for event in events:
    try:
        print(json.loads(event.data))
    except json.decoder.JSONDecodeError:
        print("Event could not be converted to JSON")
```

Of course you can checkt if it is the type `dict`:

```
for event in events:
    try:
        print(type(json.loads(event.data)))
    except json.decoder.JSONDecodeError:
        print("Event could not be converted to JSON")
```

It is not possible not to use a loop for events, because on each change the server pushes. The created loop receives each new event as soon as it is pushed. If no new event is triggered on the server, there is no new iteration.

For all ItemEvents, therefore, there must be both a continuous loop and the data must be converted from `JSON` to a `dict`!

Of course, you can also access individual elements of the `dict`:

```
for event in events:
    try:
        data = json.loads(event.data)
        
        event_topic = data.get("topic")
        event_item_name = data.split("/")[2]
        event_payload = eval(data.get("payload"))
        event_type = data.get("type")

        print(event_topic)
        print(event_item_name)
        print(event_payload)
        print(event_type)
    except json.decoder.JSONDecodeError:
        print("Event could not be converted to JSON")
```

However, `ItemEvents` do not provide information about which type an `Item` has. An `ItemEvent` contains only the changes for an `Item` that are described by an `Event`. But you can also use the `ItemEvent` to query an `Item`. This does not require `SSE`, but a simple `REST` request:

```
for event in events:
    try:
        data = json.loads(event.data)
        
        event_topic = data.get("topic")
        event_item_name = data.split("/")[2]
        event_payload = eval(data.get("payload"))
        event_type = data.get("type")

        print(event_topic)
        print(event_item_name)
        print(event_payload)
        print(event_type)
        
        try:
            item_response = requests.get(<base_url> + "/items/" + event_item_name, auth=auth, headers=headers, timeout=8)
            item_response.raise_for_status()

            if item_response.ok or item_response.status_code == 200:
                item = json.loads(item_response.text)
                item_link = item.get("link")
                item_state = item.get("state")
                item_state_description = item.get("stateDescription")
                item_editable = item.get("editable")
                item_type = item.get("type")
                item_name = item.get("name")
                item_label = item.get("label")
                item_group_names = item.get("groupNames")

                print(item_type)
                print(item_name)
                print(item_state)
        except requests.exceptions.HTTPError as errh:
            print(errh)
        except requests.exceptions.ConnectionError as errc:
            print(errc)
        except requests.exceptions.Timeout as errt:
            print(errt)
        except requests.exceptions.RequestException as err:
            print(err)
    except json.decoder.JSONDecodeError:
        print("Event could not be converted to JSON")
```

What is missing in this pseudo code now is, `<base_url>`. You could use this for the cloud or for the local instance.

Since you get all ItemEvents` for all `Items`, it is recommended to make a case distinction:

```
for event in events:
    data = event.data

    try:
        decoded = json.loads(data)
        event_topic = decoded.get("topic")
        event_item_name = event_topic.split("/")[2]
        event_payload = eval(decoded.get("payload"))
        event_type = decoded.get("type")
        
        if(event_type == "ItemAddedEvent"):
            # your code
        elif(event_type == "ItemRemovedEvent"):
            # your code
        elif(event_type == "ItemUpdatedEvent"):
            # your code
        elif(event_type == "ItemCommandEvent"):
            # your code
        elif(event_type == "ItemStateEvent"):
            event_item_type = event_payload.get("type")
            event_item_value = event_payload.get("value")
            print(event_item_type)
            print(event_item_value)
        elif(event_type == "ItemStatePredictedEvent"):
            # your code
        elif(event_type == "ItemStateChangedEvent"):
            event_item_type = event_payload.get("type")
            event_item_value = event_payload.get("value")
            event_item_old_type = event_payload.get("oldType")
            event_item_old_value = event_payload.get("oldValue")
            print(event_item_type)
            print(event_item_value)
            print(event_item_old_type)
            print(event_item_old_value)
        elif(event_type == "GroupItemStateChangedEvent"):
            # your code
    except (json.JSONDecodeError, KeyboardInterrupt):
        pass
    except Exception:
        pass    
```

### Retrieving ItemAddedEvent of an Item

The function requires the name of the item as input parameter:

```
events =  item_event.ItemAddedEvent("testItem")
```

Finally, in the end you have to remember that you need to convert from JSON and you need a loop. You get again a `dict`:

```
for event in events:
    try:
        print(json.loads(event.data))
    except json.decoder.JSONDecodeError:
        print("Event could not be converted to JSON")
```

### Retrieving ItemAddedEvent of all Items

The function does not require a parameter:

```
events =  item_event.ItemAddedEvent()
```

Alternatively you can pass a `"*"`:

```
events =  item_event.ItemAddedEvent("*")
```

Finally, in the end you have to remember that you need to convert from JSON and you need a loop. You get again a `dict`:

```
for event in events:
    try:
        print(json.loads(event.data))
    except json.decoder.JSONDecodeError:
        print("Event could not be converted to JSON")
```

### Retrieving ItemRemovedEvent of an Item

The function requires the name of the item as input parameter:

```
events =  item_event.ItemRemovedEvent("testItem")
```

Finally, in the end you have to remember that you need to convert from JSON and you need a loop. You get again a `dict`:

```
for event in events:
    try:
        print(json.loads(event.data))
    except json.decoder.JSONDecodeError:
        print("Event could not be converted to JSON")
```

### Retrieving ItemRemovedEvent of all Items

The function does not require a parameter:

```
events =  item_event.ItemRemovedEvent()
```

Alternatively you can pass a `"*"`:

```
events =  item_event.ItemRemovedEvent("*")
```

Finally, in the end you have to remember that you need to convert from JSON and you need a loop. You get again a `dict`:

```
for event in events:
    try:
        print(json.loads(event.data))
    except json.decoder.JSONDecodeError:
        print("Event could not be converted to JSON")
```

### Retrieving ItemUpdatedEvent of an Item

The function requires the name of the item as input parameter:

```
events =  item_event.ItemUpdatedEvent("testItem")
```

Finally, in the end you have to remember that you need to convert from JSON and you need a loop. You get again a `dict`:

```
for event in events:
    try:
        print(json.loads(event.data))
    except json.decoder.JSONDecodeError:
        print("Event could not be converted to JSON")
```

### Retrieving ItemUpdatedEvent of all Items

The function does not require a parameter:

```
events =  item_event.ItemUpdatedEvent()
```

Alternatively you can pass a `"*"`:

```
events =  item_event.ItemUpdatedEvent("*")
```

Finally, in the end you have to remember that you need to convert from JSON and you need a loop. You get again a `dict`:

```
for event in events:
    try:
        print(json.loads(event.data))
    except json.decoder.JSONDecodeError:
        print("Event could not be converted to JSON")
```

### Retrieving ItemCommandEvent of an Item

The function requires the name of the item as input parameter:

```
events =  item_event.ItemCommandEvent("testItem")
```

Finally, in the end you have to remember that you need to convert from JSON and you need a loop. You get again a `dict`:

```
for event in events:
    try:
        print(json.loads(event.data))
    except json.decoder.JSONDecodeError:
        print("Event could not be converted to JSON")
```

### Retrieving ItemCommandEvent of all Items

The function does not require a parameter:

```
events =  item_event.ItemCommandEvent()
```

Alternatively you can pass a `"*"`:

```
events =  item_event.ItemCommandEvent("*")
```

Finally, in the end you have to remember that you need to convert from JSON and you need a loop. You get again a `dict`:

```
for event in events:
    try:
        print(json.loads(event.data))
    except json.decoder.JSONDecodeError:
        print("Event could not be converted to JSON")
```

### Retrieving ItemStateEvent of an Item

The function requires the name of the item as input parameter:

```
events =  item_event.ItemStateEvent("testItem")
```

Finally, in the end you have to remember that you need to convert from JSON and you need a loop. You get again a `dict`:

```
for event in events:
    try:
        print(json.loads(event.data))
    except json.decoder.JSONDecodeError:
        print("Event could not be converted to JSON")
```

### Retrieving ItemStateEvent of all Items

The function does not require a parameter:

```
events =  item_event.ItemStateEvent()
```

Alternatively you can pass a `"*"`:

```
events =  item_event.ItemStateEvent("*")
```

Finally, in the end you have to remember that you need to convert from JSON and you need a loop. You get again a `dict`:

```
for event in events:
    try:
        print(json.loads(event.data))
    except json.decoder.JSONDecodeError:
        print("Event could not be converted to JSON")
```

### Retrieving ItemStatePredictedEvent of an Item

The function requires the name of the item as input parameter:

```
events =  item_event.ItemStatePredictedEvent("testItem")
```

Finally, in the end you have to remember that you need to convert from JSON and you need a loop. You get again a `dict`:

```
for event in events:
    try:
        print(json.loads(event.data))
    except json.decoder.JSONDecodeError:
        print("Event could not be converted to JSON")
```

### Retrieving ItemStatePredictedEvent of all Items

The function does not require a parameter:

```
events =  item_event.ItemStatePredictedEvent()
```

Alternatively you can pass a `"*"`:

```
events =  item_event.ItemStatePredictedEvent("*")
```

Finally, in the end you have to remember that you need to convert from JSON and you need a loop. You get again a `dict`:

```
for event in events:
    try:
        print(json.loads(event.data))
    except json.decoder.JSONDecodeError:
        print("Event could not be converted to JSON")
```

### Retrieving ItemStateChangedEvent of an Item

The function requires the name of the item as input parameter:

```
events =  item_event.ItemStateChangedEvent("testItem")
```

Finally, in the end you have to remember that you need to convert from JSON and you need a loop. You get again a `dict`:

```
for event in events:
    try:
        print(json.loads(event.data))
    except json.decoder.JSONDecodeError:
        print("Event could not be converted to JSON")
```

### Retrieving ItemStateChangedEvent of all Items

The function does not require a parameter:

```
events =  item_event.ItemStateChangedEvent()
```

Alternatively you can pass a `"*"`:

```
events =  item_event.ItemStateChangedEvent("*")
```

Finally, in the end you have to remember that you need to convert from JSON and you need a loop. You get again a `dict`:

```
for event in events:
    try:
        print(json.loads(event.data))
    except json.decoder.JSONDecodeError:
        print("Event could not be converted to JSON")
```

### Retrieving GroupItemStateChangedEvent of an Item

The function requires the names of the item and of the member as input parameter:

```
events =  item_event.GroupItemStateChangedEvent("testItem", "testGroup")
```

Finally, in the end you have to remember that you need to convert from JSON and you need a loop. You get again a `dict`:

```
for event in events:
    try:
        print(json.loads(event.data))
    except json.decoder.JSONDecodeError:
        print("Event could not be converted to JSON")
```
