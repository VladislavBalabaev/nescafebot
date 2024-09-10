import pandas as pd

from db.operations.messages import send_msg_user


async def send_matching(matched: pd.DataFrame):
    def info_by_username(username):
        nonlocal matched

        row = matched.loc[matched["username"] == username].iloc[0]

        return f"{row['info']['full_name']} (@{row['username']}) с {row['info']['program']['name']}'{row['info']['program']['year']}.\nСмайл пользователя - {row['emoji']}\nО себе: {row['info']['about']}"


    for user_id in matched.index:
        await send_msg_user(user_id, 
                            f"Привет!\nПришли с результатами случайного кофе)")
        await send_msg_user(user_id, 
                            f"Твой смайл - {matched.loc[user_id, 'emoji']}")

        assignments = matched.loc[user_id, 'assignments']
        n = len(assignments)

        if n==0:
            await send_msg_user(user_id,
                                f"В этот раз тебе не досталось тех, кому можно написать.\nВозможно, это потому что у тебя слишком много людей в черном списке.\n\nВерни кого-нибудь из него и в следующий раз шанс кого-нибудь получить будет больше")
        elif n==1:
            await send_msg_user(user_id,
                                f"В этот раз тебе выпал только один человек, которому ты можешь написать:")

            await send_msg_user(user_id,
                                info_by_username(assignments[0]))

            await send_msg_user(user_id, 
                                "Ты можешь написать ему его смайл, он сразу поймет, что выпал тебе на кофе)")
        elif n==2:
            await send_msg_user(user_id,
                                f"В этот раз тебе выпали двое человек, которым ты можешь написать:")

            await send_msg_user(user_id,
                                info_by_username(assignments[0]))

            await send_msg_user(user_id,
                                info_by_username(assignments[1]))

            await send_msg_user(user_id,
                                f"Ты можешь написать им их смайл, они сразу поймут, что выпали тебе на кофе)")
        else:
            raise ValueError(f"_id='{user_id}' has more than 2 assignments.")

    return
