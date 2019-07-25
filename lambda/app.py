import sys
import logging
import aurora_config
import pymysql
#aurora settings
aurora_host  = "http://fedexassignment.cluster-chlyvkrllupx.us-east-2.rds.amazonaws.com"
name = aurora_config.db_username
password = aurora_config.db_password
db_name = aurora_config.db_name

logger = logging.getLogger()
logger.setLevel(logging.INFO)

try:
    conn = pymysql.connect(aurora_host, user=name, passwd=password, db=db_name, connect_timeout=5)
except pymysql.MySQLError as e:
    logger.error("ERROR: Unexpected error: Could not connect to MySQL instance.")
    logger.error(e)
    sys.exit()

logger.info("SUCCESS: Connection to Aurora MySQL instance succeeded")

def handler(event, context):
	hashtagCounters = []

	with conn.cursor() as cur:
		cur.execute("select hashtag, COUNT(*) AS count FROM hashtagdata GROUP BY hashtag ORDER BY count DESC LIMIT 10")
		for row in cur:
			hashtagCounters.append(row)
	conn.commit()
	conn.close()
	cur.close()

	return json.dumps(hashtagCounters) 
