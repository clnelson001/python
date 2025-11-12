import sys
import json
# # mytest =["ok", "error", "ok", "timeout", "error", "ok","go","foo","timeout"]
# # counts ={}
# # for i in mytest:
# #     if counts.get(i):
# #         counts[i] += 1
# #     else:
# #         counts[i] = 1  
# # # for k in counts.keys():
# # #     print(k+" = "+str(counts[k]))
# # print(counts)
# def ispalindrome(s):
#     mystr = s.lower()
#     reverse="".join(reversed(mystr))
#     # print(reverse)
#     # print(mystr)
    
#     return mystr == reverse

# myinput = sys.argv[1]
# if ispalindrome(myinput):
#     print("YES, "+str(myinput)+" is a palindrome!")
# else:
#     print("NO, "+str(myinput)+" is not a palindrome!")

if len(sys.argv)!=2:
    print("Usage: python3 "+sys.argv[0]+" file.json")
    sys.exit(1)
myfile = sys.argv[1]
with open(myfile,mode='r') as f:
    data=json.load(f)
    failed = {}
    for entry in data:
        if entry.get("status") != "ok":
            failed[entry['service']]=entry['status']
    json_str = json.dumps(failed) 
    print(json_str)
            

