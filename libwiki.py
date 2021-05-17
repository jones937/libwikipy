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

    result = re.search("^[ ]*<\/page>$", line)
    if result:
        if "title" in page and "text" in page:
            g_handler(page)
        g_inpage = False
        g_intext = False
        g_inrevision = False
        g_incontributor = False
        page = {}
        return

    result = re.search("^[ ]*<ns>(.*)<\/ns>$", line)
    if result:
        page['ns'] = result.group(1)
        return

    result = re.search("^[ ]*<id>(.*)<\/id>$", line)
    if result:
        if g_inrevision:
            page['revisionid'] = result.group(1)
        elif g_incontributor:
            page['contributorid'] = result.group(1)
        else:
            page['pageid'] = result.group(1)
        return
    result = re.search("^[ ]*<parentid>(.*)<\/parentid>$", line)
    if result:
        page['parentid'] = result.group(1)
        return
    result = re.search("^[ ]*<username>(.*)<\/username>$", line)
    if result:
        page['username'] = result.group(1)
        return
    result = re.search("^[ ]*<ip>(.*)<\/ip>$", line)
    if result:
        page['ip'] = result.group(1)
        return
    result = re.search("^[ ]*<timestamp>(.*)<\/timestamp>$", line)
    if result:
        page['timestamp'] = result.group(1)
        return
    result = re.search("^[ ]*<model>(.*)<\/model>$", line)
    if result:
        page['model'] = result.group(1)
        return
    result = re.search("^[ ]*<format>(.*)<\/format>$", line)
    if result:
        page['format'] = result.group(1)
        return

    result = re.search("^[ ]*<title>(.*)<\/title>$", line)
    if result:
        #print("title="+result.group(1))
        page['title'] = result.group(1)
        return

    if not g_intext:
        result = re.search("^[ ]*<text", line)
        if result:
            #print("g_intext = True")
            g_intext = True
            line = re.sub(".*xml:space=\"preserve\">", "", line)
            line = line.rstrip('\n')
            #print("line="+line)
            page['text'] = [line]
            return
        
    result = re.search("<\/text>$", line)
    if result:
        line = re.sub("<\/text>$", "", line)
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

    if not g_inrevision:
        result = re.search("^[ ]*<revision", line)
        if result:
            g_inrevision = True
            return
    result = re.search("^[ ]*<\/revision>$", line)
    if result:
        g_inrevision = False
        return

    if not g_incontributor:
        result = re.search("^[ ]*<contributor", line)
        if result:
            g_incontributor = True
            return
    result = re.search("^[ ]*<\/contributor>$", line)
    if result:
        g_incontributor = False
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
    

