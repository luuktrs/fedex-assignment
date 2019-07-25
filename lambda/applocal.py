import sys
import logging
import aurora_config
import pymysql
import json
#aurora settings
aurora_host = "fedexassignment.cluster-chlyvkrllupx.us-east-2.rds.amazonaws.com"
name = aurora_config.db_username
password = aurora_config.db_password
db_name = aurora_config.db_name

try:
	conn = pymysql.connect(aurora_host, user=name, passwd=password, db=db_name, connect_timeout=5)
except pymysql.MySQLError as e:
	print("ERROR: Unexpected error: Could not connect to MySQL instance.")
	print(e)
	sys.exit()

print("SUCCESS: Connection to Aurora MySQL instance succeeded")
def handler(event, context):
	"""
	This function fetches content from MySQL Aurora instance
	"""

	item_count = 0
	hashtagCounters = []

	with conn.cursor() as cur:
		cur.execute("select hashtag, COUNT(*) AS count FROM hashtagdata GROUP BY hashtag ORDER BY count DESC LIMIT 10")
		for row in cur:
			item_count += 1
			hashtagCounters.append(row)
	conn.commit()
	conn.close()
	cur.close()

	return json.dumps(hashtagCounters) 

print handler("","")
