import re
import markdown


def mdsplit(text):
    
    try:
        lines = []
        for line in text.replace('\r','').replace('\t','&nbsp;&nbsp;&nbsp;&nbsp;').split('\n'):
            
            if re.match(r'^\s*$', line):
                lines.append(""+ line)

            else:
                lines.append(line)
           
        return lines
        
    except:
        return ""
    
def mdprocessmarkdown(text):
    try:
        lines = mdsplit(text)
        
        q1 = text.find('::start-input::')
        q2 = text.find('::start-output::')
        
        startoutput = lines.index('::start-output::')
        if q1 >= 0 :
            startinput = lines.index('::start-input::')
        else :
            iendmarkdown = startoutput
        
        if q1 >= 0 and q2 >= 0:
            number = [startinput,startoutput]
            iendmarkdown = min(number)
            
        
        stringmarkdown = ""
                
        for i in range(0,iendmarkdown):
            stringmarkdown += lines[i] + "<br>"
            
        md = markdown.Markdown()
        m = md.convert(stringmarkdown)
        
        return m
    
    except:
        return ""

def mdprocessmarkdownbetween(text):
    try:
        lines = mdsplit(text)
       
        q1 = text.find('::start-input::')
        q2 = text.find('::start-output::')
        stringbetween = ""
        
        startoutput = lines.index('::start-output::')
        if q1 >= 0 :
            startinput = lines.index('::start-input::')
            endinput = lines.index('::end-input::')
            endoutput = lines.index('::end-output::')
            if startinput < startoutput:
                if (startoutput) - (endinput) != 1:
                    for i in range(endinput+1,startoutput):
                        stringbetween += lines[i] + "<br>"
                        md = markdown.Markdown()
                        m1 = md.convert(stringbetween)
                        
            else:
                if (startinput) - (endoutput) != 1:
                    for i in range(endinput+1,startoutput):
                        stringbetween += lines[i] + "<br>"
                        md = markdown.Markdown()
                        m1 = md.convert(stringbetween)
                
            return m1

        else :
            return ""
    
    except:
        return ""

def mdprocessmarkdownlast(text):
    try:
        lines = mdsplit(text)
       
        q1 = text.find('::start-input::')
        q2 = text.find('::start-output::')
        stringlast = ""
        endoutput = lines.index('::end-output::')
        startoutput = lines.index('::start-output::')

        if q1 >= 0 :
            startinput = lines.index('::start-input::')
            endinput = lines.index('::end-input::')
            
            if startinput < startoutput:
                if endoutput != len(lines):
                    for i in range(endoutput+1,len(lines)):
                        stringlast += lines[i] + "<br>"
                        md = markdown.Markdown()
                        m2 = md.convert(stringlast)
                   
            else:
                if endinput != len(lines):
                    for i in range(endinput+1,len(lines)):
                        stringlast += lines[i] + "<br>"
                        md = markdown.Markdown()
                        m2 = md.convert(stringlast)
                
            return m2

        else :
            if endoutput != len(lines):
                for i in range(endoutput+1,len(lines)):
                    stringlast += lines[i] + "<br>"
                    md = markdown.Markdown()
                    m2 = md.convert(stringlast)
        
                return m2

            else: 

                return ""

    except:

        return ""

def mdprocessinput(text):

    try:
        lines = mdsplit(text)
        istartinput = lines.index('::start-input::')
        iendinput = lines.index('::end-input::')
        stringinput = ""
        for i in range(iendinput):
            if i > istartinput:
                stringinput += lines[i] + "<br>"
                
            return stringinput

    except:

        return ""


def mdprocessoutput(text):

    try:
        lines = mdsplit(text)
        istartoutput = lines.index('::start-output::')
        iendoutput = lines.index('::end-output::')
        stringoutput = ""
        for i in range(iendoutput):
            if i > istartoutput:
                stringoutput += lines[i] + "<br>"
                
        return stringoutput

    except:

        return ""

def mdprocess(text):

    try:
        lines = mdsplit(text)
        linesmarkdown = mdprocessmarkdown(lines)
        linesinput = mdprocessinput(lines)
        linesoutput = mdprocessoutput(lines)
        result = linesmarkdown + linesinput + linesoutput
        
        return result
    
    except:

        return ""
    
  

