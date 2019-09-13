from dcdownloader import arg_parse, version, base_logger, update_info
from dcdownloader.scheduler import Scheduler
from dcdownloader import parser_selector

import sys
exit = sys.exit
import os
import time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../'))

# for unittest
cmd_args = None
logger = base_logger.getLogger(__name__)


def main():
    args = arg_parse.parser.parse_args(cmd_args)

    # print(args)
    # exit()
    #
    version.show_welcome()

    # 在这里处理更新请求
    task_paths = []
    if args.update:
        time.sleep(0.1)
        scan_path = args.output_path
        logger.info('Update mode.Scanning folders...')
        # print(os.listdir(scan_path))
        file_list = list(os.listdir(scan_path))
        for file in file_list:
            target_path = os.path.join(scan_path, file)
            if not os.path.isdir(target_path):
                continue
            if os.path.exists(os.path.join(target_path, update_info.FILENAME)):
                # print(target_path)
                logger.info('Task: %s' % target_path)
                task_paths.append(target_path)

        for task in task_paths:
            info = update_info.get(task)
            if info is None:
                continue
            s = Scheduler(url=info['url'], output_path=args.output_path, parser=parser_selector.get_parser(info['url']),
                          fetch_only=args.fetch_only, proxy=args.proxy, verify_ssl=args.verify_ssl, update=args.update)
            s.run()
        exit()

    elif not args.url:
        time.sleep(0.1)
        logger.error('error: the following arguments are required: URL')
        exit(1)
    
    s = Scheduler(url=args.url, output_path=args.output_path, parser=parser_selector.get_parser(args.url),
                  fetch_only=args.fetch_only, proxy=args.proxy, verify_ssl=args.verify_ssl, update=args.update)
    s.run()


if __name__ == '__main__':
    main()
