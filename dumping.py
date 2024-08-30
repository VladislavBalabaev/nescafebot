import asyncio
import aioredis

async def main():
    # Create a Redis connection pool
    redis_con = await aioredis.from_url("redis://:" + config.REDIS_PASSWORD.get_secret_value() + "@redis_DB:6379")

    # Trigger a BGSAVE to create the dump file
    await redis_con.bgsave()

    #
    bgsave_time = 120
    await asyncio.sleep(bgsave_time)

    # Optionally, print a confirmation message
    print("Triggered BGSAVE. Redis is creating a dump file.")

    # Close the connection
    await redis_con.close()

# Run the asynchronous main function
if __name__ == '__main__':
    while True:
        asyncio.run(main())