import pandas as pd

from db.operations.messages import send_msg_user


async def send_matching(matched: pd.DataFrame):
    def emoji_by_username(username):
        nonlocal matched

        return matched.loc[matched["username"] == username, "emoji"].iloc[0]


    for user_id in matched.index:
        await send_msg_user(user_id, f"Привет! ")
        await send_msg_user(user_id, f"Твой смайл - {matched.loc[user_id, 'emoji']}")

        assignments = matched.loc[user_id, 'assignments']
        n = len(assignments)

        if n==0:
            await send_msg_user(
                user_id,
                f"В этот раз тебе не досталось тех, кому можно написать.\nВозможно, это потому что у тебя слишком много людей в черном списке.\n\nВерни кого-нибудь из него и в следующий раз шанс кого-нибудь получить будет больше",
            )
        elif n==1:
            await send_msg_user(
                user_id,
                f"В этот раз тебе выпал только один человек, которому ты можешь написать, это - @{assignments[0]}.\n\nТы можешь написать ему его смайл - {emoji_by_username(assignments[0])}, он сразу поймет, что выпал тебе на кофе)",
            )
        elif n==2:
            await send_msg_user(
                user_id,
                f"В этот раз тебе выпали двое человек, которым ты можешь написать, это - @{assignments[0]} со смайлом {emoji_by_username(assignments[0])}, а также @{assignments[1]} со смайлом {emoji_by_username(assignments[1])}.\n\nТы можешь написать им их смайл, они сразу поймут, что выпали тебе на кофе)",
            )

    return
