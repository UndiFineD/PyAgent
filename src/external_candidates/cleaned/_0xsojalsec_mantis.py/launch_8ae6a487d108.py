# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-mantis\launch.py
import logging
import time

from mantis.config_parsers.logging_utils import LoggingConfig
from mantis.utils.args_parse import ArgsParse
from mantis.workflows.mantis_workflow import MantisWorkflow


def main():
    print("""\u001b[32m

              __  __             _   _     
             |  \/  | __ _ _ __ | |_(_)___ 
             | |\/| |/ _` | '_ \| __| / __|
             | |  | | (_| | | | | |_| \__ \\
             |_|  |_|\__,_|_| |_|\__|_|___/  
            
                                \u001b[1m\u001b[34mRecon Automation Framework (v1.0) \u001b[34m\u001b[1m                                           
          \u001b[0m""")
    args = ArgsParse.args_parse()
    LoggingConfig.configure_logging(args)
    if args.use_ray:
        runtime_env = {"working_dir": ".", "excludes": [".git"]}
        __import__("ray").init(runtime_env=runtime_env)
    MantisWorkflow.select_workflow(args=args)


if __name__ == "__main__":
    start = time.perf_counter()
    main()
    finish = time.perf_counter()
    # logging.info(f"Total time taken to run the tool: {round(finish - start, 2)} seconds")
