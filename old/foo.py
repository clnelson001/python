import sys
import json

VALID = (
    "ts",
    "agent_id",
    "hostname",
    "status",
    "cpu_pct",
    "mem_pct",
    "last_checkin_sec"
)

def parseLine (myLine):
    
    result = ""
    for key in line:
        if key not in VALID:
            result = "Unexpected value detected!"
        else:
            if line.get(key,0):
                result = line[key]
    return result 

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 "+sys.argv[0] + " <filename.log>")
        sys.exit(1)
    
    myfile = sys.argv[1]
    
    with open(myfile, mode='r') as f:
        
        for line_no, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                # In a real script you might log this somewhere
                print(f"Skipping invalid JSON at line {line_no}")
                continue


            #result =  parseLine(line)
    #print(type(result))
    fruits = ["apple", "banana", "cherry"]

    for index, fruit in enumerate(fruits):
        print(index, fruit)
    print("\n\n")
    for i, fruit in enumerate(fruits, start=192):
        print(i, fruit)
    print("\n\n")
    for i, ch in enumerate("SENTINEL"):
        print(i, ch)
    print("\n\n")





if __name__ == "__main__":
    main()
