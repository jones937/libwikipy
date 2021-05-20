import re

g_dumpfile = ""
g_handler = ""
page = {}
g_inpage = False
g_intext = False
g_inrevision = False
g_incontributor = False

"""
Data Structure
page['title'] = "タイトル"
page['text'] = ["行1", "行2", "行3"]
"""

#---- re.compile --------------------------
RE_PAGE1 = re.compile("^[ ]*<\/page>$")
RE_TITLE1 = re.compile("^[ ]*<title>(.*)<\/title>$")
RE_PRESERVE1 = re.compile(".*xml:space=\"preserve\">")
RE_TEXT1 = re.compile("^[ ]*<text")
RE_TEXT2 = re.compile("<\/text>$")
RE_TEXT3 = re.compile("<\/text>$")
#------------------------------------------

def set_filename(filename):
    global g_dumpfile
    #print("filename=" + filename)
    g_dumpfile = filename

def set_handler(handler_arg):
    global g_handler
    g_handler = handler_arg

def convert_ref2norm(line):
    line = line.replace("&lt;","<")
    line = line.replace("&gt;",">")
    line = line.replace("&quot;","\"")
    line = line.replace("&apos;","'")
    line = line.replace("&amp;","&")
    return line


def parse():
    global g_inpage
    global g_intext
    global g_inrevision
    global g_incontributor
    global page
    #print("do_proc() start!")
    #print("g_dumpfile=" + g_dumpfile)

    with open(g_dumpfile) as f:
        for line in f:
            if not g_inpage:
                if "<page>" in line:
                    g_inpage = True
                    continue

            #result = re.search("^[ ]*<\/page>$", line)
            result = RE_PAGE1.search(line)
            if result:
                if "title" in page and "text" in page:
                    g_handler(page)
                g_inpage = False
                g_intext = False
                g_inrevision = False
                g_incontributor = False
                page = {}
                continue



            #result = re.search("^[ ]*<title>(.*)<\/title>$", line)
            if not g_intext:
                result = RE_TITLE1.search(line)
                if result:
                    #print("title="+result.group(1))
                    page['title'] = result.group(1)
                    continue


            if not g_intext:
                #result = re.search("^[ ]*<text", line)
                result = RE_TEXT1.search(line)
                if result:
                    #print("g_intext = True")
                    g_intext = True
                    #line = re.sub(".*xml:space=\"preserve\">", "", line)
                    line = RE_PRESERVE1.sub("", line)
                    line = line.rstrip('\n')
                    #print("line="+line)
                    page['text'] = [line]
                    continue
                
            #result = re.search("<\/text>$", line)
            result = RE_TEXT2.search(line)
            if result:
                #line = re.sub("<\/text>$", "", line)
                line = RE_TEXT3.sub("", line)
                line = line.rstrip('\n')
                if "text" in page:
                    page['text'].append(line)
                else:
                    page['text'] = [line]
                g_intext  = False
                continue

            if g_intext:
                line = line.rstrip('\n')
                if "text" in page:
                    page['text'].append(line)
                else:
                    page['text'] = [line]
                continue
    

