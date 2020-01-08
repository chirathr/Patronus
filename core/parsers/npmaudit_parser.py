from core.utils.elastic import elastic
from mysql.connector import errorcode
from core.utils.utils import Utils
from mysql.connector import Error
from config.config import Config
import mysql.connector
import configparser
import requests
import logging
import hashlib
import json
import uuid
import time
import os
import sys

class Npmauditparser():
	def __init__(self):
		self.es = elastic()
		self.utils = Utils()
		self.config = Config()

	def node_output(self, repo:str):
			if os.path.exists('%s%s/node_results.json' % (self.config.PATRONUS_DOWNLOAD_LOCATION, repo)):
				with open('%s%s/node_results.json' % (self.config.PATRONUS_DOWNLOAD_LOCATION, repo), encoding="utf8") as file:
					try:
						res = json.loads(file.read())
					except ValueError as e:
						logging.debug('Error could not load the json file for the project: %s' % (repo))
					for i in res['advisories']:
						try:
							issue = {'repo':repo, 'scanner': 'npm-audit', 'bug_type':'','language': 'nodejs', 'class_name':'', 'method_name':'', 'line_no_start':'', 'line_no_end':'','file_name': '', 'vulnerable_code':'', 'severity':'', 'module_name':'', 'advisories_url':'', 'vulnerable_versions':'', 'patched_versions':'', 'dependency_url':'', 'CVE':'', 'description':'', 'source_url':'', 'title':''}
							issue["module_name"] = res['advisories'][i]['module_name']
							issue["title"] = res['advisories'][i]['title']
							issue["severity"] = res['advisories'][i]['severity']
							issue["advisories_url"] = res['advisories'][i]['url']
							issue["vulnerable_versions"] = res['advisories'][i]['vulnerable_versions']
							issue["patched_versions"] = res['advisories'][i]['patched_versions']
							if self.utils.check_issue_exits(repo, str(issue)) == False and str(issue) != "":
								self.utils.sent_result_to_db(repo, str(issue), 'node-js', 'npm-audit')
								self.es.push_data_to_elastic_search(issue)
								self.utils.sent_to_slack(repo, json.dumps(issue, indent=4))
						except Exception as e:
							logging.debug("Error parsing json file for project %s. Error: %s" % (repo, e))
			return