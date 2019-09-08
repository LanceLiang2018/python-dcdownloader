from dcdownloader import base_logger
import json
import os
import aiofiles


FILENAME = 'comic_info.json'


async def save(url: str, save_path: str):
    logger = base_logger.getLogger(__name__)
    info = {
        'url': url
    }
    try:
        async with aiofiles.open(os.path.join(save_path, FILENAME), 'w', encoding='UTF8') as f:
            # await json.dump(f, info)
            await f.write(json.dumps(info))
    except IOError:
        logger.warning("Couldn't save info file %s !" % FILENAME)
        return


def get(save_path: str):
    logger = base_logger.getLogger(__name__)
    try:
        with open(os.path.join(save_path, FILENAME), 'r', encoding='UTF8') as f:
            info = json.load(f)
            return info
    except (IOError, json.decoder.JSONDecodeError) as e:
        logger.warning('Info file error! %s' % str(e))
        return


def exist(save_path: str):
    if os.path.exists(os.path.join(save_path, FILENAME)):
        return True
    return False

