import re, sys, os, datetime

mins = sys.argv[1] # Log check interval, minutes

mass, ip, unknownbr = [], [], [] # mass - list for importing log, ip - list of non local IP addresses, unknownbr - list of unknown browsers
nonlocl = int("0")
ipstr, brstr = str(""), str("")
browsers = ['Mozilla','Firefox', 'Chrome', 'AppleWebKit'] # List of existing browsers
output = "" # empty output

with open('accesslog.txt') as f:
    for line in f:
        pat = '^(\d+\.\d+\.\d+\.\d+)\s(\-)\s(\-)\s(\[\d{2}\/[A-Za-z]*\/\d{4}\:\d{2}\:\d{2}\:\d{2}\s\+\d{4}\])\s\"(([^\"]*))\"\s(\d{3})\s([^\"]*)\s\"([^\"]*)\"\s\"([^\"]*)\"'
        line2 = line.replace('\\\"', '')
        mass.append(re.split(pat, line2))

for line in mass: # look at every line of the array
    brcount = 0
    match = re.match(r'^(10(\.(25[0-5]|2[0-4][0-9]|1[0-9]{1,2}|[0-9]{1,2})){3}|((172\.(1[6-9]|2[0-9]|3[01]))|192\.168)(\.(25[0-5]|2[0-4][0-9]|1[0-9]{1,2}|[0-9]{1,2})){2})$', str(line[1]))
    if not(match): # Check if IP is private or not
        nonlocl = nonlocl+1 # If not, adding 1 to the counter
        ip.append(line[1]) # And append IP to the list
    for i in browsers: # Now looping through browser list
        if i in line[10]: # If browser from list "browsers" exists in the log line
            brcount = brcount + 1 # add 1 to the counter
    if brcount == 0: # If no known browsers were found, append the user agent from log to the array
        bro = (line[10][:30] + '...') if len(line[10]) > 33 else line[10] # Trunkating long user agents 
        unknownbr.append(re.sub('[^A-Z a-z 0-9 , . / -]+', '', bro) + " (" + str(line[1]) + ")") # Delete special characters from browser string

ipset = set(ip) # Making two sets
brset = set(unknownbr) # to delete duplicates

if (len(ipset) != 0 or len(brset) != 0):
    if (len(ipset) != 0):
        output = output + "Unknown IPs:<code>\n"
        for line in ipset:
            cnt = ip.count(line)
            output = output + line + " (" + str(cnt) + ")\n"
        output = output + "</code>"
    if (len(brset) != 0):
        output = output + "Unknown browsers:<code>\n"
        for line in brset:
            output = output + line + "\n"
        output = output + "</code>\n"
    output = output + datetime.datetime.now().strftime("%Y.%m.%d %H:%M:%S") + "\n#honeybot #info"
    print(output)