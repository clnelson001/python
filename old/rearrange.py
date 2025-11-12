import sys
import json

def rearrange(myList):
    new_data={}
    
    for dict in myList:
        if not new_data.get(dict['host']):
            new_data[dict['host']] = [dict['status']]
        else:
           new_data[dict['host']].append(dict['status'])
    return new_data

def arg_check():
    if len(sys.argv)!=2:
        print("Usage: python3 "+sys.argv[0]+" <inputFile.json>")
        sys.exit(1)
    
def getFile():
    inputFile = sys.argv[1]
    return inputFile

def main():
    arg_check()
    inputFile = getFile()
    outputfile='output'

    try:
        with open(inputFile,mode='r') as f:
            input = json.load(f)
            new_data = rearrange(input)
    except:
        print("ERROR opening "+inputFile)
        sys.exit(1)

    try:
        with open(outputfile,mode='w') as j:
            json.dump(new_data,j)
    except:
        print("ERROR opening "+outputfile)
        sys.exit(1)

    result = json.dumps(new_data) 
    print(result)


if __name__=="__main__":
    main()