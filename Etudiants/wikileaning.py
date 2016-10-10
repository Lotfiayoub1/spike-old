#!/usr/bin/python

import subprocess
import json
import re
import rospy
import std_msgs
import urllib

def listen_callback(msg, pub):
	""" Function receiving the callback data from the voice recognition.
	
	Args:
		msg (object): The return message from the subscriber callback.
		pub (rospy.Publisher): A publisher object used to return the process response.
	
	"""
	rospy.loginfo('eard: ' + msg.data)
	
	matches = re.match('(what is|who is) (.*)', msg.data, re.IGNORECASE)
	if (matches):
		topic = matches.group(2);
		text = topic + ' is ' + learn_specific(topic)
	
	else:
		text = 'Did you know ' + learn_random()
	
	rospy.loginfo(text)	
	pub.publish(std_msgs.msg.String(text))
	return

def learn_random():
	""" Allow to get and return to the synth a random wiki article. """
	article_id = get_random();
	rospy.loginfo('Article ID: ' + str(article_id))
	summary = get_summary(article_id)
	
	return summary;

def learn_specific(topic):
	""" Try to get an article about a specified topic and return it to the synth
	
	Args:
		topic_id (string): Name of the topic to search for on wikipedia.
	
	"""
	article_id = get_topic_id(topic)
	rospy.loginfo('Article ID: ' + str(article_id))
	summary = get_summary(article_id)
	
	return summary

def get_random():
	""" Get the id of a random article on wikipedia.
	
	Returns:
		(int) The id of the found article.
	
	"""
	
	api_url = 'https://en.wikipedia.org/w/api.php?format=json&action=query&list=random&rnnamespace=0'
	try:
		api_rtn = subprocess.check_output(['curl', '-X', 'GET', api_url])
		parsed_json = json.loads(api_rtn)
		rtn = parsed_json['query']['random'][0]['id']
		
	except subprocess.CalledProcessError as err:
		rtn = -1
	
	return rtn

def get_topic_id(topic):
	""" Get the id of a string topic.
	
	Args:
		topic (string): The topic to search for the id.
		
	Returns:
		(int) The id of the specified topic.
	
	"""
	
	api_url = 'https://en.wikipedia.org/w/api.php?format=json&action=query&titles=%s' % (urllib.quote(topic, safe=''))
	try:
		api_rtn = subprocess.check_output(['curl', '-X', 'GET', api_url])
		parsed_json = json.loads(api_rtn)
		rtn = parsed_json['query']['pages'].keys()[0]
	
	except subprocess.CalledProcessError as err:
		rtn = -1
	
	return rtn

def get_summary(article_id):
	""" Get the summary of the article.
	
	Args:
		article_id (int): The id of the article to request the summary.
		
	Returns:
		(array) Returns an array with the title of the article and the summary.
	
	"""
	
	if (article_id != -1):
		api_url = 'https://en.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exlimit=max&explaintext&exintro&redirects=&pageids=%s' % (article_id)
		api_rtn = subprocess.check_output(['curl', '-X', 'GET', api_url])
		parsed_json = json.loads(api_rtn)
		page_id = parsed_json['query']['pages'].keys()[0]
		summary = (parsed_json['query']['pages'][str(page_id)]['extract']).encode('utf8')
		rospy.loginfo('Article Summary: ' + summary)
		
	else:
		summary = 'Unable to complete request, no internet connexion is available.'
		rospy.loginfo('Unable to connect to internet to process request.')
	
	return summary

if __name__ == '__main__':
	# Useful variables
	listen_topic = 'topic_wiki'
	publish_topic = 'topic_speak_wiki'
	
	# Register the node
	rospy.init_node('node_wikileaning', anonymous=True)
	rospy.loginfo('Wiki Learning')
	
	# Register publisher
	pub = rospy.Publisher(publish_topic, std_msgs.msg.String, queue_size=10)
	rospy.loginfo('Publisher speak on: ' + publish_topic)
	
	# Register listener
	rospy.Subscriber(listen_topic, std_msgs.msg.String, listen_callback, pub)
	rospy.loginfo('Subscriber listening on: ' + listen_topic)
	
	# Make it spin!
	rospy.loginfo('Spinning...')
	rospy.spin()
