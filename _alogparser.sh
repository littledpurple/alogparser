#!/bin/bash
cd /root/alogparser

host=""
ip=""
API=""
chat=""
mins=30

cat /var/log/httpd/access_log | grep -v "^..1"| awk -v minTime=$(date -d $mins' min ago' '+%Y%m%d%H%M%S') -f tst.awk > accesslog.txt

python alogparser.py $mins > msg.txt

[ ! -f "msg.txt" ] && { echo "Error: $0 file not found."; exit 2; }
 
if [ -s "msg.txt" ] 
then
	message=`cat msg.txt`
        message="<b>$host</b> $ip
$mins minute report
${message}"
        curl -F $"text="$'\U0001F514'" $message" -F "parse_mode=html" "https://api.telegram.org/bot$API/sendMessage?chat_id=$chat"
        curl -F document=@accesslog.txt "https://api.telegram.org/bot$API/sendDocument?chat_id=$chat"
fi

rm accesslog.txt
rm msg.txt