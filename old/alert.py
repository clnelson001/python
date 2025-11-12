import sys
import json
import csv


def process_line(l):
    result = csv.writer
    if l.get('sha256'):
        lkey = {l['hostname'],l['sha256']}
    elif l.get('threat_id'):
        lkey = {l['hostname'],l['threat_id']}
    else:
        lkey = {l['hostname']}
    


def main():
    DEBUG=False
    
    if len(sys.argv) < 2:
        print("USAGE: python3 "+sys.argv[0]+" <input.log>")
        sys.exit(1)

    logFile = sys.argv[1];    
    try:
        with open(logFile,mode='r') as f:
            for lineCount, line in enumerate(f,1):
                line = line.strip()
                try:
                    l = json.loads(line)
                except:
                    print("Error in json at line "+str(lineCount))
                    continue
                if DEBUG:
                    print(str(lineCount)+": "+json.dumps(l))
                result=process_line(l)
    except:
        print("ERROR - Colud not open file: "+logFile)
    with open("out",'w') as o:
        json.dumps(result,f)

if __name__=="__main__":
    main()