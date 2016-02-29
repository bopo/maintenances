#!/bin/sh


URL[0]="http://www.linuxhostingtalk.com"
URL[1]="http://www.revolutionforums.org/vba.php"
URL[2]="http://www.tundraforum.org/forum.php"

len=${#URL[*]}
i=0

while [ $i -lt $len ]  
do
	HTTP_CODE=`curl -o /dev/null -s -w "%{http_code}" "${URL[$i]}"`

	if [ $HTTP_CODE != '200' ];then
		#`/usr/bin/php /root/PHPFetion.php ${URL[$i]}`
		echo "Web is not running"
	else
		echo "Web is running"
	fi
    let i++  
done
