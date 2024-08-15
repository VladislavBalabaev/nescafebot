import random
import secrets
import pandas as pd
from collections import defaultdict

from emojis import distinct_emoji_list


def uniform_blacklist_matching(blacklists):
    # max_assignments = (2 * len(users)) // len(users) + 1
    max_assignments = 2


    users = list(blacklists.keys())
    matched = {user: [] for user in users}
    assignment_counts = defaultdict(int)                # a dictionary that provides a default value for a non-existent key


    for user in users:
        possible_candidates = [u for u in users if u != user and u not in blacklists[user]]
        random.shuffle(possible_candidates)

        candidates_sorted = sorted(possible_candidates, key=lambda u: assignment_counts[u])

        for candidate in candidates_sorted:
            if len(matched[user]) < 2 and assignment_counts[candidate] < max_assignments:
                matched[user].append(candidate)
                assignment_counts[candidate] += 1

                if len(matched[user]) == 2:
                    break

    return matched


def match():
    # USERS RELATED - before matching:
    # df.loc[df["active"], "users"]
        # check if user didn't block bot, if did -> user active=False, if not:

    blacklists = ...
    


    matched = uniform_blacklist_matching(blacklists)

    matched = pd.DataFrame(matched.items(), columns=["user", "assignments"])

    emojis = distinct_emoji_list()
    matched["smile"] = [secrets.choice(emojis) for _ in range(matched.shape[0])]

    return matched
