from core.vcs.bitbucket import MyRemoteCallbacks
from core.sast.constants import Constants
from core.utils.elastic import elastic
from mysql.connector import errorcode
from mysql.connector import Error
from config.config import Config
from os.path import dirname
import mysql.connector
import configparser
import subprocess
import operator
import logging
import json
import os
import hashlib
import requests
import uuid
import time
import sys
import datetime
from datetime import timedelta



class Utils():
	def __init__(self):
		self.const = Constants()
		self.config = Config()

	def execute_cmd(self, command, repo):
		try:
			subprocess.run(command.split())
			logging.info("Executed command ` %s on project %s`" % (command, repo))
		except Exception as e:
			logging.debug("Error while executing command on project %s ` %s `" % (command, repo))
		return

	def run_cloc(self, repo:str):
		parent_dir = dirname(dirname(os.path.abspath(os.path.dirname(__file__))))
		os.chdir(parent_dir + '/tools')
		self.execute_cmd('cloc %s%s --json --out=%s%s/cloc.txt' % (self.config.PATRONUS_DOWNLOAD_LOCATION,repo,self.config.PATRONUS_DOWNLOAD_LOCATION, repo), repo)
		return

	def parse_cloc(self, repo:str):
		lang = self.config.PATRONUS_SUPPORTED_LANG
		lang_dict = {}
		
		if os.path.exists('%s%s/cloc.txt' % (self.config.PATRONUS_DOWNLOAD_LOCATION,repo)):		
			with open('%s%s/cloc.txt' % (self.config.PATRONUS_DOWNLOAD_LOCATION, repo)) as file:
				res = json.loads(file.read())
				if res.get('Java'):
					if res['Java']['nFiles']:
						lang_dict["java"] = res['Java']['nFiles']
				
				if res.get('JavaScript'):
					if res['JavaScript']['nFiles']:
						lang_dict["javascript"] = res['JavaScript']['nFiles']
				 
				if res.get('Go'):
					if res['Go']['nFiles']:
						lang_dict["go"] =  res['Go']['nFiles']
			return lang_dict

	def detect_programming_language(self, repo:str):
		"""
		"""
		self.run_cloc(repo)
		lang_dict = self.parse_cloc(repo)
		if lang_dict:
			return {'repo' : repo, 'lang' : max(lang_dict.items(), key=operator.itemgetter(1))[0]}
		return

	def sent_result_to_db(self, repo:str, text:str, language:str=None, scanner:str=None):
			try:
				connection = self.mysql_connection()
				sql_insert_query = "INSERT INTO results (scan_id, project_name, issue, language, scanner, hash) VALUES (%s, %s, %s, %s, %s, %s)"
				sid = uuid.uuid1()
				res_hash = hashlib.sha256(text.encode()).hexdigest()
				val = (str(sid), repo, text, language, scanner, res_hash)
				cursor = connection.cursor(prepared=True)
				try:
					result = cursor.execute(sql_insert_query, val)
					connection.commit()
				except mysql.connector.Error as error:
					logging.info("Error sending data to database for project :%s : Error %s" % (repo, error))
			except mysql.connector.Error as error:
				logging.debug("Error sending data sent to database for project %s" % (repo))
				connection.rollback()
			finally:
			    if(connection.is_connected()):
			        cursor.close()
			        connection.close()
			return

	def mysql_connection(self):
		try:
			connection = mysql.connector.connect(host=self.config.DB_HOST, database=self.config.DB_DATABASE, user=self.config.DB_USER, password=self.config.DB_PASSWORD)
		except:
			logging.info('Error connecting mysql')
		return connection

	def check_issue_exits(self, repo:str, text:str):
		issues_list = []
		try:
		    connection = self.mysql_connection()
		    sql_select_query = "SELECT hash from results WHERE project_name=%s"
		    res_hash = hashlib.sha256(text.encode()).hexdigest()
		    val = (repo,)
		    cursor = connection.cursor(prepared=True)
		    result = cursor.execute(sql_select_query, val)
		    res = cursor.fetchall()
		    for x in res:
		    	issues_list.append(x[0])
		    if res_hash in issues_list:
		    	return True
		    logging.info("Data does not exist for project %s" % (repo))
		except Exception as error:
			logging.debug("Error sending data sent to database for project %s. Error: %s" % (repo, error))
		finally:
			if (connection.is_connected()):
				cursor.close()
				connection.close()
		return False


	def sent_asset_to_db(self, repo:str, language:str):
			try:
				connection = self.mysql_connection()
				sql_insert_query = "INSERT INTO asset_inventory VALUES (%s, %s, %s, %s)"
				asset_id = uuid.uuid1()
				creation_date = datetime.datetime.now()
				val = (str(asset_id), repo, creation_date, language)
				cursor = connection.cursor(prepared=True)
				try:
					result = cursor.execute(sql_insert_query, val)
					connection.commit()
				except mysql.connector.Error as error:
					logging.info("Error sending asset to database for project :%s : Error %s" % (repo, error))
			except mysql.connector.Error as error:
				logging.debug("Error sending asset sent to database for project %s" % (repo))
				connection.rollback()
			finally:
			    if(connection.is_connected()):
			        cursor.close()
			        connection.close()
			return

	def check_asset_exits(self, repo:str, language:str):
		issues_list = []
		try:
		    connection = self.mysql_connection()
		    sql_select_query = "SELECT asset_name from asset_inventory WHERE asset_name=%s"
		    val = (repo,)
		    cursor = connection.cursor(prepared=True)
		    result = cursor.execute(sql_select_query, val)
		    res = cursor.fetchall()
		    for x in res:
		    	issues_list.append(x[0])
		    if repo in issues_list:
		    	return True
		    	logging.info("Asset %s exists" % (repo))
		    else:
		    	self.sent_asset_to_db(repo, language)
		    	logging.info("Asset %s Does not exists" % (repo))
		except Exception as error:
			logging.debug("Error sending data sent to database for project %s. Error: %s" % (repo, error))
		finally:
			if (connection.is_connected()):
				cursor.close()
				connection.close()
		return False

	def sent_asset_to_db(self, repo:str, language:str):
			try:
				connection = self.mysql_connection()
				sql_insert_query = "INSERT INTO asset_inventory VALUES (%s, %s, %s, %s)"
				asset_id = uuid.uuid1()
				creation_date = datetime.datetime.now()
				val = (str(asset_id), repo, creation_date, language)
				cursor = connection.cursor(prepared=True)
				try:
					result = cursor.execute(sql_insert_query, val)
					connection.commit()
				except mysql.connector.Error as error:
					logging.info("Error sending asset to database for project :%s : Error %s" % (repo, error))
			except mysql.connector.Error as error:
				logging.debug("Error sending asset sent to database for project %s" % (repo))
				connection.rollback()
			finally:
			    if(connection.is_connected()):
			        cursor.close()
			        connection.close()
			return

	def sent_to_slack(self, repo:str, data:str):
		url = self.config.PATRONUS_SLACK_WEB_HOOK_URL
		text = "Results for %s \n``` %s ```" % (repo, data)
		payload = {'text': text}
		requests.post(url, data=json.dumps(payload))	