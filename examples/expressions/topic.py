
#########################
# EXPERIMENT: Dialog
def load_topic():

	# load topic
	topic = nao.dialog.loadTopic("/home/nao/topics/startrek.top")
	nao.dialog.activateTopic(topic)
	nao.dialog.subscribe(topic)
	#dialog.startPush()

	return topic

# unload
def unload_topic():
	nao.dialog.deactivateTopic(topic)
	nao.dialog.unloadTopic(topic)
	nao.dialog.unsubscribe(topic)
	#undialog.stopPush()

# run
def go_topic():
	topic = load_topic()
	return topic