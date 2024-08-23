import time
import sys


def delay_print(s):
    """
    fonction permettant d'afficher un message
    :param s: message à afficher
    :type s:str
    """
    for c in s:
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(0.04)
