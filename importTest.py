import rearrange

def main():
    rearrange.arg_check()
    myFile=rearrange.getFile()
    print(myFile)

if __name__=="__main__":
    main()