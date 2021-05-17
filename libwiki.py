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
RE_NS1 = re.compile("^[ ]*<ns>(.*)<\/ns>$")
RE_ID1 = re.compile("^[ ]*<id>(.*)<\/id>$")
RE_PARENTID1 = re.compile("^[ ]*<parentid>(.*)<\/parentid>$")
RE_USERNAME1 = re.compile("^[ ]*<username>(.*)<\/username>$")
RE_IP1 = re.compile("^[ ]*<ip>(.*)<\/ip>$")
RE_TIMESTAMP1 = re.compile("^[ ]*<timestamp>(.*)<\/timestamp>$")
RE_MODEL1 = re.compile("^[ ]*<model>(.*)<\/model>$")
RE_FORMAT1 = re.compile("^[ ]*<format>(.*)<\/format>$")
RE_TITLE1 = re.compile("^[ ]*<title>(.*)<\/title>$")
RE_TEXT1 = re.compile("^[ ]*<text")
RE_PRESERVE1 = re.compile(".*xml:space=\"preserve\">")
RE_TEXT2 = re.compile("<\/text>$")
RE_TEXT3 = re.compile("<\/text>$")
RE_REVISION1 = re.compile("^[ ]*<revision")
RE_REVISION2 = re.compile("^[ ]*<\/revision>$")
RE_CONTRIBUTOR1 = re.compile("^[ ]*<contributor")
RE_CONTRIBUTOR2 = re.compile("^[ ]*<\/contributor>$")
#------------------------------------------

def set_filename(filename):
    global g_dumpfile
    #print("filename=" + filename)
    g_dumpfile = filename

def set_handler(handler_arg):
    global g_handler
    g_handler = handler_arg

def is_bz2(filename):
    if ".bz2" in filename:
        return True
    return False

def proc_core(line):
    global g_inpage
    global g_intext
    global g_inrevision
    global g_incontributor
    global page

    #print("line="+line)

    # convert a HTML character entity reference to a normal character.
    line = line.replace("&lt;","<")
    line = line.replace("&gt;",">")
    line = line.replace("&quot;","\"")
    line = line.replace("&apos;","'")
    line = line.replace("&amp;","&")

    if not g_inpage:
        if "<page>" in line:
            g_inpage = True
            return

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
        return

    #result = re.search("^[ ]*<ns>(.*)<\/ns>$", line)
    if not g_intext:
        result = RE_NS1.search(line)
        if result:
            page['ns'] = result.group(1)
            return

    #result = re.search("^[ ]*<id>(.*)<\/id>$", line)
    if not g_intext:
        result = RE_ID1.search(line)
        if result:
            if g_inrevision:
                page['revisionid'] = result.group(1)
            elif g_incontributor:
                page['contributorid'] = result.group(1)
            else:
                page['pageid'] = result.group(1)
            return
    #result = re.search("^[ ]*<parentid>(.*)<\/parentid>$", line)
    if not g_intext:
        result = RE_PARENTID1.search(line)
        if result:
            page['parentid'] = result.group(1)
            return
    #result = re.search("^[ ]*<username>(.*)<\/username>$", line)
    if not g_intext:
        result = RE_USERNAME1.search(line)
        if result:
            page['username'] = result.group(1)
            return
    #result = re.search("^[ ]*<ip>(.*)<\/ip>$", line)
    if not g_intext:
        result = RE_IP1.search(line)
        if result:
            page['ip'] = result.group(1)
            return
    #result = re.search("^[ ]*<timestamp>(.*)<\/timestamp>$", line)
    if not g_intext:
        result = RE_TIMESTAMP1.search(line)
        if result:
            page['timestamp'] = result.group(1)
            return
    #result = re.search("^[ ]*<model>(.*)<\/model>$", line)
    if not g_intext:
        result = RE_MODEL1.search(line)
        if result:
            page['model'] = result.group(1)
            return
    #result = re.search("^[ ]*<format>(.*)<\/format>$", line)
    if not g_intext:
        result = RE_FORMAT1.search(line)
        if result:
            page['format'] = result.group(1)
            return

    #result = re.search("^[ ]*<title>(.*)<\/title>$", line)
    if not g_intext:
        result = RE_TITLE1.search(line)
        if result:
            #print("title="+result.group(1))
            page['title'] = result.group(1)
            return

    if not g_intext:
        if not g_inrevision:
            #result = re.search("^[ ]*<revision", line)
            result = RE_REVISION1.search(line)
            if result:
                g_inrevision = True
                return
    #result = re.search("^[ ]*<\/revision>$", line)
    if not g_intext:
        result = RE_REVISION2.search(line)
        if result:
            g_inrevision = False
            return

    if not g_intext:
        if not g_incontributor:
            #result = re.search("^[ ]*<contributor", line)
            result = RE_CONTRIBUTOR1.search(line)
            if result:
                g_incontributor = True
                return
    #result = re.search("^[ ]*<\/contributor>$", line)
    if not g_intext:
        result = RE_CONTRIBUTOR2.search(line)
        if result:
            g_incontributor = False
            return

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
            return
        
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
        return

    if g_intext:
        line = line.rstrip('\n')
        if "text" in page:
            page['text'].append(line)
        else:
            page['text'] = [line]
        return

        

def do_loop_bz2(dumpfile):
    with bz2.open(dumpfile) as f:
        for s_line in f:
            proc_core(s_line)

def do_loop_xml(dumpfile):
    with open(dumpfile) as f:
        for s_line in f:
            proc_core(s_line)

def parse():
    #print("do_proc() start!")
    #print("g_dumpfile=" + g_dumpfile)

    if is_bz2(g_dumpfile):
        do_loop_bz2(g_dumpfile)
    else:
        do_loop_xml(g_dumpfile)
    

