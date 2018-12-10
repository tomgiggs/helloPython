#encoding=utf8
import logging
import random
from pyleus.storm import Spout

log = logging.getLogger('counter')



class WordSpout(Spout):
    line = 'hello this is a storm python code demo'.strip().split(' ')
    OUTPUT_FIELDS = ["word"]

    def next_tuple(self):
        global line
        line = random.choice(line)
        log.debug(line)
        self.emit((line,))


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,
        filename='./spout_demo.log',
        format="%(message)s",
        filemode='a',
    )
    WordSpout().run()
