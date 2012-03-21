#!/usr/bin/env python
# -*- coding: utf-8 *-*

import socket
import _thread
import curses

global __linecount__
__linecount__ = 0

def pprint(pad, *args):
    global __linecount__
    if __linecount__ > 33:
        pad.addstr(0, 0, '                    \n'*34)
        pad.addstr(0, 0, '')
        __linecount__ = 0

    for a in args:
        pad.addstr(" %s" % (str(a),))
    pad.addstr('\n')
    pad.border('|', '|')
    pad.refresh()
    __linecount__ += 1

def print_thread(soc, pad):
    while 1:
        try:
            s = str(soc.recv(1024), 'utf-8', 'ignore')
            pprint(pad, "[RECV] " + (s if s.strip() else 'NULL STRING'))
        except:
            continue

if __name__ == '__main__':
    soc, conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM), None

    while 1:
    #    try:
        print("Client or Server?")
        s = input("[C/s] : ")
        if (s == 'c') or (not s):
            host = input('hostname: ')
            port = int(input('port: '))
            soc.connect((host, port))
            conn = soc
            break
        elif s == 's':
            port = int(input('port: '))
            soc.bind(('', port))
            soc.listen(5)
            conn, addr = soc.accept()
            print('Connected by', addr)
            break
        else:
            continue
    #    except KeyboardInterrupt:
    #        exit(0)
    #
    #    except Exception as e:
    #        print(e)
    #        pass

    conn.settimeout(5.0)
    stdscr = curses.initscr()
    curses.echo()
    curses.cbreak()
    outpad = curses.newwin(35, 60, 0, 0)
    inpad = curses.newwin(35, 60, 0, 60)
    curses.setsyx(80, 0)

    _thread.start_new_thread(print_thread, (conn, outpad,))

    while 1:
        inpad.addstr(' $ ')
        cmd = str(inpad.getstr(), 'utf-8', 'ignore').split(' ', 1)

        if cmd[0] == 'send':
            conn.send(cmd[1].encode())
        elif cmd[0] == 'exit':
            curses.endwin()
            break
        else:
            try:
                exec(' '.join(cmd))
            except Exception as e:
                pprint(inpad, e)

    conn.close()
