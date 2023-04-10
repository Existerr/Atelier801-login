from api import Client, Forum

import asyncio

async def main():
    try:
        client = Client()
        forum = Forum(client)

        print(f'connected:  {await forum.login("username", "password")}') #replace with your credentials

    finally:
        await client.close()

if __name__ == "__main__":
    asyncio.run(main())

        

        

   

