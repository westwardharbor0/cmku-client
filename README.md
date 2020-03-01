# cmku-client
Small library to access data from www.cmku.cz in your Python code <br>
<strong>Note</strong>: all actions are only half year to the future
#Features
- get latest dog actions from source
- get breeds list 
- get actions types
- cache already loaded results
# Examples
### Enable cache
Enable caching to load all results only ones
```Python
from cmku_client.client import CMKUClient
client = CMKUClient(cache=True)
```
### Getting future actions
Get a list of nearest actions
```Python
from cmku_client.client import CMKUClient
client = CMKUClient()
actions = client.load_actions()
print(actions)
```
### Getting breeds
Get a list of all breeds
```Python
from cmku_client.client import CMKUClient
client = CMKUClient()
breeds = client.load_breeds()
print(breeds)
```
### Getting actions in date interval
Get a list of actions that are in a date interval
```Python
from datetime import datetime
from cmku_client.client import CMKUClient
client = CMKUClient()
actions = client.load_by_date(date_from=datetime(2020, 1, 1), date_to=datetime(2020, 5, 1))
print(actions)
```
### Getting action detail
Get a action detail
```Python
from cmku_client.client import CMKUClient
client = CMKUClient()
action = client.load_action_detail(action_id=666)
print(action)
```
### Getting actions with name
Get a list of actions which name contains string or substr
```Python
from cmku_client.client import CMKUClient
client = CMKUClient()
action = client.load_by_name(name="oblastní")
print(action)
```