import re
import markdown


def mdsplit(text):
    # print(r'{}'.format(text))
    lines = []
    for line in text.replace('\r','').split('\n'):
        print (line)
        if re.match(r'^\s*$', line):
            lines.append(""+ line)
        else:
            lines.append(line)
    return lines

def markdownprocess(text):
    prefixstart = '::'
    prefixend = '::'
    code_start =   '::start-code::'
    code_end =   '::end-code::'
    input_start =  '::start-input::' 
    input_end =  '::end-input::' 
    output_start =  '::start-output::'
    output_end =  '::end-output' 
    
    lines = mdsplit(text)
    a = []
    for index,l in enumerate(lines):
        
        # if(l.find('{{')or l.find('{{') == 0):
        #     if(l.find('}}') != -1 ):
        #         find1 = l.find("{{")
        #         find2 = l.find("}}")
        #         new = "<input type='text' style='background-color: #FCF5D8;'size='8'>"
                
        #         l1 = l[0:find1] + new + l[find2+2:len(l)]
        #         lines[index] = l1
        #         print(("##",l.find('{{')or l.find('{{') == 0))
        #         print('###',l.find ('}}')) 

        if(l == code_start):
            lines[index] =  "<p style='color:green'>"
            a.append(index)
        if(l == code_end):
            lines[index] = "</p>"
            a.append(index)

        if(l == input_start):
            lines[index] = "<!--"
            a.append(index)

        if(l == input_end):
            lines[index] = "-->"
            a.append(index)

        if(l == output_start):
            lines[index] = "<mark>"
            a.append(index)

        if(l == output_end):
            lines[index] = "</mark>"
            a.append(index)


    html = "<br>".join(lines)
    print("html:",html)
    html = html.replace("<br><br>","<br>")
    html = html.replace("<br></p><br>","</p>")
    html = html.replace("<br><mark><br>","<mark>")
    print("linesnobr:",html)
    md = markdown.Markdown()
    m = md.convert(html)

    return m