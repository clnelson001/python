import rearrange
import json
import sys

def main():
    rearrange.arg_check()
    myFile=rearrange.getFile()
    #print(myFile)
    k_list=[]
    k_count=1
    try:
        with open(myFile,mode='r') as f:
            data_list = json.load(f)
    except:
        print("could not open file: "+myFile)
        sys.exit(1)
    for data in data_list:
        keys = data.keys()
        for k in keys:
                k_list.append(k)
    k_list.sort()
    print(k_list)



if __name__=="__main__":
    main()