import asyncio

from nats import NATS


nc = NATS()

async def publisher():
    while True:
        try:
            await nc.publish('updates.main', b'All is well')
            await nc.flush()
            await asyncio.sleep(2)
            print('[Отправитель] Сообщение отправлено')
        except asyncio.CancelledError:
            break


async def subscriber1():
    def cb(msg):
        print('[Получатель 1] Получено сообщение:', msg)

    await nc.subscribe('updates.main', cb=cb)
    print('[Получатель 1] Подписка оформлена')


async def subscriber2():
    def cb(msg):
        print('[Получатель 2] Получено сообщение:', msg)

    await nc.subscribe('updates.*', cb=cb)
    print('[Получатель 2] Подписка оформлена')


async def main():
    await nc.connect('localhost:4222')
    print('Соединение установлено')

    pub_task = asyncio.create_task(publisher())
    sub1_task = asyncio.create_task(subscriber1())
    sub2_task = asyncio.create_task(subscriber2())
    await asyncio.gather(sub1_task, sub2_task, pub_task)
        
    await nc.close()
    print('Соединение закрыто')


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
