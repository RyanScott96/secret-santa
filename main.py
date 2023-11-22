import json
import random
import copy

token = 'name'
group = 'family'

def read_tokens():
    groups = {}
    with open("data/sample.json") as file:
        data = json.loads(file.read())
        for i in data:
            groups.setdefault(i[group], []).append(i[token])
        return groups

def draw_assignments(groups):
    assignments = []
    senders = copy.deepcopy(groups)
    recipients = copy.deepcopy(groups)

    while senders:

        # Choose senders and get valid targets for senders
        sender_group_name, sender_members = senders.popitem()
        targets = copy.deepcopy(recipients)
        if sender_group_name in targets:
            targets.pop(sender_group_name)

        # Assign recievers randomly from valid targets
        for person in sender_members:
            target_group_key, target_group_values = random.choice(list(targets.items()))
            target_member_index = random.randrange(len(target_group_values))
            target_member = targets[target_group_key].pop(target_member_index)
            assignments.append(
                {
                    'sender': person,
                    'recipient': target_member
                }
            )

            # Remove recipient from original recipient set
            recipients[target_group_key].pop(target_member_index)

            # Remove groups as necessary
            if len(recipients[target_group_key]) == 0:
                recipients.pop(target_group_key)
            if len(targets[target_group_key]) == 0:
                targets.pop(target_group_key)

    return assignments


if __name__ == '__main__':
    groups = read_tokens()
    assignments = draw_assignments(groups)
    with open('output/assignments.json', 'w') as output:
        output.write(json.dumps(assignments))
