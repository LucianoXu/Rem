##################################################################
# input - output interactive prover through file system

from .prover import *
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
import time
import os

class InteractiveFileSystem(FileSystemEventHandler):
    def __init__(self, input : str, output : str, opts : dict[str, np.ndarray]) -> None:
        super().__init__()
        self.input = input
        self.output = output

        self.opts = opts

        # process once
        with open(input, "r", encoding="utf-8") as p_in:
            code = p_in.read()
        with open(output, "w", encoding="utf-8") as p_out:
            p_out.write("Calculating...")
            p_out.flush()
            Prover.restart(opts)
            Prover()(code)
            outstr = str(Prover())
            p_out.seek(0)
            p_out.truncate()
            p_out.write(outstr)

        self.last_code = code

    def on_modified(self, event):
        
        if event.is_directory or os.path.basename(event.src_path) != os.path.basename(self.input):
            return

        with open(self.input, "r", encoding="utf-8") as p_in:
            code = p_in.read()

        # test whether the modification has been calculated
        if code == self.last_code:
            return
        
        print(f"'{self.input}' modification detected.")
        self.last_code = code

        p_out = open(self.output, "w", encoding="utf-8")
        p_out.write("Calculating...")
        p_out.flush()

        # restart and calculate
        Prover.restart(self.opts)
        Prover()(code)
        outstr = str(Prover())

        p_out.seek(0)
        p_out.truncate()
        p_out.write(outstr)
        p_out.close()





from qplcomp import QOpt, EQOpt
def qpv2_server(input : str, output : str = "output.txt", opts: dict[str, np.ndarray] = {}) -> None:
    '''
    Start the QPV2 prover in input and output files.

    opts: the extra quantum operators
    '''

    # try open the input file
    with open(input, "r") as p:
        pass

    with open(output, "w") as p:
        p.write("   QPV2: write and save to start.")

    event_handler = InteractiveFileSystem(input, output, opts)
    observer = Observer()
    observer.schedule(event_handler, os.path.dirname(input))
    observer.start()

    try:
        while True:
            time.sleep(0.2)

    except KeyboardInterrupt:
        observer.stop()
    observer.join()

    

    


    