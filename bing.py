from ping3 import ping
from time import sleep
import subprocess
from rich.console import Console

TIMEOUT=0.5
BASE_VOLUME=0.001
INTERVAL=0.2
THRESHOLD=0.2

BLOCKS = ['▁', '▂', '▃', '▄', '▅', '▆', '▇', '█']

def play_notes(notes, duration=INTERVAL, volume=0.01):
    if isinstance(notes, str):
        synth_args = notes
    else:
        synth_args = ' '.join(notes)
    command = f"play -n synth {duration} {synth_args} vol {volume}"
    subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

if __name__ == '__main__':
    console = Console(width=100)
    while True:
        block = ' '
        try:
            p = ping('8.8.8.8', timeout=TIMEOUT)
            if p == None:
                style = '[red]'
                block = 'X'
                play_notes('trapezium G', volume=BASE_VOLUME*5, duration=INTERVAL*3)
            else:
                r = p/TIMEOUT
                bidx = int(len(BLOCKS) * r)
                block = BLOCKS[bidx]
                if p > THRESHOLD:
                    style = '[yellow]'
                    volume = p/TIMEOUT * BASE_VOLUME
                    play_notes('pluck A', volume=volume)
                else:
                    style = '[green]'
        except Exception as exc:
            style = '[black]'
            block = 'E'
        console.print(f'{style}{block}', end='')
        sleep(INTERVAL)
