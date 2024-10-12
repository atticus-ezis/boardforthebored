from collections import defaultdict

dict_list = [{'class':'Sports', 'name':'George'},{'class':'Sports', 'name':'Michael'}, {'class':'Music', 'name':'Kenny'},{'class':'Festival', 'name':'Lenard'}]

#


def group_events_by_class(events):
    grouped_events = defaultdict(list)
    for event in events:
        grouped_events[event['class']].append(event)
    return grouped_events 

print(group_events_by_class(dict_list))

default_dict = group_events_by_class(dict_list)
normal_dict = dict(default_dict)
print(normal_dict)








# {
#     "Sports": [
#         {'class':'Sports', 'name':'George'},
#         {'class':'Sports', 'name':'Michael'}
#     ],
#     "Music": [
#          {'class':'Music', 'name':'Kenny'}
#     ],
#     "Festival": [
#         {'class':'Festival', 'name':'Lenard'}
#     ]
# }

# 1. get all class
# 2. group by class , assign to array