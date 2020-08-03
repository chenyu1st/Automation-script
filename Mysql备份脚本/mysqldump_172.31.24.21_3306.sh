#!/bin/sh
db_user="root"
db_passwd="123456"
db_host="localhost"

DICPATH=/data/backup/$HOSTNAME

LOGPATH=$DICPATH/log
DATPATH=$DICPATH/data

if [ ! -d $LOGPATH ]; then
        mkdir -p $LOGPATH
fi

if [ ! -d DATPATH ]; then
        mkdir -p $DATPATH
fi

backup_dir=$DICPATH
time="$(date +"%d-%m-%Y")"

MYSQL="/usr/local/mysql/bin/mysql"
MYSQLDUMP="/usr/local/mysql/bin/mysqldump"
MKDIR="/bin/mkdir"
RM="/bin/rm"
MV="/bin/mv"
GZIP="/bin/gzip"
sock="/data/mysql/mysql3306/mysql.sock"

# check the directory for store backup is writeable
test ! -w $backup_dir && echo "Error: $backup_dir is un-writeable." && exit 0

# the directory for story the newest backup
test ! -d "$backup_dir/backup.0/" && $MKDIR "$backup_dir/backup.0/"

# get all databases
all_db="$($MYSQL -u $db_user -h $db_host -p$db_passwd -Bse 'show databases')"
for db in $all_db
do
$MYSQLDUMP  -S $sock  -u $db_user -p$db_passwd --skip-lock-tables --opt --add-drop-database --add-drop-table --events --triggers --routines --default-character-set=utf8 --master-data=2  --single-transaction --complete-insert -d --quote-names --log-error=$backup_dir/mysqldump_db_$time.log $db | $GZIP -9 > "$backup_dir/backup.0/$time.$db.gz"
done

$MYSQLDUMP  -S $sock  -uroot -p$db_passwd --all-databases --opt --add-drop-database --add-drop-table --events --triggers --routines --default-character-set=utf8 --master-data=2  --single-transaction --complete-insert --quote-names  --log-error=$backup_dir/mysqldump$time.log | $GZIP -9 > "$backup_dir/backup.0/$time.all_mysql"

# delete the oldest backup
test -d "$backup_dir/backup.7/" && $RM -rf "$backup_dir/backup.7"
# rotate backup directory
for int in 6 5 4 3 2 1 0
do
if(test -d "$backup_dir"/backup."$int")
then
next_int=`expr $int + 1`
$MV "$backup_dir"/backup."$int" "$backup_dir"/backup."$next_int"
fi
done
exit 0;

