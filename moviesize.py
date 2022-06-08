class Data:
	def __init__(self, width = 0, height = 0, size = 0, fps = 0, aspect_ratio = "16:9", length = 0):
		self.width = width																		# width in px
		self.height = height																	# height in px
		self.size = size																		# file size in bytes
		self.fps = fps																			# framerate in frames per second
		self.aspect_ratio = [int(a) / int(b) for a, b in [tuple(aspect_ratio.split(":"))]][0] 	# convert "x:y" to x/y (aspect ratio)
		self.length = length																	# length in seconds