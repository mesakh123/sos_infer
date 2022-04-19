import os
import socket
import asyncio
import pytz
from datetime import datetime
from ..event.eventrouter import EventService
from ..dto.eventschema import EventSchema
from ..models.eventmodels import Events
from ..config.database import database
from ..logger import curr_logger as logger


async def receive_data(reader, writer):

    try:
        request = (await reader.read(255)).decode("utf8")
        request = str(request)
        strings = request.split(";")
        data = {
            "payload_length": strings[0],
            "timestamps": strings[1],
            "ip_address": strings[2],
            "type": int(strings[3]),
        }

        logger.info(
            "Event received at "
            + str(
                datetime.now(pytz.timezone("Asia/Taipei")).strftime(
                    "%Y-%m-%d %H:%M:%S:%f"
                )
            )
            + " with time payload "
            + strings[1]
        )

        event = EventSchema(**data)
        attemps = 5

        saved = False

        while attemps:
            try:

                last_record_id = await EventService.webSocketCreateEvent(event)
                writer.write(request.encode("utf8"))
                await writer.drain()

                saved = True

            except:
                attemps -= 1

            if saved:
                break

            await asyncio.sleep(1)

        if not saved:
            raise Exception
    except:
        writer.write(b"Please try again")
        await writer.drain()

    writer.close()


async def run_server():
    port = int(str(os.environ.get("TRITON_SOCKET_PORT", "9999")))
    server = await asyncio.start_server(receive_data, "0.0.0.0", port)
    async with server:
        await asyncio.gather(server.serve_forever())


async def run_client(ip, port):

    while True:
        try:
            reader, writer = await asyncio.open_connection(ip, port, ssl=False)
        except:
            break
        query = Events.select().where(Events.c.sent == 0)
        data = await database.fetch_all(query=query)
        if data:
            for d in data:
                new_data = dict(d.items())
                new_data.pop("sent")
                id = new_data["id"]
                new_data.pop("id")
                s = ";".join(str(v) for k, v in new_data.items()) + ";"

                try:
                    new_data["sent"] = 1
                    query = (
                        Events.update().where(Events.c.id == int(id)).values(**new_data)
                    )
                    sent = False
                    await database.execute(query=query)
                    writer.write(s.encode("utf-8"))
                except Exception as e:
                    print
                await asyncio.sleep(1)
        writer.close()
        await writer.wait_closed()


async def run_client2(ip, port):
    while True:
        query = Events.select().where(Events.c.sent == 0)
        data = await database.fetch_all(query=query)
        if data:
            logger.info(
                "Query db with sent = 0 finished at "
                + str(
                    datetime.now(pytz.timezone("Asia/Taipei")).strftime(
                        "%Y-%m-%d %H:%M:%S:%f"
                    )
                )
            )
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((ip, port))
                s.setblocking(0)
                for d in data:
                    new_data = dict(d.items())
                    new_data.pop("sent")
                    id = new_data["id"]
                    new_data.pop("id")
                    string = ";".join(str(v) for k, v in new_data.items()) + ";"

                    try:
                        s.sendall(string.encode("utf-8"))
                        new_data["sent"] = 1
                        query = (
                            Events.update()
                            .where(Events.c.id == int(id))
                            .values(**new_data)
                        )
                        logger.info(
                            "Event sent success to the Front End at "
                            + str(
                                datetime.now(pytz.timezone("Asia/Taipei")).strftime(
                                    "%Y-%m-%d %H:%M:%S:%f"
                                )
                            )
                            + " with time payload "
                            + new_data
                        )

                        await database.execute(query=query)

                    except Exception as e:
                        logger.info(
                            "Event sent fail to the Front End at "
                            + str(
                                datetime.now(pytz.timezone("Asia/Taipei")).strftime(
                                    "%Y-%m-%d %H:%M:%S:%f"
                                )
                            )
                        )
                        logger.info("Exception : " + str(e))
                    await asyncio.sleep(1)
        await asyncio.sleep(1)


async def tcp_reconnect():
    host = str(os.environ.get("FE_SOCKET_IP", "0.0.0.0"))
    port = int(str(os.environ.get("FE_SOCKET_PORT", "5001")))
    server = "{} {}".format(host, port)
    timezone = pytz.timezone("Asia/Taipei")
    t = True
    while True:
        now = datetime.now(timezone).strftime("%d/%m/%Y %H:%M:%S")
        print("{} Connecting to server {} ...".format(now, server))
        if t:
            try:
                await run_client2(host, port)
            except ConnectionRefusedError:
                print("Connection to server {} failed!".format(server))
            except asyncio.TimeoutError:
                print("Connection to server {} timed out!".format(server))
            else:
                print("Connection to server {} is closed.".format(server))
        else:
            await run_client2(host, port)
        await asyncio.sleep(1.0)
