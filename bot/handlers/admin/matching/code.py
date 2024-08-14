# #suppose
# users = ["vbalab", "Madfyre", "loh", "sova", "b", "c", "d"]
# blacklists = {"vbalab": {"Madfyre"},
#               "Madfyre": {}, 
#               "loh": {"Madfyre", "sova"},
#               "sova": {"c"},
#               "b": {"c"},
#               "c": {"d"},
#               "d": {"b"}}

# def match(users: list, blacklists: dict) -> dict:
#     matched = {}
#     matched = max(blacklists, key=lambda x: len(x.))
#     return matched


# a = match(users=users, blacklists=blacklists)
# print(a)
# # for k, v in a.items():
# #     print(f"{k}: {v}")