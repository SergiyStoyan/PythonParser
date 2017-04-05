from lxml import etree

def StringifyChildren(node):
	from lxml.etree import tostring
	from itertools import chain
	parts = ([node.text]
		+ list(chain(*([tostring(c, with_tail=False), c.tail] for c in node.getchildren())))
		+ [node.tail]
	)
	# filter removes possible Nones in texts and tails
	return ''.join(filter(None, parts))
