#!/usr/bin/python
import sys
import re
import libwiki

def handler(page):
    #print("handler() start!")
    title = page['title']
    #print("title = "+title)
    for line in page['text']:
        result = re.search("http:\/\/[0-9a-z\.]*megalodon", line)
        if result:
            print("* [[:" + title + "]]");
            print("*: <nowiki>[" + line + "]</nowiki>");

def sub(dumpfile):
    libwiki.set_filename(dumpfile)
    libwiki.set_handler(handler)
    libwiki.do_proc()

def main():
    if len(sys.argv) < 2:
        print("Usage: main.py <filename>")
        return
    dumpfile = sys.argv[1]
    print(dumpfile)
    sub(dumpfile)
    print("done.")

if __name__ == '__main__':
    main()
