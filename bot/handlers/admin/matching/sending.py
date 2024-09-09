import pandas as pd

from db.operations.messages import send_msg_user


async def send_matching(matched: pd.DataFrame):
    def row_by_username(username):
        nonlocal matched

        return matched.loc[matched["username"] == username].iloc[0]


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
            row = row_by_username(assignments[0])

            await send_msg_user(
                user_id,
                f"В этот раз тебе выпал только один человек, которому ты можешь написать, это - {row['info']['full_name']} (@{row['username']}) с {row['info']['program']['name']}'{row['info']['program']['year']}.\n\nТы можешь написать ему его смайл - {row['emoji']}, он сразу поймет, что выпал тебе на кофе)",
            )
        elif n==2:
            row1 = row_by_username(assignments[0])
            row2 = row_by_username(assignments[1])

            await send_msg_user(
                user_id,
                f"В этот раз тебе выпали двое человек, которым ты можешь написать, это - {row1['info']['full_name']} (@{row1['username']}) с {row1['info']['program']['name']}'{row1['info']['program']['year']} со смайлом {row1['emoji']}, а также {row2['info']['full_name']} (@{row2['username']}) с {row2['info']['program']['name']}'{row2['info']['program']['year']} со смайлом {row2['emoji']}.\n\nТы можешь написать им их смайл, они сразу поймут, что выпали тебе на кофе)",
            )
        else:
            raise ValueError(f"_id='{user_id}' has more than 2 assignments.")

    return
