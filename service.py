import os
# import asyncio
import json

import aiofiles

FILE_NAME = "DATA"
BASE_DIR = os.getcwd() + "/"


async def method_write(name, body):
    await write_to_file(name=name, text=body)
    return "НОРМАЛДЫКС РКСОК/1.0\r\n\r\n".encode("utf-8")


async def method_give(name, body):
    json_data = await get_data_from_file()
    text = json_data.get(name)
    if text:
        response = "НОРМАЛДЫКС РКСОК/1.0\r\n".encode("utf-8") + text.encode("utf-8")
        return response
    else:
        return "НИНАШОЛ РКСОК/1.0\r\n\r\n".encode("utf-8")


async def method_delete(name, body):
    if await delete_from_file(name):
        return "НОРМАЛДЫКС РКСОК/1.0\r\n\r\n".encode("utf-8")
    else:
        return "НИНАШОЛ РКСОК/1.0\r\n\r\n".encode("utf-8")


async def get_data_from_file() -> dict:
    try:
        async with aiofiles.open(BASE_DIR+FILE_NAME, mode='r', encoding="utf-8") as file:
            json_data = await file.read()
            data = json.loads(json_data)
            return data
    except FileNotFoundError:
        async with aiofiles.open(BASE_DIR+FILE_NAME, mode='w', encoding="utf-8") as file:
            await file.write(json.dumps({}))
        return {}


async def write_to_file(name: str, text: str):
    data = await get_data_from_file()
    data[name] = text
    async with aiofiles.open(BASE_DIR+FILE_NAME, mode='w', encoding="utf-8") as file:
        await file.write(json.dumps(data))
    return True


async def delete_from_file(name: str):
    data = await get_data_from_file()
    if data.get(name):
        del data[name]
        async with aiofiles.open(BASE_DIR+FILE_NAME, mode='w', encoding="utf-8") as file:
            await file.write(json.dumps(data))
        return True
    else:
        return False


# asyncio.run(write_to_file(name="Anton Shilinasdas", text=" hihihi Anton"))
# asyncio.run(get_data_from_file())