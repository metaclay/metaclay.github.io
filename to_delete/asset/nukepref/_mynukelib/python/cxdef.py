import nuke
import nukescripts
import sys, math
import operator
import random
import os
import cxclass
import re
import claystudio
import shlex
from nukescripts.panels import PythonPanel

# from hiero.core import *
# import hiero.ui
# import os



# GLOBAL VAR
cam_display_state=1
cknob_of_nodetab=['label','note_font','note_font_size','note_font_color','hide_input','cached','disable','dope_sheet','postage_stamp','postage_stamp_frame','lock_connections']
cknob_of_internal=['name', 'help', 'onCreate', 'onDestroy', 'knobChanged', 'updateUI', 'autolabel', 'panel', 'tile_color', 'gl_color', 'selected', 'xpos', 'ypos', 'icon', 'indicators', 'mapsize', 'window']
cknobno=cknob_of_nodetab+cknob_of_internal
cknobtx=['translate','rotate','scale','skew','center','invert_matrix','scaling','uniform_scale','pivot']
cknobtxfilter=['filter','clamp','black_outside']
cknobmblur=['motionblur','shutter','shutteroffset','shuttercustomoffset']
__all__='__ALL__'
clinebr='-------------------------------------'
clinebr2='+++++++++++++++++++++'
clinebr3='/////////////////////////////////////'
linebr=clinebr
cbr='\n'
cdagobj=['Node','Group','Gizmo','Viewer'] 
reprobj=cdagobj
gvm=0 #global verbose mode , used in debug mode
partition01=partition02=' ~ '
matrixnodes=['Camera','Axis','Light','Light2','Spotlight','DirectLight','Environment']
cstoken = 1 # check if connected to valid claystudio server


def convert_sequence_format(x,mode=0):
	import re
	if mode==0 : # convert ##### to %05d
		x=re.sub('#+',lambda x: '%0'+str(len(x.group()))+'d',x)
	else : # convert %05d to ##### 
		x=re.sub('%0([\d+])d', lambda x: int(x.group(1))*'#',x)
	return x


def cvarinit(val,valout=0):
	''' reset VALUE to VALOUT if the val is 0 or '' or [] or {} '''
	if val in [[],0,'',{},(),None]:
		return valout
	else :
		return val

def ccurlevel(node=None):
	''' return the path or level where current node is located , based on fullname of the Node'''
	''' ex: root/group1/Blur1 ---> level: root/group1/ '''
	if node :
		level=node.fullName().rpartition('.')[0] 
		level='root.'+level if level else 'root'
	else :
		if type(nuke.thisNode()).__name__!='PanelNode':
			level=nuke.thisNode().fullName()
			level='root.'+level if level !='root' else level
		else :
			level=''
	return level   

def clower_if_possible(x):
	''' convert to lower case if possible (if string) '''
	try:
		return x.lower()
	except AttributeError:
		return x

clipo=clower_if_possible 

def ccloseall_controlpanel():
	for node in nuke.allNodes(): 
		node.hideControlPanel()


def csave_preferences_to_file():
	'''
	Save current preferences to the prefencesfile in the .nuke folder.
	Pythonic alternative to the 'ok' button of the preferences panel.
	'''

	nukeFolder = os.path.expanduser('~') + '/.nuke/'
	preferencesFile = nukeFolder + 'preferences%i.%i.nk' %(nuke.NUKE_VERSION_MAJOR,nuke.NUKE_VERSION_MINOR)

	preferencesNode = nuke.toNode('preferences')

	customPrefences = preferencesNode.writeKnobs( nuke.WRITE_USER_KNOB_DEFS | nuke.WRITE_NON_DEFAULT_ONLY | nuke.TO_SCRIPT | nuke.TO_VALUE )
	customPrefences = customPrefences.replace('\n','\n  ')

	preferencesCode = 'Preferences {\n inputs 0\n name Preferences%s\n}' %customPrefences 

	# write to file
	openPreferencesFile = open( preferencesFile , 'w' )
	openPreferencesFile.write( preferencesCode )
	openPreferencesFile.close()


def renameShotToFolderName():
	#
	#nuke studio renaming shot name in timeline to folder continer name
	#
	# from hiero.core import *
	import hiero.core
	import hiero.ui
	import os

	seq= hiero.ui.activeSequence()
	te = hiero.ui.getTimelineEditor(seq)
	my_track_items=te.selection() 

	for ti in my_track_items:
		if isinstance(ti, hiero.core.TrackItem):
			media_source = ti.source().mediaSource()
			fi = media_source.fileinfos()[0] # assuming single file infos object
			folder_name = os.path.basename(os.path.dirname(fi.filename()))
			ti.setName(folder_name)


def cic(a,b):
	''' sort list by ignoring case -> to combine with x.sort() function'''
	''' usage: x.sort(cic) '''
	return cmp(clipo(a),clipo(b))


def crowcol_char(string='',mode=0,row=1,col=1):
	''' create 2d array list (matrix) '''    
	''' mode -> 0:use from string input 1:sequential number 2:seq of alpha lowercase 3: seq of alpha uppercase 4:random char'''
	if mode==0: # use input string
		corevar='string'
	elif mode==1: # sequential number
		corevar='x+(y*col)'
	elif mode==2: # seq alpha lowercase
		corevar='chr(97+ (((x)+(y*col))%26 )  )'
	elif mode==3: # seq alpha uppercase
		corevar='chr(97+ (((x)+(y*col))%26 )  ).upper()'
	elif mode==4: # random char
		corevar='chr(random.randint(97,122))'
	headvar='[[ '
	tailvar=' for x in range(col) ] for y in xrange(row)]'
	list = eval (headvar+corevar+tailvar)
	return list


def clist_lcase(list,uppercase=0):
	''' convert to upper or lower case ''' 
	if not uppercase:
		return [item.lower() for item in list if type(item).__name__ == 'str']
	else :
		return [item.upper() for item in list if type(item).__name__ == 'str']


def clist_lcase2(list,uppercase=0):
	''' convert to upper or lower case, same as above but using lambda/map function''' 
	if not uppercase:
		return [x.lower() if type(x).__name__=='str' else x for x in list]
	else :
		return [x.upper() if type(x).__name__=='str' else x for x in list]


def cremspace_from_str(mystr,mode=0):
	''' remove any white space '''
	''' mode-> 0:all 1:head 2:tail 3:head&tail '''
	if mode==0:
		mystr=mystr.replace(' ','')
	elif mode==1:
		mystr=mystr.lstrip()
	elif mode==2:
		mystr=mystr.rstrip()
	elif mode==3:
		mystr=mystr.strip()
	return mystr


def cremdupitem_from_list(list):
	''' remove duplicate item from list, no ignorecase feature available ''' 
	mydict = dict.fromkeys(list)
	list = list(mydict.keys())
	return list


def cremdupitem_from_list2(list,icase=0):
	''' remove duplicate item from list by storing unique value, icase:igonrecase '''
	outlist = []
	for element in list:
		if not icase :
			if element not in outlist:
				outlist.append(element)
		else :
			if (element.lower() if type(element).__name__=='str' else element) not in clist_lcase(outlist):
				outlist.append(element)            
	return outlist


def cfillstring(strx,strfill=' ',length=20):
	''' fill string with some char, example : test --> test********** '''
	''' length = maximum output string length '''
	strx=strx+(strfill * (length-len(strx)))
	return strx


def clist_from_string(mystr,sep=' ',lstrip=1,rstrip=1,remspace=0):
	''' 
	convert string to list by splitting using variable -sep 
	example : '  3   4     7  8' when sep by space(' ') , result: ['3', '4', '7', '8']
	example : '  22,  45 ,    3   ,9  ,100' sep by comma(','), result: ['22', '45', '3', '9', '100']
	remspace-> 0:remove all space 1:remove space and keep single space
	'''
	if type(mystr).__name__ != 'str' : mystr=str(mystr)
	listx=mystr.split(sep)    
	listout=[]
	for i in listx:
		i=i.lstrip() if lstrip else i
		i=i.rstrip() if rstrip else  i
		if remspace==1 :
			i=i.replace(' ','')
		elif remspace==2: 
			i=' '.join(i.split())
		listout.append(i) 
	listout=cremitem_from_list(listout,match=[''],matchmode=3)
	return listout


def cstring_match(stringtosearch,pattern,matchmode=0,matchcase=0,invmatch=0):
	'''
	match (pattern) to (string to search) 
	all elements will be typecast to string type 
	matchmode-> 0:any 1:head 2:tail 3:match all 
	matchcase-> 0:ignore case 1:case sensitive 
	invmatch-> inverse result
	'''
	# if elements are not string then force typecast to string.
	stringtosearch=str(stringtosearch)
	pattern=str(pattern)
	# match 
	if matchmode==0 : patternmatch='__string__.find(__pattern__)>=0'
	elif matchmode==1 : patternmatch='__string__.find(__pattern__)==0'
	elif matchmode==2 : patternmatch='__string__.rpartition(__pattern__)[2]=="" '
	elif matchmode==3 : patternmatch='__string__==__pattern__'
	patternmatch=patternmatch.replace('__string__','stringtosearch') if matchcase else patternmatch.replace('__string__','clower_if_possible(stringtosearch)')
	patternmatch=patternmatch.replace('__pattern__','pattern') if matchcase else patternmatch.replace('__pattern__','clower_if_possible(pattern)')
	match=eval(patternmatch)
	return match if not invmatch else not match


def cstring_matchlist(stringtosearch,patternlist,matchmode=0,matchcase=0,inversematch=0):
	''' matchmode> 0:any 1:head 2:tail 3:match all '''
	''' matchcase-> 0:ignore case 1:case sensitive '''
	''' patternlist is <list> '''
	match=True
	type1=type(stringtosearch).__name__
	if patternlist:
		for pattern in patternlist:
			type2=type(pattern).__name__
			if type1==type2=='str' :
				if pattern!='' :
					match=cstring_match(stringtosearch,pattern,matchmode,matchcase)  
				else :
					match=cstring_match(stringtosearch,pattern,3,matchcase)  
			else :
				match=True if stringtosearch==pattern else False
			if match : break
	return match if not inversematch else not match

citem_matchlist=cstring_matchlist


def cremitem_from_list(listx,itemtomatch='item',match=[],matchmode=0,matchcase=0,invmatch=0): 
	''' remove item from list'''
	''' invfilter-> 0:remove if match 1:remove if not match '''
	''' itemtomatch-> obj to be eval() to compare , example  : 'item':it self // 'item.name()':name attribute of the item  // 'item[0]':item index[0] '''
	''' '''
	listxref=listx[:]
	if match :    
		[listx.remove(item) if (citem_matchlist(eval(itemtomatch),match,matchmode,matchcase,invmatch)) else None for item in listxref] 
	return listx


def trim_header_space(docstring):
	if not docstring:
		return ''
	# Convert tabs to spaces (following the normal Python rules)
	# and split into a list of lines:
	lines = docstring.expandtabs().splitlines()
	# Determine minimum indentation (first line doesn't count):
	indent = sys.maxsize
	for line in lines[1:]:
		stripped = line.lstrip()
		if stripped:
			indent = min(indent, len(line) - len(stripped))
	# Remove indentation (first line is special):
	trimmed = [lines[0].strip()]
	if indent < sys.maxsize:
		for line in lines[1:]:
			trimmed.append(line[indent:].rstrip())
	# Strip off trailing and leading blank lines:
	while trimmed and not trimmed[-1]:
		trimmed.pop()
	while trimmed and not trimmed[0]:
		trimmed.pop(0)
	# Return a single string:
	return '\n'.join(trimmed)


def cremheaderspace_from_str(mystr):
	''' remove header space from multiline string '''
	mystr=mystr.split('\n')
	mystr=cremitem_from_list(mystr,match=[''],matchmode=3) #remove empty lines
	outstr=[ cremspace_from_str(strx,1) for strx in mystr] #remove header space from every lines
	outstr='\n'.join(outstr)
	return outstr


def cmstr_to_list(mystr,removemptyline=0, encap=0,remheaderspace=0,remtailspace=0):
	''' convert multi line string into list -> list:[line1, line2 , line3] '''
	''' removeemptyline-> remove empty line (line contain only white space)'''
	''' encap-> encapsulated everyline with symbol , example : xxxx -> ?xxxx? '''
	''' remhheaderspace/remtailspace -> remove any white space in head/tail of the line '''
	linelist=mystr.split('\n')
	if removemptyline: 
		linelist=cremitem_from_list(linelist,'',matchmode=3)
	list=[]
	for i in linelist:
		i=cremspace_from_str(i,1) if remheaderspace else i
		i=cremspace_from_str(i,2) if remtailspace  else i
		list.append(cencap(i)) if encap else list.append(i)
	return list


def cfindstring(string,pattern,icase=0):
	''' find string similar to string.find() but with ignorecase feature , icase:ignore case '''
	if icase:
		return string.lower().find(pattern.lower())
	else:
		return string.find(pattern)

def csortdict(dict,sortcase=0,keyidx=0):
	''' sorting the dictionary '''
	''' sortcase=> 0:sort by ignoring case 1:sort use case sensitivity '''
	''' keyidx=> 0:sort by key 1:sort by value '''
	return sorted(list(dict.items()), key=lambda x:clipo(x[keyidx])) if not sortcase else sorted(list(dict.items()), key=lambda x:x[keyidx])


def cireplace(str,old,new,count=0): 
	''' replace word in string without case sensitive ''' 
	pattern = re.compile(re.escape(old),re.I)
	return re.sub(pattern,new,str,count)


def cencap(str,strbegin="(",strend=")"):
	''' encapsulate string with char/str '''
	''' ex: mystring -> <mystring> '''
	strout=strbegin+str+strend
	return strout


def cclamp(val,lo,hi):
	return max(min(val,hi),lo)


def chex(n):
	''' format value into hexadecimal format , ex: 15->0f '''
	x = '%x' % (n,)
	return ('0' * (len(x) % 2)) + x


def rgb_to_hex(r,g,b):
	import random
	hexColour = int('%02x%02x%02x%02x' % (r*255,g*255,b*255,1),16)
	return hexColour	


def numpad(val,digit,pad,diff=0):
	''' convert numeric into digit padding : numberpad(123,6,'x')-> xxx123 '''
	''' diff-> 0:use digit as total digit -example: if digit=10 then 0012345678, 1:use digit as additional digit to add -example : digit=10 then 000000000012345678 '''
	val=str(val)
	if pad=='0' :
		val=val.zfill(digit)
	else :
		length=len(val)
		if diff : x=digit 
		else : x=digit-length
		for i in range(x) :
			val=pad+val
	return val


def ctccheckvalid(tc,fps=25):
	''' check if tc input is in valid format'''
	if tc=='' : tc='0'
	tc=tc.split(':') 
	length=len(tc)
	errmsg=''
	if length>4  :
		return 'error: too many digit'
	for i in range(length) :
		if not tc[i].isdigit() :
			return 'error: tc has to be numeric digit'
	for i in range(length-1):
		if int(tc[i])>=60 or int(tc[i]) <0:
			return 'error: h/m/s value has to be between 0-59'
	if int(tc[length-1])>=fps or int(tc[length-1])<0:
		return 'error: frame can not exceed fps'
	return errmsg


def ctcformatdigit(tc,fps=25):
	''' format tc so every segment will be in XX format, ex: 2:3:4 ->02:03:04'''
	err=ctccheckvalid(tc,fps)
	if not err:
		tc=tc.split(':')
		length=len(tc)
		for i in range(length):
			tc[i]=numpad(tc[i],2,'0')
		return ':'.join(tc)
	else:
		return err


def ctcpad(tc,fps=25):
	'''padding tc into format-> 00:00:00:00'''
	'''ex: 12:07 -> 00:00:12:07 '''
	err=ctccheckvalid(tc,fps)
	if not err:
		tc=ctcformatdigit(tc,fps)
		tcx=tc.split(':')
		length=len(tcx)
		return numpad(tc,4-length,'00:',1)
	else :
		return err


def ctctoframe(tc,fps=25):
	''' convert TC to framenumber'''
	err=ctccheckvalid(tc,fps)
	if not err :
		tc=ctcformatdigit(tc,fps)
		tc=ctcpad(tc,fps)
		arr=tc.split(':')
		hour=arr[0];min=arr[1];sec=arr[2];frm=arr[3]
		frametot = (int(hour)*60*60*fps)+(int(min)*60*fps)+(int(sec)*fps)+int(frm)
		return frametot
	else:
		return -1


def numberpad(val,digit,pad):
	#convert numeric into digit padding : numberpad(123,6,'x')-> xxx123
	val=str(val)
	length=len(val)
	if digit>length :
		i=0
		dif=digit-length
		padstr=''
		while i < dif:
			padstr=padstr+pad
			i=i+1
		val=padstr+val
	return val


def crandchar():
	''' generate a random character'''
	import random
	rand = random.randint(0,35)
	ch = chr(rand + 55)
	return ch


def cremap(val,inmin,inmax,outmin,outmax):
	''' remap value into different range'''
	diffin=inmax-inmin
	diffout=outmax-outmin
	diffval=val-inmin
	newval=outmin+((diffout/diffin)*diffval)
	return newval


def get_wh(node,whmode,expmode):
	''' return width/height of a node , whmode->0:center 1:w/h , expmode->0:numeric/value 1:expression'''
	if expmode :
		val=['width','height'] if whmode else ['width/2','height/2']
	else :
		w=node.width()
		h=node.height()
		val =[w,h] if whmode else [.5*w, .5*h]
	return val    

			
def charrepeatlist(check_string):
	# check how many times every unique char has been repeated
	# output data type is dictionary of every character used inside the string
	count = {}
	for s in check_string:
			if s in count:
				count[s] += 1
			else:
				count[s] = 1
	return count


def ischarrepeat(check_string,key):
	# check how many times selected char has been repeated
	# output data type is int
	count=charrepeatlist(check_string)
	if key in count :
		out=count[key]
	else :
		out=0
	return out


def getmatrix4(node,matrixname):
	''' 
	return a nuke.math.Matrix4 object with the transformations of a node
	"node" is the node object of any 3D node in Nuke
	that has a world or local matrix knob 
	'''
	try:
		nodeMatrix = nuke.math.Matrix4()
		for x in range(node[matrixname].width()):
			for y in range(node[matrixname].height()):
				nodeMatrix[x*4+y] = node[matrixname].value(y,x)
	except (NameError, AttributeError):
			nuke.message('Node %s does not have a valid world_matrix or local_matrix knobs.\nReturning the identity matrix instead' % node.name())
			nodeMatrix.makeIdentity()
	return nodeMatrix



def putmatrixtonode(matrix4,node):
	matrix4.transpose()
	node.knob('matrix').setValue(matrix4)


def distanceAxisToCard(axisNode, cardNode):
	''' 
	return the distance from an Axis, or any node with Axis-like knobs
	to the plane defined by a card
	'''
	axisMatrix = getMatrixFromNode(axisNode)
	cardMatrix = getMatrixFromNode(cardNode)
	v = nuke.math.Vector3(0,0,0)
	axisPosition = axisMatrix.transform(v)
	cardPosition = cardMatrix.transform(v)
	cardNormal = nuke.math.Vector3()  
	cardOrientation = cardNode['orientation'].value()
	cardNormal.set(int('X' not in cardOrientation), int('Y' not in cardOrientation), int('Z' not in cardOrientation))
	cardNormal = cardMatrix.inverse().ntransform(cardNormal)
	cardNormal.normalize()
	return cardNormal.dot(axisPosition-cardPosition)


def printformatmatrix(matrix,width=4,height=4,mode=0):
	for y in range (0,height):
		arr=''
		for x in range(0, width):
			val=matrix[x*height+y]
			if math.modf(val)[0]==0 and mode==1 : 
				val=int(val) 
			else:
				val="%0.8f" % (val)
			arr=arr+str( val)+'\t\t\t\t\t'
		print(arr)


def listradtodeg(radlist):
	deg=[]
	for rad in radlist:
		deg.append(math.degrees(rad))
	return deg


def listdegtorad(deglist):
	rad=[]
	for deg in deglist:
		rad.append(math.radians(deg))
	return rad


def createlistfrommatrix(v):
	# create list from matrix4 or vector
	list=[]
	for i in range(0,len(v)):
		list.append(v[i])
	return list

def creatematrixfromlist(list):
	# create matrix4/vector from list
	myMatrix = nuke.math.Matrix4()
	for val in matrixValues:
		myMatrix[matrixValues.index(val)] = val
	return myMatrix

def collect_allnodes(count=0,group=nuke.root()):
	''' 
	collect all nodes from current level downstream recursively
	e.g : 
	collect_allnodes() -> will collect all nodes
	collect_allnodes(group=nuke.toNode('root.Group1')) -> 
		collect all nodes start from 'group1' level downstream recursively
	'''
	group.begin() if count==0 else None
	nodes=nuke.allNodes()
	subnodes=[]
	for node in nodes :
		try:
			node.begin()
		except :
			pass
		else :
			recnodes=collect_allnodes(count+1,node)
			subnodes+=recnodes
	nodes+=subnodes
	return nodes

def collect_knobs(node,useglobalexclude=0,elist=[],excludemode=0,excludecase=0,classx=[],classxmode=0,classxcase=0,pattern=[],patternmode=0,patterncase=0,unsort=0,sortcase=0,keepnull=0,invmatchelist=0,invmatchclass=0,invmatchpat=0,useelist=1,useclassx=1,usepattern=1):
	''' collect all knobs from input node '''
	''' useglobalexclude= use global exclude list '''
	''' elist= additional exclude list '''
	''' excludemode= when apply excludelist (global + elist) 0: any 1:head 2:tail 3:match all '''    
	''' excludecase= when apply excludelist 0:ignore case 1:case sensitive '''
	''' classx=filtering the knob class(type)'''
	''' classxcase=similar to exclude case'''
	''' classxmode=similar to exclude mode'''
	''' pattern,patterncase,patternmode = similar to classx but filtering the name insted of class'''
	''' unsort= 0:sort output 1: unsort output '''
	''' sortcase= 0:ignore case when sorting output  1:case sensitive when sorting output '''
	''' keepnull= keep null/empty name '''
	knobs=getattr(node, 'allKnobs', lambda :'error')()
	if knobs !='error' :
		if useglobalexclude: excludelist=cknobno
		if useglobalexclude : knobs=cremitem_from_list(knobs,'item.name()',excludelist,3) # process globalexclude
		if not keepnull : knobs=cremitem_from_list(knobs,'item.name()',['',' '],3) # process keepnull
		if useelist : knobs=cremitem_from_list(knobs,'item.name()',elist,excludemode,excludecase, invmatchelist) # process elist
		if useclassx : knobs=cremitem_from_list(knobs,'item.Class()',classx,classxmode,classxcase,not invmatchclass) # process classx
		if usepattern : knobs=cremitem_from_list(knobs,'item.name()',pattern,patternmode,patterncase,not invmatchpat) # process pattern
		# sort
		if not unsort: 
			if sortcase:
				knobs.sort(key=lambda x:x.name()) #sort case sensitive
			else :
				knobs.sort(key=lambda x:x.name().lower()) #sort ignore case
	else :
		knobs=["%s <%s object> has no KNOBS attribute" %  (getattr(node,'name',lambda:node)(),type(node).__name__)]
	return knobs


def collect_class(nodes,unsort=0,sortcase=0,unique=1):
	''' collect classes of the input ~nodes '''
	''' unsort-> sort or not, 0:sort 1:no sort'''
	''' sortcase-> sort case sensitity, 0:ignore case 1:case sensitive'''
	listx= [getattr(node, 'Class', lambda :'error collect class')() for node in nodes ]
	if unique : listx=list(set(listx))
	if not unsort :
		if sortcase: listx.sort()
		else: listx.sort(cic)
	return listx


def collect_nodes_from_inout(node,recursive=0,diglevel=100,frominput=1,inputidx=-1,loop=0):
	'''
	recursive-> dig input/output stream recursively
	diglevel-> how deep to do recursive
	frominput-> 0:output stream 1:input stream
	inputidx-> input stream index -> node.input(inputidx) 
	loop=looping variable used in recursive process.
	'''
	if node :
		if loop <= diglevel :
			if frominput :
				if inputidx<0 :
					innum=node.inputs()
					nodes=[]
					for i in range(innum):
						if node.input(i) :
							nodes+=[node.input(i)]
				else :
					nodes=[node.input(inputidx)]
			else :
				nodes=node.dependent()
				nodes=nodes[:];[nodes.remove(nodex) if node not in collect_nodes_from_inout(nodex) else None for nodex in nodes] # temporary bugfix : bug-> dependent() anomali behaviour
			if recursive and nodes :
					loop+=1
					nodesx=[] 
					for node in nodes :
						collect=collect_nodes_from_inout(node,recursive,diglevel,frominput,inputidx=-1,loop=loop)
						nodesx+= collect if collect else []
					nodes+=nodesx
			if nodes : nodes=list(set(nodes)) #make unique
		else :
			nodes=[] 
	else :
		nodes=[]
	return nodes


def collect_nodes(sel=0,classx=[],classxmode=0,classxcase=0,pattern=[],patternmode=0,patterncase=0,unsort=0,sortcase=0,level='',externalblock=0,recursive=0,invmatchclass=0,invmatchpat=0,inputidx=-1,diglevel=100,tonodeinout='',run=0):
	'''
	COLLECT SELECTED OR ALL NODES 
	classx= filter by class, classx can be list or string 
	classxcase= case sensitivity when filtering 0:ignore 1:case sensitive 
	classxmode= mode how the classx is used-> 0:any 1:head 2:tail 3:match all
	sel= 0:all 1:selected 2:thisNode().input() 3:thisNode().dependent() 4:selectedNode().input() 5:selectedNode().dependent() 
	6: toNode().input() 7:toNode().dependent().
	level= set level to work with 
	unsort= sort the final output list 0:sort 1:no sort 
	sortcase= use or ignore case sensitivity when sorting -> 0:ignore 1:sensitive 
	patternmode= like classxmode but for pattern    
	patterncase= like classxcase but for pattern    
	pattern= pattern to match node's name , can be list or string     
	externalblock-> 1:use external block .begin() and end() and disable internal block 
	recursive->search node recursively when select nodes from output (dig down output tree) 
	invmatchclass/invmatchpat = mode to inverse the match logic (=> exclude vs include)
	inputidx = input index when grab from input , negative value means grab all input.
	diglevel-> how deep to dig recursively
	tonodeinout-> source for input/output stream, no need to write fullname.
	run-> 0:node 1:se 2:menu/panel
	'''

	# level process
	if run==0 : 
		levelx=nuke.thisParent()
		runfrom='dag'
	elif run==1 : 
		levelx=nuke.toNode(level)
		runfrom='se'
	else : 
		levelx=''
		runfrom='menu'
	oricurlevel=ccurlevel()
	if type(nuke.toNode(oricurlevel)).__name__ =='Node' :
		oricurlevel=ccurlevel().rpartition('.')[0]

	_sel_with_no_workinglevel_ = [2,3] #this value will run without working level
	_start_working_level_=(levelx!='' and sel not in _sel_with_no_workinglevel_ and not externalblock)
	levelx.begin() if _start_working_level_ else None 

	# get nodes list
	nodes=[]
	curlevel=ccurlevel()
	if sel==0: # all
		nodes=nuke.allNodes()
		if not nodes : cerr(msg="there's no node at all @%s"%curlevel)
	elif sel==1: # selected
		nodes =nuke.selectedNodes()
		if not nodes : cerr(msg="no selected node @%s"%curlevel)
	elif sel==2: # thisNode().input()
		if runfrom=='dag' :
			node=nuke.thisNode() 
			if node :
				nodes=collect_nodes_from_inout(node,recursive,diglevel=diglevel,inputidx=inputidx)
				if nodes :
					nodes=list(set(nodes)) 
				else :
					cerr(msg='node %s got no input stream'%('root.'+node.fullName()))
			else :
				cerr(msg='thisNode() execute:fail')
		else :
			cerr('(sel=3) thisNode() is N/A in non-DAG mode')
	elif sel==3: # thisNode().dependent() / output
		if runfrom=='dag' :
			node=nuke.thisNode() 
			if node :
				nodes=collect_nodes_from_inout(node,recursive,frominput=0,diglevel=diglevel)
				if nodes :
					nodes=list(set(nodes)) 
				else :
					cerr(msg='node %s got no output/dependent stream'%('root.'+node.fullName()))
			else :
				cerr(msg='thisNode() execute:fail')
		else :
			cerr('(sel=3) thisNode() is N/A in non-DAG mode')
	elif sel==4: # selectedNode().input()
		nodes=nuke.selectedNodes()
		if nodes :
			node=nodes[0] 
			nodes=collect_nodes_from_inout(node,recursive,diglevel=diglevel,inputidx=inputidx)
			if nodes :
				nodes=list(set(nodes)) 
			else :
				cerr(msg='node %s got no input stream'%('root.'+node.fullName()))
		else :
			cerr(msg="no selected node @%s"%curlevel)
	elif sel==5: # selectedNode().dependent() / output
		nodes=nuke.selectedNodes()
		if nodes :
			node=nodes[0] 
			nodes=collect_nodes_from_inout(node,recursive,frominput=0,diglevel=diglevel)
			if nodes :
				nodes=list(set(nodes)) 
			else :
				cerr(msg='node %s got no output/dependent stream'%('root.'+node.fullName()))
		else :
			cerr(msg="no selected node @%s"%curlevel)
	elif sel==6: # toNode().input()
		node = nuke.toNode(tonodeinout)
		if node :
			nodes=collect_nodes_from_inout(node,recursive,diglevel=diglevel,inputidx=inputidx)
			if nodes :
				nodes=list(set(nodes)) 
			else :
				cerr(msg='node %s got no input stream'%('root.'+node.fullName()))
		else : 
			cerr(msg="node %s doesn't exist " %tonodeinout)
	elif sel==7: # toNode().dependent() / output
		node = nuke.toNode(tonodeinout)
		if node :
			nodes=collect_nodes_from_inout(node,recursive,frominput=0,diglevel=diglevel)
			if nodes :
				nodes=list(set(nodes)) 
			else :
				cerr(msg='node %s got no output/dependent stream'%('root.'+node.fullName()))
		else : 
			cerr(msg="node %s doesn't exist " %tonodeinout)
	# levelx.end() if _start_working_level_ else None 
	#nuke.toNode(oricurlevel).end()

	# filtering
	if nodes :
		if classx in ['__all__','__ALL__',['__all__'],['__ALL__']] : classx=[]
		nodes=cremitem_from_list(nodes,'item.Class()',classx,classxmode,classxcase,not invmatchclass) # filter classx
		nodes=cremitem_from_list(nodes,'item.name()',pattern,patternmode,patterncase,not invmatchpat) # filter pattern
		if not unsort: 
			if sortcase:
				nodes.sort(key=lambda x:x.name()) #sort case sensitive
			else :
				nodes.sort(key=lambda x:x.name().lower()) #sort ignore case   
	return nodes   

def collect_into_pulldown(pulldownknob,listx=[],sep='',add_all_=0,extractlist=1):
	if listx :
		if not sep : sep=partition01
		listx =[(sep.join([str(x.__repr__() if (type(x).__name__ in reprobj or cstring_match(type(x).__name__,'_Knob',matchmode=2,matchcase=1) ) else x) for x in item]) if extractlist else item ) if type(item).__name__=='list' else (item.__repr__() if (type(item).__name__ in reprobj or cstring_match(type(item).__name__,'_Knob',matchmode=2,matchcase=1)) else item) for item in listx]

	listx=['__all__']+listx if add_all_ else listx
	pulldownknob.setValues(listx)
	pulldownknob.setValue(listx[0]) if listx else None


def caddknob_objpicker(node,tabname='cobjpicker_tab',tablabel='obj picker',listname='cobjpicker_select',listlabel=' select ',refreshbtnname='cobjpicker_refresh',refreshbtnlabel=' refresh ',grabselbtnname='cobjpicker_grabsel',grabselbtnlabel=' grab selected ',classtoselect=[],seqpadigitname=3,seqpadigitlabel=1,seqname=1,seqlabel=0,mode=0,nodemode=0,createtab=1,createrefresh=1,creategrab=1):
	''' this is automatioin for adding knob for picking object '''
	''' classtoselect-> filter by class '''
	''' seqpadigitname = padding/digit for name id '''
	''' seqpadigitlabel-> padding/digit for label'''
	''' seqlabel-> 0:label use no seqnumber 1:label use seqnumber'''
	''' mode-> 0:node picker 1:class picker 2:knob picker '''
	''' return last valid ID '''
	''' '''
	def check_id_exist(node):
		idx=0
		while node.knob(listname+numpad(idx,seqpadigitname,'0')) is not None:
			idx+=1
		return idx

	if seqname:
		idx=check_id_exist(node) # use to get available or valid id 
		idx1=numpad(idx,seqpadigitname,'0') # idx1=name id
		# idx2=cifelse(seqlabel,numpad(idx,seqpadigitlabel,'0'),'') 
		idx2=numpad(idx,seqpadigitlabel,'0') if seqlabel else ''  # idx2=label id
	else :
		idx1,idx2='',''
	if mode ==0 : #name
		exprbase='''
		p=this.knob('%s%s')
		listx=[x.name() for x in listx]
		cxdef.collect_into_pulldown(p,listx=listx)
		'''%(listname,idx1)
	elif mode==1 : #class
		exprbase='''
		p=this.knob('%s%s')
		listx=cxdef.collect_class(listx)
		cxdef.collect_into_pulldown(p,listx=listx)
		'''%(listname,idx1)
	elif mode==2 : #knobs
		exprbase='''
		p=this.knob('%s%s')
		node=listx[0] if listx else ''
		if node :
			knobs=cxdef.collect_knobs(node)
			knobs=[x.name() for x in knobs]
			cxdef.collect_into_pulldown(p,listx=knobs)
		else :
			print 'no selected node to fetch knobs'
		'''%(listname,idx1)

	exprbase='\n\n'+trim_header_space(exprbase)
	expr1="this=nuke.thisNode()\nlistx=cxdef.collect_nodes(0,classx=%s)"%classtoselect+exprbase
	expr2="this=nuke.thisNode()\nlistx=cxdef.collect_nodes(1,classx=%s)"%classtoselect+exprbase

	# define knob
	listknob=nuke.Enumeration_Knob(listname+idx1,listlabel+' '+idx2,[])
	refreshknob=nuke.PyScript_Knob(refreshbtnname+idx1,refreshbtnlabel+' '+idx2, expr1)
	grabselknob=nuke.PyScript_Knob(grabselbtnname+idx1,grabselbtnlabel+' '+idx2, expr2)    
	tabknob=nuke.Tab_Knob(tabname,tablabel)
	# create knob
	if not node.knob(tabname) : #if tab not exist ..
		node.addKnob(tabknob)     if createtab else None # ..then add tab
	error=[]
	if seqname :
		node.addKnob(listknob) # create pulldown list
		if mode!=2 : #  if mode is NOT KNOB picker..
			node.addKnob(refreshknob) if createrefresh else None #..add refresh
		node.addKnob(grabselknob) if creategrab else None # create grabsel button
	else :
		#error catcher : error if knob already exist.
		if node.knob(listknob.name()) : error.append(listknob.name())
		if node.knob(refreshknob.name()) : error.append(refreshknob.name())
		if node.knob(grabselknob.name()) : error.append(grabselknob.name())
		#execute if not error
		if error :
			error='knob exist :\n'+'\n'.join(error)
			nuke.message(error)
		else :
			node.addKnob(listknob) # create pulldown list
			node.addKnob(refreshknob) if createrefresh else None # create refresh 
			node.addKnob(grabselknob) if creategrab else None # create grabsel button
	return (idx1,error) # return last valid ID and error string

def caddknob_nodepicker(node,pulldownbtn=1,sortbtn=0,formatbtn=0,classxbtn=1,patternbtn=1,printbtn=0,pulldownlabel='nodes',name=''):
	idx='000';idn=idx
	if name and not name.isspace() : idx=name
	while node.knob('select_nodes_%s'%idx)  :
		if name and not name.isspace() :
			idx+=idn;id=int(idn);id+=1;idn=numpad(id,3,'0')
		else :
			id=int(idx);id+=1;idx=numpad(id,3,'0')
	cxclass.ccreate_nodes_el(None,obj=node,idx=idx,frompanel=0,sortbtn=sortbtn,formatbtn=formatbtn,printbtn=printbtn,classxbtn=classxbtn,patternbtn=patternbtn,pulldownbtn=pulldownbtn,pulldownlabel=pulldownlabel)
	cxclass.ccreate_nodesexpr_el(node,idx=idx,sortbtn=sortbtn,formatbtn=formatbtn,printbtn=printbtn,classxbtn=classxbtn,patternbtn=patternbtn,pulldownbtn=pulldownbtn)


def caddknob_knobpicker(node,pulldownbtn=1,sortbtn=0,formatbtn=0,elistbtn=1,classxbtn=1,patternbtn=1,printbtn=0,inputbtn=1,pulldownlabel='knobs',name=''):
	idx='000';idn=idx
	if name and not name.isspace() : idx=name
	while node.knob('select_knobs_%s'%idx)  :
		if name and not name.isspace() :
			idx+=idn;id=int(idn);id+=1;idn=numpad(id,3,'0')
		else :
			id=int(idx);id+=1;idx=numpad(id,3,'0')
	cxclass.ccreate_knobs_el(None,obj=node,idx=idx,frompanel=0,sortbtn=sortbtn,formatbtn=formatbtn,printbtn=printbtn,classxbtn=classxbtn,patternbtn=patternbtn,pulldownbtn=pulldownbtn,elistbtn=elistbtn,pulldownlabel=pulldownlabel,inputbtn=inputbtn)
	cxclass.ccreate_knobsexpr_el(node,idx=idx,sortbtn=sortbtn,formatbtn=formatbtn,printbtn=printbtn,classxbtn=classxbtn,patternbtn=patternbtn,pulldownbtn=pulldownbtn,elistbtn=elistbtn)

		
def cshakeclone():
	EXCLUSION_LIST = ["xpos","ypos","help","hide_input","note_font_color","onCreate","updateUI","knobChanged","note_font","tile_color","selected","autolabel","process_mask","label","onDestroy","inject","indicators","maskFrom","maskChannelMask","maskChannelInput","Mask","postage_stamp","disable","maskChannelMask", "panel", "maskFromFlag","name","cached","fringe", "maskChannelInput" , "note_font_size" , "filter", "gl_color","transform"]
	originals = nuke.selectedNodes()
	[ n['selected'].setValue(False) for n in nuke.allNodes() ]
	for original in originals:
		new = nuke.createNode(original.Class())
		for i in original.knobs():
			if i not in EXCLUSION_LIST:
								# Try to set the expression on the knob
				new.knob(i).setExpression("%s.%s" % (original.name(), original.knob(i).name()))
								# This will fail if the knob is an Array Knob...use setSingleValue to compensate
								# Thanks Hugh!
				if isinstance(new.knob(i), nuke.Array_Knob):
					new.knob(i).setSingleValue(original.knob(i).singleValue()) 
								# This will fail if the knob is a String Knob...use a TCL expression link to compensate
								# Thanks Michael!
				elif isinstance(new.knob(i), nuke.String_Knob): 
					new.knob(i).setValue("[value %s.%s]" % (original.name(), original.knob(i).name())) 
		new['selected'].setValue(False)    
	[ n['selected'].setValue(True) for n in originals ]


def cshowerr(mode):
	if mode=='input': msg='Pls connect Input ...'
	elif mode=='input': msg='Pls connect Input ...'
	nuke.message(msg)


def resetOffsetReadNode():
	nodes=nuke.selectedNodes()
	for node in nodes :
		if node.knob('frame_mode').value() == 'offset' :
			node.knob('frame').setValue('0')
		else :
			if node.knob('frame_mode').value()=='start at':
				node.knob('frame').setValue('1')


def ccenterglobal():
	x=nuke.selectedNode().width()
	y=nuke.selectedNode().height()
	out=cxclass.crectclass(0,0,x,y)
	return out
	
	
def crectnode(node):
	'''
	crectnode return instance of crectclass Class 
	usage: crectnode(Node) 
	'''
	x=node.width()
	y=node.height()
	out=cxclass.crectclass(0,0,x,y)
	return out


def delete_all_input_node():
	# _delete all input node 
	all=nuke.allNodes()
	for node in all :
		if node.name().rfind('Input')>=0 :
			nuke.delete(node)


def caddknob_nodepicker_combo():
	node=nuke.selectedNode()
	# MAIN KNOB
	idx=caddknob_objpicker(node,'cobjpicker_tab','node picker','cobjpicker_classlist','class','cobjpicker_refreshcls','refresh','cobjpicker_grabselcls','grab selected',classtoselect=[],mode=1)[0]
	caddknob_objpicker(node,'cobjpicker_tab','node picker','cobjpicker_nodelist','node','cobjpicker_refreshnode','refresh','cobjpicker_grabselnode','grab selected',classtoselect='[__classfilter__]',mode=0)
	caddknob_objpicker(node,'cobjpicker_tab','node picker','cobjpicker_channellist','channel','cobjpicker_refreshchan','refresh','cobjpicker_grabselchan','grab selected',classtoselect=[],mode=2)
	# ADDITIONAL KNOB
	node.addKnob(nuke.Boolean_Knob('cobjpicker_hidechannode'+idx,'hide chan node'))
	node.addKnob(nuke.Boolean_Knob('cobjpicker_hidechanint'+idx,'hide chan internal'))
	node.addKnob(nuke.String_Knob('cobjpicker_expr'+idx,' '))
	node.addKnob(nuke.Double_Knob('cobjpicker_value'+idx,' '))
	node.addKnob(nuke.Text_Knob('cobjpicker_divider'+idx,'',' '))
	# DEFAULT VALUE
	node.knob('cobjpicker_hidechannode'+idx).setValue(1)
	node.knob('cobjpicker_hidechanint'+idx).setValue(1)
	# DELETE UNWANTED KNOB
	node.removeKnob(node.knob('cobjpicker_grabselchan'+idx))
	# SET EXPR TO REFRESH BTN
	scr=node.knob('cobjpicker_refreshnode'+idx).command()
	scr='''
	this=nuke.thisNode()
	__classfilter__=this.knob('cobjpicker_classlist'''+idx+'''').value()\n'''+scr
	scr=cremheaderspace_from_str(scr)
	node.knob('cobjpicker_refreshnode'+idx).setCommand(scr)
	# SET EXPR TO GRAB BTN
	scr=node.knob('cobjpicker_grabselnode'+idx).command()
	scr=scr.replace('__classfilter__','')
	node.knob('cobjpicker_grabselnode'+idx).setCommand(scr)
	# PUT EXPR INTO LABEL
	scr='''
	[#--------- cobjpicker_channel__idx__ control ------------#
	python -exec {
	this=nuke.thisNode()
	# control channel autoupdate
	node=this.knob('cobjpicker_nodelist__idx__').value()
	if node!='0':
		allknobs=nuke.toNode(node).allKnobs()
		listx=[]
		excludelist=[]
		knob_exclude1=this.knob('cobjpicker_hidechannode__idx__').value()
		knob_exclude2=this.knob('cobjpicker_hidechanint__idx__').value()
		if knob_exclude1 : excludelist=excludelist+cxdef.cknob_of_nodetab
		if knob_exclude2 : excludelist=excludelist+cxdef.cknob_of_internal
		for knob in allknobs:
			if knob.name() not in excludelist:
				listx.append(knob.name())
				listx.sort(cxdef.cic)
		this.knob('cobjpicker_channellist__idx__').setValues(listx)
	# control exprfield
	expr=this.knob('cobjpicker_nodelist__idx__').value()+'.'+this.knob('cobjpicker_channellist__idx__').value()
	this.knob('cobjpicker_expr__idx__').setValue(expr)
	this.knob('cobjpicker_value__idx__').setExpression(expr)
	}]
	'''
	scr='\n\n'+trim_header_space(scr)
	scr=scr.replace('__idx__',idx)
	label=node.knob('label').value()
	print(label)
	label=label+scr
	node.knob('label').setValue(label)
	


def randchars(rowmax,colmax,countmax,word):
	''' create multiple random char/word '''
	''' word-> char/string to be repeated, if empty then use random() '''
	def getword(word):
		if word =='' :
			word=crandchar()
		return word

	text=''
	if countmax==0 :
		for i in range(rowmax):
			for j in range(colmax):
				text=text+getword(word)
			text=text+'\n'
	else :
		for i in range(countmax):
			text=text+getword(word)
	return text

def caddrootpathknob():
	def knobexist():
		knobtocheck = 'path'
		if nuke.root().knob(knobtocheck) :
			return 1
		else:
			return 0
	if not knobexist() :
		nuke.root().addKnob(nuke.EvalString_Knob('path','path'))
		pathknob=nuke.root().knob('path')
		pathknob.setValue('[file dirname [value root.name]]')


def chideknobsel(node,pattern='',mode=0):
	if mode==0 : # match all
		if node.knob(pattern) :
			node.knob(pattern).setVisible(not node.knob(pattern).visible())
	if mode==1 : # contain
		allknobs=node.allKnobs()
		if allknobs : 
			init=1
			for knob in allknobs:
				if knob.name().find(pattern)>=0 :
					knobobj =node.knob(knob.name())
					if init : 
						state=knobobj.visible()
						init=0
					knobobj.setVisible(not state)
		else :
			print('nothing to hide')
	if mode==2 : # start with
		allknobs=node.allKnobs()
		if allknobs :
			init=1
			for knob in allknobs:
				if knob.name().find(pattern)==0:
					knobobj =node.knob(knob.name())
					if init :
						state=knobobj.visible()
						init=0                    
					knobobj.setVisible(not state)
		else :
			print('nothing to hide')
	if mode==3 : # end with
		allknobs=node.allKnobs()
		if allknobs :
			init=1
			for knob in allknobs:
				if knob.name().rpartition(pattern)[2]=='':
					knobobj =node.knob(knob.name())
					if init :
						state=knobobj.visible()
						init=0                    
					knobobj.setVisible(not state)
		else :
			print('nothing to hide')

def cblink_value(ondur=3,offdur=0,starton=1,refstart=1):
	offdur=ondur if not offdur else offdur
	frame=nuke.frame()
	val=1 if ((frame-refstart)%(ondur+offdur))<ondur else 0
	if not starton : val= not val
	return val

def is_ascii(mystr,mode=0):
	'''
	check if string is all member of ascii
	mystr is unicode
	mode-> 0:0-127 , 1:128-255 , 2:0-255
	'''    
	if mode ==0 : # check standard ascii 0-127 
		return all(ord(c) < 128 for c in mystr)
	elif mode==1 : # check extended ascii 128-255
		return all((ord(c) >= 128 and ord(c) <256 ) for c in mystr)
	elif mode==2 : # check extended ascii 0-255
		return all( ord(c) <256  for c in mystr)
	elif mode==3 : # check extended ascii 0-255
		return all( ord(c) >=256  for c in mystr)



def collect_objdata(objs,unique=1,datas=['name()'],appendfail=0,unsort=0,sortcase=0,sortid=0,escape=1,showstringvalue=0,showbuttonvalue=0):
	''' 
	obj is object nodes/nodes etc which has attributes
	datas = list of attributes : ['Class()','name()'] etc.
	using ['_self_'] to fetch rawobject (repr)
	escape-> if inner-list or sub-list contain only single item, then escape it from LIST. 
	example: [['name'],['age']]become ['name','age']
	appendfail-> to add or not add the 'fail' result to the list.
	sortid-> which item inside list to be the index order, 
	example : ['name()','value()','Class()'] if want class() to be index order then  set sortid to: 2
	showstringvalue-> 0: do not show value() from _string_Knob (coz it will be too long)
	showbuttonvalue-> 0: do not show command/pyscript of a button_knob (too long)
	'''
	outlist=[]
	for obj in objs :
		itemdata=[]
		for data in datas :
			if data == '_self_' :
				objstr='obj'
			else:
				objstr='obj.'+data

			# check if fail
			fail=0
			try :
				objdata=eval(objstr)
			except AttributeError :
				objdata='fail@'+data
				fail=1
				print("object -%s- does not have -%s- attribute" %(getattr(obj,'name',lambda:obj)(),data) if data!='_self_' else "object -%s- error"%getattr(obj,'name',lambda:obj)())

			# show/hide value() of pyscript and string knob
			if not showbuttonvalue :
				if data=='value()' and type(obj).__name__ =='PyScript_Knob' :
					objdata='[expr]'
			if not showstringvalue :
				if data=='value()' and type(obj).__name__.find('String_')>=0 :
					objdata='[string]'

			# whether to add or not to add 'fail' data into final list.
			if appendfail :
				itemdata.append(objdata) 
			else :
				itemdata.append(objdata) if not fail else None

		# unique or not
		if unique :
			outlist.append(itemdata) if itemdata not in outlist else None
		else :
			outlist.append(itemdata)

	if outlist not in [[],[[]]] :
		# sorting
		if not unsort :
			if sortcase:
				outlist.sort(key=lambda x: x[sortid])
			else :
				outlist.sort(key=lambda x: clipo(x[sortid]))
		# escape item from list type into a non-list type
		if escape :
			if len(datas)==1 : outlist=[x[0] for x in outlist]
	return outlist

def cerr(msg='',mode=0,verbose=0):
	if not msg :
		if mode ==0 : msg='No Selected'
		elif mode==1 : msg='<empty>'
		elif mode==2 : msg='No Input'
	if verbose :
		nuke.message(msg)
	else :
		print(msg)


def getTheCornerpinAsMatrix():

	projectionMatrixTo = nuke.math.Matrix4()
	projectionMatrixFrom = nuke.math.Matrix4()

	#dir(projectionMatrix)
	theCornerpinNode = nuke.selectedNode()
	theNewCornerpinNode = nuke.createNode("CornerPin2D")
	theNewCornerpinNode['transform_matrix'].setAnimated()

	imageWidth = float(theCornerpinNode.width())
	imageHeight = float(theCornerpinNode.height())

	first = nuke.Root().knob('first_frame').getValue()
	first = int(first)
	last = nuke.Root().knob('last_frame').getValue()
	last = int(last)+1
	frame = first
	while frame<last:
		to1x = theCornerpinNode['to1'].valueAt(frame)[0]
		to1y = theCornerpinNode['to1'].valueAt(frame)[1]
		to2x = theCornerpinNode['to2'].valueAt(frame)[0]
		to2y = theCornerpinNode['to2'].valueAt(frame)[1]
		to3x = theCornerpinNode['to3'].valueAt(frame)[0]
		to3y = theCornerpinNode['to3'].valueAt(frame)[1]
		to4x = theCornerpinNode['to4'].valueAt(frame)[0]
		to4y = theCornerpinNode['to4'].valueAt(frame)[1]
	
		from1x = theCornerpinNode['from1'].valueAt(frame)[0]
		from1y = theCornerpinNode['from1'].valueAt(frame)[1]
		from2x = theCornerpinNode['from2'].valueAt(frame)[0]
		from2y = theCornerpinNode['from2'].valueAt(frame)[1]
		from3x = theCornerpinNode['from3'].valueAt(frame)[0]
		from3y = theCornerpinNode['from3'].valueAt(frame)[1]
		from4x = theCornerpinNode['from4'].valueAt(frame)[0]
		from4y = theCornerpinNode['from4'].valueAt(frame)[1]
	
		projectionMatrixTo.mapUnitSquareToQuad(to1x,to1y,to2x,to2y,to3x,to3y,to4x,to4y)
		projectionMatrixFrom.mapUnitSquareToQuad(from1x,from1y,from2x,from2y,from3x,from3y,from4x,from4y)
		theCornerpinAsMatrix = projectionMatrixTo*projectionMatrixFrom.inverse()
		theCornerpinAsMatrix.transpose()
	
		a0 = theCornerpinAsMatrix[0]
		a1 = theCornerpinAsMatrix[1]
		a2 = theCornerpinAsMatrix[2]
		a3 = theCornerpinAsMatrix[3]    
		a4 = theCornerpinAsMatrix[4]
		a5 = theCornerpinAsMatrix[5]
		a6 = theCornerpinAsMatrix[6]
		a7 = theCornerpinAsMatrix[7]   
		a8 = theCornerpinAsMatrix[8]
		a9 = theCornerpinAsMatrix[9]
		a10 = theCornerpinAsMatrix[10]
		a11 = theCornerpinAsMatrix[11]    
		a12 = theCornerpinAsMatrix[12]
		a13 = theCornerpinAsMatrix[13]
		a14 = theCornerpinAsMatrix[14]
		a15 = theCornerpinAsMatrix[15]
	
		theNewCornerpinNode['transform_matrix'].setValueAt(a0,frame,0)
		theNewCornerpinNode['transform_matrix'].setValueAt(a1,frame,1)
		theNewCornerpinNode['transform_matrix'].setValueAt(a2,frame,2)
		theNewCornerpinNode['transform_matrix'].setValueAt(a3,frame,3)    
		theNewCornerpinNode['transform_matrix'].setValueAt(a4,frame,4)
		theNewCornerpinNode['transform_matrix'].setValueAt(a5,frame,5)
		theNewCornerpinNode['transform_matrix'].setValueAt(a6,frame,6)
		theNewCornerpinNode['transform_matrix'].setValueAt(a7,frame,7)    
		theNewCornerpinNode['transform_matrix'].setValueAt(a8,frame,8)
		theNewCornerpinNode['transform_matrix'].setValueAt(a9,frame,9)
		theNewCornerpinNode['transform_matrix'].setValueAt(a10,frame,10)
		theNewCornerpinNode['transform_matrix'].setValueAt(a11,frame,11)
		theNewCornerpinNode['transform_matrix'].setValueAt(a12,frame,12)
		theNewCornerpinNode['transform_matrix'].setValueAt(a13,frame,13)
		theNewCornerpinNode['transform_matrix'].setValueAt(a14,frame,14)
		theNewCornerpinNode['transform_matrix'].setValueAt(a15,frame,15)
		frame = frame + 1


def cstring_divide(m,start='{',end='}'):
	# This will divide string into substring
	# divide by start and end
	# example : str="test this {first segment} and this is {second segment} ... {etc}"
	# output are 3 strings: '{first segment}' , '{second segment}' , '{etc}'
	scrarr=[]
	while m[m.find(start):m.find(end)+1] !='' :
		scrarr.append(m[m.find(start):m.find(end)+1])
		m=m[m.find(end)+2:]
	return scrarr
	
def cfind_lastkeyframe(knob,index=0,this_is_trackernode=0):
	# node is node object
	# knob is knob object
	# index is channel index -> x is 0, y is 1, etc.
	if this_is_trackernode:
		frame=max(knob.getKeyList())
	else :
		anim = knob.animation(index)
		if anim:
			keys = list(anim.keys())
			if keys:  # May be empty if knob is expression-driven
				frame = keys[-1].x
		return frame
	
def cfind_firstkeyframe(knob,index=0):
	# node is node object
	# knob is knob object
	# index is channel index -> x is 0, y is 1, etc.
	anim = knob.animation(index)
	if anim:
		keys = list(anim.keys())
		if keys:  # May be empty if knob is expression-driven
			frame = keys[0].x
	return frame
		
def canimation_indexrange(knob,framestart,frameend,idx):
	# this will return tupple of index : (indexstart,indexend) 
	# which match the timeline start and end frame.
	indexinrange=[]
	anim=knob.animation(idx)
	if anim :
		keys=list(anim.keys())
		for i in keys :	
			if (i.x >= framestart) and (i.x <=frameend) :
				indexinrange.append(keys.index(i))
	if indexinrange :
		return (indexinrange[0],indexinrange[-1])
	else :
		return ()


def cgetTrackNames(node):
	if node.Class()=='Tracker4':
		k=node['tracks']
	else :
		k=node['userTracks']

	s=k.toScript().split(' \n} \n{ \n ')
	s.pop(0)
	ss=str(s)[2:].split('\\n')
	ss.pop(-1)
	ss.pop(-1)
	outList=[]
	for i in ss:
		outList.append(i.split('"')[1])
	return outList

def cgetTrackNum(node):
	return len(cgetTrackNames(node))

def trimHeaderSpace(docstring):
	if not docstring:
		return ''
	# Convert tabs to spaces (following the normal Python rules)
	# and split into a list of lines:
	lines = docstring.expandtabs().splitlines()
	# Determine minimum indentation (first line doesn't count):
	indent = sys.maxsize
	for line in lines[1:]:
		stripped = line.lstrip()
		if stripped:
			indent = min(indent, len(line) - len(stripped))
	# Remove indentation (first line is special):
	trimmed = [lines[0].strip()]
	if indent < sys.maxsize:
		for line in lines[1:]:
			trimmed.append(line[indent:].rstrip())
	# Strip off trailing and leading blank lines:
	while trimmed and not trimmed[-1]:
		trimmed.pop()
	while trimmed and not trimmed[0]:
		trimmed.pop(0)
	# Return a single string:
	return '\n'.join(trimmed)



def cconnectpin_splinewarp(nodename):
	warpnode=nuke.toNode(nodename)
	warpcurve=warpnode['curves']
	warpscr=warpcurve.toScript()
	warproot=warpcurve.rootLayer
	pinlist=[ i for i in warproot if 'hold' not in i.name]
	connectstr=''
	for i in pinlist:
		connectstr=connectstr+'{edge '+i.name+'_hold '+i.name+' {cp 0 0 0 0 0 {{}}} {a}} '
	warpscr=warpscr[:-1]+connectstr+'}'
	warpcurve.fromScript(warpscr)

def ctracker_to_splinewarp():
	import RotopaintToSplineWarp_v2
	trclass=['Tracker4']
	camtrclass=['CameraTracker']
	if nuke.selectedNodes():
		trnode=nuke.selectedNodes()[0]
		if trnode.Class() in trclass or trnode.Class() in camtrclass :
			tracknum=len(cgetTrackNames(trnode))
			ronode=nuke.createNode('Roto')
			roknob=ronode.knob('curves')
			import nuke.rotopaint as rp
			if trnode.Class() in camtrclass:
				trknob=trnode.knob('userTracks')
				trcol=15
			else :
				trknob=trnode.knob('tracks')
				trcol=31
			keylist=trknob.getKeyList()
			framerangestr=str(keylist[0])+'-'+str(keylist[-1])
			framerange=nuke.FrameRange(framerangestr)

			ref=nuke.frame()

			for j in range(tracknum):
				arrx=[];arry=[]
				pin1=rp.Shape(roknob,type='bspline')
				pin2=rp.Shape(roknob,type='bspline')
				colx=(j*trcol)+2
				coly=(j*trcol)+3
				for i in framerange:
					arrx.append(trknob.getValueAt(i,colx))
					arry.append(trknob.getValueAt(i,coly))
				print(colx)
				print(arrx)
				hold=[trknob.getValueAt(ref,colx),trknob.getValueAt(ref,coly)]

				pinpoint=rp.ShapeControlPoint(0,0)
				for i in framerange:
					pinpoint.center.addPositionKey(i,(arrx[i-1],arry[i-1]))
				pin1.name='pin'+str(j)
				pin1.append(pinpoint)
				pin2.name='pin'+str(j)+'_hold'
				pin2.append(hold)

			warpnodename=RotopaintToSplineWarp_v2.Roto_to_WarpSpline_v2(framerangestr)
			ronode.knob('selected').setValue(True)
			nuke.nodeDelete()
			cconnectpin_splinewarp(warpnodename)	

		else:
			nuke.message('This is not a Tracker or Camera tracker node\nPlease select Tracker/CameraTracker node')	
	else:
		nuke.message('Please select Tracker node or Camera tracker node')



def setInOutCurViewer():
	ns=nuke.selectedNodes('FrameRange')
	if ns :
		n=ns[0]
		range=str(n.firstFrame())+'-'+str(n.lastFrame())
		viewer_node = nuke.activeViewer().node()
		viewer_node['frame_range_lock'].setValue(True) 
		viewer_node['frame_range'].setValue(range)


def beforeRender():
	import re
	def delete_proxy_label(input):
		if re.search('cxproxylabel',input.name()) :
			nuke.delete(input)

	def add_proxy_label():
		if nuke.root().proxy() :
			t=nuke.thisNode()
			height=t.height()
			xref=t.xpos()
			yref=t.ypos()
			input=t.input(0)
			textnode=nuke.nodes.Text(name='cxproxylabel')
			textnode.setXpos(xref)
			textnode.setYpos(yref-30)
			t.setInput(0,textnode)
			textnode.setInput(0,input)
			textnode.knob('font').setValue("/Library/Fonts/Arial.ttf")
			textnode.knob('message').setValue(' proxy')
			textnode.knob('yjustify').setValue('bottom')
			textnode.knob('size').setValue(50*(height/1080.0))

	def disable_reading():
		n = nuke.thisNode()
		reading = n.knob('reading').value()
		if reading :
			n.knob('reading').setValue(0)
			n.knob('cxreading').setValue(1)
		n.knob('disable').setValue(0)

	# t=nuke.thisNode()
	# input=t.input(0) 
	# if input:       
		# delete_proxy_label(input)
		# add_proxy_label()
		# disable_reading()


def afterRender():
	# import re
	# def deleteProxyLabel(input):
	# 	if re.search('cxproxylabel',input.name()) :
	# 		nuke.delete(input)

	# t=nuke.thisNode()
	# input=t.input(0)
	# if input :       
	# 	deleteProxyLabel(input)
	def enable_reading():
		n = nuke.thisNode()
		reading = n.knob('cxreading').value()
		color = 2275148031 # 2184464127
		if reading :
			n.knob('reading').setValue(1)
			n.knob('cxreading').setValue(0)
			n.knob('tile_color').setValue(color)

	enable_reading()




def knob_delkeyrange(knob,select=0,selected=0):
	# delete range of keyframe
	# select =0 (forward), 1 (backward), 2(range)
	node=knob.node()
	nodename=node.name()
	animated=nuke.animations()
	this_is_trackernode_w_tracksknob= 1 if   ((node.Class() in ['CameraTracker','Tracker4']) and (knob.name() in ['tracks','userTracks'])) else 0


	if this_is_trackernode_w_tracksknob :
		col=15 if node.Class()=='CameraTracker' else 31
		divider=5 if node.Class()=='CameraTracker' else 2
		def forward():
			frameend=max(knob.getKeyList())
			framestart=nuke.frame()
			return list(range(framestart+1,frameend+1))
		def backward():
			framestart=min(knob.getKeyList())
			frameend=nuke.frame()
			return list(range(framestart,frameend))
		def inrange():
			panel=cinput_range_panel()
			panel.showModalDialog()
			framestart=panel.knobs()['start'].value()
			frameend=panel.knobs()['end'].value()
			if framestart>frameend : framestart,frameend=frameend,framestart
			return list(range(framestart,frameend+1))
		setframevar={
			0:forward,
			1:backward,
			2:inrange,
			}			
		framerange=setframevar[select]()
		if selected :
			selectedanimated=[i for i in animated if not animated.index(i)%divider]
			selectedtrack=[int((i.partition('.')[2]).partition('.')[0])-1 for i in selectedanimated]
		else :
			length=len(cgetTrackNames(node))
			selectedtrack=list(range(0,length))

		for i in framerange:
			for column in selectedtrack:
				column=((column)*col)
				for m in [2,3]:
					knob.removeKeyAt(i,column+m) 
				if node.Class()=='Tracker4' : # delete additional channel if it's tracker node
					for m in [4,5,9,0]+list(range(21,31)):
						knob.removeKeyAt(i,column+m) 

	else :
		if animated :
			def forward():
				framestart=nuke.frame()+1
				frameend=1000000 #cfind_lastkeyframe(knob,index,this_is_trackernode)
				return (framestart,frameend)
			def backward():
				framestart=-1000000 #cfind_firstkeyframe(knob,index)
				frameend=nuke.frame()
				return (framestart,frameend)
			def inrange():
				panel=cinput_range_panel()
				panel.showModalDialog()
				framestart=panel.knobs()['start'].value()
				frameend=panel.knobs()['end'].value()
				if framestart>frameend : framestart,frameend=frameend,framestart
				return (framestart,frameend)
			setframevar={
				0:forward,
				1:backward,
				2:inrange,
				}	
			framerange=setframevar[select]()
			framestart=framerange[0]	
			frameend=framerange[1]
			def cchantoindex(x):
				return {
					'x': 0,
					'y': 1,
					'r': 0,
					'g': 1,
					'b': 2,
					'a': 3,	

				}[x]	

			for i in animated :
				if i.rfind('.')!= -1 :
					channame=str(i[i.rfind('.')+1:])
				else :
					channame='x'
				index=cchantoindex(channame)
				indexrange=canimation_indexrange(knob,framestart,frameend,index)
				if indexrange :
					if select==0 : #forward
						idxstart=indexrange[0]
						idxend=indexrange[1]+1
					elif select==1 : #backward
						idxstart=indexrange[0]
						idxend=indexrange[1]		
					else : #range
						idxstart=indexrange[0]
						idxend=indexrange[1]+1
					nuke.animation(nodename+'.'+i,'erase',( str(idxstart),str(idxend)  ))




def knob_print_info():
	''' print knob info '''
	x=nuke.thisKnob()
	print('knob info:')
	print('----------')
	print('name:',x.name())
	print('type:',x.Class())
	print()


def knob_setlock(knob,mode=0):
	''' mode-> 0:off 1:on 2:auto-toggle '''
	if mode==2 :
		state=knob.enabled()
		knob.setEnabled(not state)
	elif mode==1 or mode==0:
		knob.setEnabled(bool(mode))


def knob_link(mode):
	this=nuke.thisNode()
	knob=nuke.thisKnob()
	if mode==0 :
		inputx=this.input(0)
		if inputx :
			if inputx.knob(knob.name()) :
				scr='input0.'+knob.name()
				knob.setExpression(scr)
			else :
				print('input(0) got no knob %s' % knob.name())
	elif mode==1 :
		nodes=ccollect_nodes(1)
		if nodes :
			sel=nodes[0]
			if (sel.knob(knob.name())) :
				scr=sel.name()+'.'+knob.name()
				knob.setExpression(scr)
			else :
				print('%s got no knob %s' % (sel.name(),knob.name()))



def knob_noanim_and_reset(node,knob):
	knob.clearAnimated()
	if knob.name()=='center' :
		w=node.width()/2
		h=node.height()/2
		knob.setValue((w,h))
	else :
		knob.setValue(knob.defaultValue())



def knob_mpath():
	shPanel = ShapePanel( nuke.selectedNode() )
	if not shPanel.showModalDialog():
		return
	shapeName = shPanel.elementKnob.value()
	knob=nuke.thisKnob()
	this=nuke.thisNode()
	nodes=nuke.selectedNodes()
	if nodes :
		node=nodes[0]
		if not this.knob('mpath_control') : 
			this.addKnob(nuke.Double_Knob('mpath_control','motion path control'))
		this.knob('mpath_control').setRange(0,1)
		if knob.arraySize()==2 :
			scr1='''
			[python -execlocal {
			try:
			   shape = nuke.toNode("%s")['curves'].toElement("%s").evaluate(nuke.frame())
			except:
			   pass
			ret = shape.getPoint(nuke.thisNode()['mpath_control'].value()).x 
			}]''' % (node.name(),shapeName)

			scr2='''
			[python -execlocal {
			try:
			   shape = nuke.toNode("%s")['curves'].toElement("%s").evaluate(nuke.frame())
			except:
			   pass
			ret = shape.getPoint(nuke.thisNode()['mpath_control'].value()).y 
			}]''' % (node.name(),shapeName)

			scr1='\n\n'+ctrimheader_space(scr1)
			scr2='\n\n'+ctrimheader_space(scr2)	

			knob.setExpression(scr1,0)
			knob.setExpression(scr2,1)
		else :
			print('not apply to non-2 dimensional knob')
	else :
		print('no source path, select roto node') 


def knob_bmina(indexa=1,indexb=0):
	knob=nuke.thisKnob()
	knobname=knob.name()
	this=nuke.thisNode()
	if this.input(indexa) and this.input(indexb) :
		if not this.input(indexa).knob(knobname) : 
			print('input(%d) have no knob %s' % (indexa,knobname))
			return 0
		if not this.input(indexb).knob(knobname) :
			print('input(%d) have no knob %s' % (indexb,knobname))
			return 0
		scra='input%d.%s' % (indexa,knobname)
		scrb='input%d.%s' % (indexb,knobname)
		scr=scra+'-'+scrb
		knob.setExpression(scr)
	else :
		print('need 2 inputs')



def knob_set_whvalue(nodex,whmode=0,expmode=0,negative=0):
	''' 
	use to set knob value using right-click menu 
	nodex-> get wh data from ... 0:root 1:this/input 2:parent(group)
	whmode-> 0:center 1:w/h
	expmode-> 0:value 1:expression
	sign-> 0:positive 1:negative
	'''
	knob=nuke.thisKnob()
	if expmode :
		sign='-' if negative else ''
		if nodex==0 : node='root.'
		elif nodex==1 : node=''
		else : node='parent.'
		val=get_wh(node,whmode,expmode)
		for i in range(knob.arraySize()):
			knob.setExpression(sign+node+val[i],i)    
	else :
		sign=-1 if negative else 1
		if nodex==0 : node=nuke.root()
		elif nodex==1 : node=nuke.thisNode()
		else : node=nuke.thisParent()
		val=get_wh(node,whmode,expmode)
		for i in range(knob.arraySize()):
			knob.setValue(sign*val[i],i)

def remove_user_knobs():
	nodes=nuke.selectedNodes()
	for node in nodes :
		knob= []
		knobtab=[]
		for k in node.knobs():
			if isinstance(node.knob(k), nuke.Tab_Knob) : 
				knobtab.append(k)
			else :
				knob.append(k)
		knob+=knobtab
		for k in knob :
			if k != '' :
				try :
					node.removeKnob(node.knobs()[k])
				except ValueError:
					continue

		node.knob(0).setFlag(0)





def labelScriptTemplate():
	from cxsetting import __platform__
	import subprocess
	path=nuke.tcl("set x [getenv HOME]")+"/.nuke/_mynukelib/python/labelScript.txt"
	subprocess.call(["open", path])


def read(backdrop=0):
	from sys import platform
	import nukescripts , os , re
	from os.path import join,isfile,exists
	from cxsetting import __nukeremapid__ 

	def generic_read(param=''):
		fullpath = nuke.getClipname('Read')
		if fullpath : 
			fullpath=nuke.tcl("set x \""+fullpath+"\"")
			read=nuke.createNode('Read',param)
			read.knob('file').fromUserText(fullpath)

	param = "auto_alpha 1 before black frame_mode offset frame 0" # basic param for create READ node
	ns=nuke.selectedNodes()
 
	if ns :

		write_exist=0
		for n in ns:
			if n.Class()=='Write':
				write_exist=1
				break

		if write_exist :   
			nukescripts.clear_selection_recursive() # clear all selection
			readlist=[]

			for n in ns :
				if n.Class() == 'Write' : # if write node
					xposref = n.xpos(); yposref=n.ypos(); xdist=90
					proxyon = nuke.root().proxy()
	
					# set fullpath to file or proxy path depends on the proxyon state
					fullpath = n.knob('file').value() if not proxyon else ( n.knob('proxy').value() if n.knob('proxy').value() else n.knob('file').value() )
					fullpathori = fullpath
					fullpath = fullpath.strip()
					issequence = 0
					stillimage = 0
	
					if fullpath: # if path not empty
							fullpath = nuke.tcl('set x "'+fullpath+'"')
							stillimage = 1 if (checkFtype(fullpath)==3) else 0
	
							# cleanup colorspace data
							colorspace = n.knob('colorspace').value()
							if 'default' in colorspace :
								colorspace = colorspace.replace("default","") 
								colorspace = colorspace.strip()
								colorspace = colorspace[1:-1] # remove the bracket "(" and ")" from default value, example (sRGB) --> sRGB
								colorspace = colorspace.strip()
							param = ' colorspace "' + colorspace + '"'
	
							name = os.path.basename(fullpath)
							
							if re.search('#+',name) or re.search('%0\d+d',name) or re.search('%d',name) : 
								# if the sequence indicator suchs as # , %0xd or %d exists --> then this is sequence
								issequence = 1
								path = os.path.dirname(fullpath)
		
								# update path using remaps rule to match current OS
								remaps = nuke.toNode('preferences').knob("platformPathRemaps").toScript().split(';')
								remapnum = int(len(remaps)/3)
								for i in range(remapnum):
									if path.startswith(remaps[__nukeremapid__+(3*i)]):
										path = path.replace(remaps[__nukeremapid__+(3*i)],remaps[__nukeremapid__+(3*i)])
										break
										
								namesearch = name # name = os.path.basename(fullpath)
		
								# capture the sequence indicator %0xd , %d and
								# replace nuke style of sequence to regex pattern style and save pattern to 'namesearch'
								# this regex pattern then will be used to match and search the files
								# ex : %05d --> \d{5}
								# ------ namesearch=re.sub('[#]+',lambda x : '(\d{'+str(len(x.group()))+'})',namesearch)
								namesearch = re.sub('%0(\d+)d',lambda x : '(\d{'+str(x.group(1))+'})',namesearch)
								namesearch = re.sub('%d','(\\\d+)',namesearch)
		
								files = [i for i in os.listdir(path) if (isfile(join(path,i)) and re.search(namesearch,i) )] # find files using 'namesearch' containing regex pattern
		
								files = sorted(files)
								if files :
									firstfile = files[0]
									lastfile = files[len(files)-1]
									first = re.search(namesearch,firstfile).group(1) # get first index
									last = re.search(namesearch,lastfile).group(1) # get last index
									fullpath = os.path.join(path,name)+' ' +str(int(first))+'-' + str(int(last))
									if len(files) == 1 : stillimage = 1

							# create new READ node
							read = nuke.createNode('Read',param)
							readlist.append(read)
							read.setXpos(xposref+xdist)
							read.setYpos(yposref)
							read.knob('file').fromUserText(fullpath)
							read.knob("auto_alpha").setValue(1)
							read.knob("file").setValue(fullpathori)
	
							# if stillimage then hold the head/tail
							if stillimage :
								read.knob('before').setValue('hold')
								read.knob('after').setValue('hold')
							else :
								read.knob('before').setValue('black')
								read.knob('after').setValue('black')
		
							# if mov
							if not issequence and not stillimage :
								read.knob('frame_mode').setValue('start at')
								read.knob('frame').setValue(str(nuke.root().firstFrame()-nuke.root()['cxslateduration'].value()))
		
							if backdrop: 
								n.setYpos(n.ypos()+40)
		
							read.setXYpos(n.xpos(),n.ypos()+160)
	
							if backdrop :
								temp1 = nuke.nodes.Dot(); temp2=nuke.nodes.Dot()
								temp1.setXYpos(n.xpos()-40,n.ypos())
								temp2.setXYpos(n.xpos()+ 120,n.ypos())                       
								nukescripts.clear_selection_recursive()
								read.setSelected(1); n.setSelected(1);temp1.setSelected(1); temp2.setSelected(1)
								read.setXYpos(read.xpos(),read.ypos()+40)
								backdrop = nukescripts.autoBackdrop()
								n.setYpos(n.ypos()-40)
								nuke.delete(temp1)
								nuke.delete(temp2)
								backdrop['tile_color'].setValue(rgb_to_hex(.433,.498,.454))
								read.setXYpos(read.xpos(),read.ypos()-80)
							nukescripts.clear_selection_recursive() # clear all selected Nodes
							

					else :
						print('Path is empty.')
			for n in readlist :
				n.setSelected(True)
				return readlist
		else:
			generic_read(param)                            
	else :
		generic_read(param)



textcustom_util='''
	addUserKnob {20 User l util}
	addUserKnob {26 bboxdiv l bbox T " "}
	addUserKnob {22 bboxparent l " INPUT " T cxdef.textcustom_fitbox_to_input()  +STARTLINE}
	addUserKnob {22 bboxroot l " ROOT " T nuke.thisNode().knob('box').setValue((0,0,nuke.root().width(),nuke.root().height()))}
	addUserKnob {22 bboxhd l " HD 1920x1080 " T nuke.thisNode().knob('box').setValue((0,0,1920,1080))}

	addUserKnob {26 exprdiv l expr T " "}
	addUserKnob {22 getoutputlist l "  get output list  " T cxdef.textcustom_getoutputlist() +STARTLINE}
	addUserKnob {22 timecode l "  timecode  " T cxdef.textcustom_timecode()}
	addUserKnob {22 textmatrixexpr l "  inject text matrix EXPR  " T cxdef.textcustom_textmatrix_expr() +STARTLINE }
	addUserKnob {22 remtextmatrixknobs l "  remove text matrix knobs  " T cxdef.textcustom_remtextmatrix_knobs() }
	addUserKnob {22 typewriterexpr l "  inject typewriter EXPR  " T cxdef.textcustom_typewriter_expr() +STARTLINE }
	addUserKnob {22 remtypewriterknobs l "  remove typewriter knobs  " T cxdef.textcustom_remtypewriter_knobs() }
	addUserKnob {22 texttcexpr l "  inject text timecode EXPR  " T cxdef.textcustom_texttc_expr() +STARTLINE }'''

card_custom_util = '''
	addUserKnob {20 cgrid "cGrid"}
	addUserKnob {7 gridv l "grid V" R 1 250}
	gridv 10
	addUserKnob {7 gridh l "grid H" R 1 250}
	gridh {{gridv*(width/height)*pa}}
	addUserKnob {22 setlink l "set link" T cardutil_setlink() +STARTLINE}
	addUserKnob {22 makesquare l "make square grid expr" -STARTLINE T cardutil_makesquare()}
	addUserKnob {26 "" +STARTLINE}
	addUserKnob {7 pa R 0 5}
	pa 1
	addUserKnob {22 grabpa l "grab pixel aspect" -STARTLINE T cardutil_grabpa()}
	addUserKnob {20 util}
	addUserKnob {26 ImagePlane l "Image Plane " T :}
	addUserKnob {4 camlist l "select camera " M {}}
	addUserKnob {22 refreshcam l "refresh cam list" -STARTLINE T cardutil_refreshcamlist()}
	addUserKnob {22 linkiplane l "link image plane - hold cam" T cardutil_linkimageplanecamera() +STARTLINE}
	addUserKnob {22 linkiplane2 l "link image plane - hold card" T cardutil_linkimageplanecamera2() +STARTLINE}
	addUserKnob {26 ""}
	addUserKnob {22 Cardonground l "card on ground setup" T "node=nuke.thisNode()\n\nw=node.input(0).width()\nh=node.input(0).height()\noffset=node.knob('pivotoffset').value()\nval=(h/w)/2+offset\nnode.knob('pivot').setValue(-val,1)\nnode.knob('translate').setValue(val,1)" +STARTLINE}
	addUserKnob {7 pivotoffset l "    offset :  " -STARTLINE R -1 1}
	addUserKnob {22 topleft l + T "node=nuke.thisNode()\n\nw=node.input(0).width()\nh=node.input(0).height()\nval=(h/w)/2\nnode.knob('pivot').setValue(-.5,0)\nnode.knob('pivot').setValue(val,1)" +STARTLINE}
	addUserKnob {22 topmid l - -STARTLINE T "node=nuke.thisNode()\n\nw=node.input(0).width()\nh=node.input(0).height()\nval=(h/w)/2\nnode.knob('pivot').setValue(0,0)\nnode.knob('pivot').setValue(val,1)"}
	addUserKnob {22 topright l + -STARTLINE T "node=nuke.thisNode()\n\nw=node.input(0).width()\nh=node.input(0).height()\nval=(h/w)/2\nnode.knob('pivot').setValue(.5,0)\nnode.knob('pivot').setValue(val,1)"}
	addUserKnob {22 midleft l | T "node=nuke.thisNode()\n\nw=node.input(0).width()\nh=node.input(0).height()\nval=(h/w)/2\nnode.knob('pivot').setValue(-.5,0)\nnode.knob('pivot').setValue(0,1)" +STARTLINE}
	addUserKnob {22 center l x -STARTLINE T "node=nuke.thisNode()\n\nnode.knob('pivot').setValue(0,0)\nnode.knob('pivot').setValue(0,1)"}
	addUserKnob {22 midright l | -STARTLINE T "node=nuke.thisNode()\n\nw=node.input(0).width()\nh=node.input(0).height()\nval=(h/w)/2\nnode.knob('pivot').setValue(.5,0)\nnode.knob('pivot').setValue(0,1)"}
	addUserKnob {22 bottomleft l + T "node=nuke.thisNode()\n\nw=node.input(0).width()\nh=node.input(0).height()\nval=(h/w)/2\nnode.knob('pivot').setValue(-.5,0)\nnode.knob('pivot').setValue(-val,1)" +STARTLINE}
	addUserKnob {22 bottommid l _ -STARTLINE T "node=nuke.thisNode()\n\nw=node.input(0).width()\nh=node.input(0).height()\nval=(h/w)/2\nnode.knob('pivot').setValue(0,0)\nnode.knob('pivot').setValue(-val,1)"}
	addUserKnob {22 bottomright l + -STARTLINE T "node=nuke.thisNode()\n\nw=node.input(0).width()\nh=node.input(0).height()\nval=(h/w)/2\nnode.knob('pivot').setValue(.5,0)\nnode.knob('pivot').setValue(-val,1)"}'''

def cardutil_setlink():
	this=nuke.thisNode()
	this.knob('rows').fromScript('gridv')
	this.knob('columns').fromScript('gridh')

def cardutil_makesquare():
	this=nuke.thisNode()
	this.knob('gridh').fromScript('gridv*(width/height)*pa')

def cardutil_grabpa():
	nuke.thisNode().knob('pa').setValue(nuke.thisNode().input(0).pixelAspect())

def cardutil_refreshcamlist():
	cameralist=['Camera2','Camera']
	name=nuke.thisNode().name()
	group=nuke.root()
	group.begin()
	all =nuke.allNodes()
	list=[]
	for node in all :
		if node.Class() in cameralist :
			list.append(node.name())
	list.sort()
	group.end()
	nuke.toNode(name).knob('camlist').setValues(list)

def cardutil_linkimageplanecamera():
	this=nuke.thisNode()
	source=nuke.thisNode().knob('camlist').value()
	expr=source+".focal"
	expr2=source+".haperture"
	m=source+'.world_matrix'
	this.knob('lens_in_focal').fromScript(expr)
	this.knob('lens_in_haperture').fromScript(expr2)
	this.knob('z').setValue(1)
	this.knob('matrix').setExpression(m)
	this.knob('useMatrix').setValue(1)

def cardutil_linkimageplanecamera2():
	this=nuke.thisNode()
	card=this.name()
	source=nuke.thisNode().knob('camlist').value()
	cam=nuke.toNode(source)
	expr='(1/haperture)*focal*'+card+'.uniform_scale*'+card+'.scaling'
	cam.knob('translate').setExpression(expr,2)


def add_lock_knob(nodes):
	''' add lock knob & script --> for toggling lock '''	
	for node in nodes :
		if not node.knob('clock') :
			node.addKnob(nuke.Tab_Knob('util'))
			node.addKnob(nuke.Boolean_Knob('clock', 'lock'))
			scr='''
			[#------------- lock control ---------------
			python -exec {
			this=nuke.thisNode()
			state=not this.knob('clock').value()
			allknobs=this.allKnobs()
			for knob in allknobs:
				if knob.name() != 'clock':
					knob.setEnabled(state) 
			} 
			]
			'''
			scr='\n\n'+trim_header_space(scr)
			val=node.knob('label').value()+scr
			node.knob('label').setValue(val)


def nodePosition():
	selnodes=nuke.selectedNodes()
	if selnodes :
		print('----- Nodes Position -----\n')
		for node in selnodes:
			print(node.name()+'  X: '+str(node.xpos())+'   Y: '+str(node.ypos()))

def refreshallabel():
	nodes=nuke.allNodes()
	for node in nodes :
		data=node.knob('label').value()
		node.knob('label').setValue(data)

def cfade():
	nodes=nuke.selectedNodes()
	if nodes :
		inp=nodes[0].firstFrame()
		outp=nodes[0].lastFrame()
	else :
		inp=nuke.root().firstFrame()
		outp=nuke.root().lastFrame()
	cfade=nuke.createNode('cfade')
	cfade.knob('inp').setValue(inp)
	cfade.knob('outp').setValue(outp)
	cfade.knob('inp2').setValue(inp)
	cfade.knob('outp2').setValue(outp)
	cfade.knob('indur').setValue(0)
	cfade.knob('outdur').setValue(0)

def hide_knobs():	
	nodes=nuke.selectedNodes()
	if nodes :
		for node in nodes :
			allknobs = node.knobs()
			for k in allknobs:
				node.knob(k).setVisible(False)

def restore_knobs():
	nodes=nuke.selectedNodes()
	if nodes:
		for node in nodes :
			allknobs = node.knobs()
			for k in allknobs:
				node.knob(k).setVisible(True)


def knob_setlock(knob,mode=0):
	''' mode-> 0:off 1:on 2:auto-toggle '''
	if mode==2 :
		state=knob.enabled()
		knob.setEnabled(not state)
	elif mode==1 or mode==0:
		knob.setEnabled(bool(mode))


def lock_knobs(mode=0,toggleall=0,nodes=[]):
	''' mode-> 0:off 1:on 2:toggle'''
	''' toggleall in not equal to toggle in "mode" '''
	''' toggleall= set enabled-state for all knobs by checking only first knob condition, if first knob is enabled-ON then it will set OFF to all knobs '''
	''' in the other hand mode=0 (toggle) means , toggling knob enabled-state to its current state (per knob based) '''
	''' for doing per-knob toggle , invoke this -> callknobs_setlock(3) '''
	''' for doing toggleall, invoke -> callknobs_setlock(toggleall=1)'''
	nodes=nuke.selectedNodes()
	if nodes :
		for node in nodes :
			allknobs=node.allKnobs()
			mode= int(not allknobs[0].enabled()) if toggleall else mode # set mode based on first knob enable-state, to control all knobs enabled value.
			for knob in allknobs:
				knob_setlock(knob,mode)
			nuke.toNode(node.name()).setSelected(False)
			nuke.toNode(node.name()).setSelected(True)


def textcustom_remtypewriter_knobs() :
	this=nuke.thisNode()
	typewriterknobs=[]
	for knob in this.allKnobs() :
		typewriterknobs.append(knob) if knob.name().find('typewriter_')>=0 else None
	for knob in typewriterknobs :
		this.removeKnob(knob)


def textcustom_typewriter_expr() :
	this=nuke.thisNode()
	if not this.knob('typewriter_tab') :
		this.addKnob(nuke.Tab_Knob("typewriter_tab","typewriter"))
		this.addKnob(nuke.Double_Knob("typewriter_startframe","start frame"))    
		this.addKnob(nuke.Double_Knob("typewriter_chardur","char duration"))    
		this.addKnob(nuke.Double_Knob("typewriter_blinkondur","blink on dur"))    
		this.addKnob(nuke.Double_Knob("typewriter_blinkoffdur","blink off dur"))    
		this.addKnob(nuke.Enumeration_Knob("typewriter_endmode","end-mode",['hold','repeat','repeat down','blank']))    
		this.addKnob(nuke.Enumeration_Knob("typewriter_cursortype","cursor type",["0.no cursor" ,"1.underscore", "2.vertical line", "3.custom char"]))
		this.addKnob(nuke.String_Knob("typewriter_customcursor","custom cursor"))  
		blockstr='\u2580\u2588\u2590\u25a0\u2591\u2592\u2593\u2192'
		cursorblocklist=list(blockstr)
		id=0
		for i in cursorblocklist :
			blockname=i.encode('utf-8')
			this.addKnob(nuke.PyScript_Knob('typewriter_cursorblock'+str(id),blockname,'nuke.thisNode().knob("typewriter_customcursor").setValue(nuke.thisKnob().label())'))
			id+=1

		this.knob('typewriter_startframe').setValue(1)
		this.knob('typewriter_chardur').setValue(3)
		this.knob('typewriter_blinkondur').setValue(3)
		this.knob('typewriter_cursortype').setValue(1)
		this.knob('typewriter_blinkoffdur').setExpression('typewriter_blinkondur')
		this.knob('typewriter_startframe').setRange(1,200)
		this.knob('typewriter_chardur').setRange(1,10)
		this.knob('typewriter_blinkondur').setRange(1,10)
		this.knob('typewriter_blinkoffdur').setRange(1,10)
		this.knob('typewriter_customcursor').setValue('*')
		this.knob('typewriter_customcursor').clearFlag(nuke.STARTLINE)
		this.knob('typewriter_cursorblock0').setFlag(nuke.STARTLINE)
	if this.knob('message').toScript().find('###typewriter_expr_id###')<0 :
		expr ='''
		[python -execlocal {
		###typewriter_expr_id###
		text="""#--------- text here ----------------#
		__TEXT__
		"""#----------text end -----------------#
		text=text[39:len(text)-1]
		text=text.replace('\d', chr(153)) #del
		text=text.replace('\h', chr(168)) #hold
		text=text.replace('\e', chr(171)) #delrow
		this=nuke.thisNode()
		startframe=this.knob('typewriter_startframe').value()
		charduration=this.knob('typewriter_chardur').value()
		cursorblinkondur=this.knob('typewriter_blinkondur').value()
		cursorblinkoffdur=this.knob('typewriter_blinkoffdur').value()
		cursortype=int(this.knob('typewriter_cursortype').value()[0])
		frame=nuke.frame()-startframe

		idx=int(frame/charduration)+1
		if this.knob('typewriter_endmode').value()!='hold' :
			if this.knob('typewriter_endmode').value()=='repeat' :
				idx=idx%len(text) if idx>=0 else -(abs(idx)%len(text)) 
			elif this.knob('typewriter_endmode').value()=='blank' :
				idx=-1 if idx>len(text) else idx

		if this.knob('typewriter_endmode').value()=='repeat down' :
			text2=''
			for i in range(int(idx/len(text))):
				text2+='\\n'+text[:len(text)]
			text2+='\\n'+text[:idx%len(text)]
			text=text2
		else:
			text=text[:idx] if idx>=0 else "" #blank if idx is negative value

		cursor=''

		textout=[]
		for i in list(text):
			if i == chr(153) :
				textout.pop() if len(textout)>0 else None
			elif i == chr(168):
				pass
			elif i == chr(171) :
				if len(textout)>0 :
					idxx=len(textout)-1
					while textout[idxx]!= '\\n' and idxx>0 :
						textout.pop()
						idxx=idxx-1
					textout.pop()
			else :
				textout.append(i)
		if cursortype == 1:
			cursor='_' * cblink_value(cursorblinkondur,cursorblinkoffdur)
		elif cursortype == 2 :
			cursor='|' * cblink_value(cursorblinkondur,cursorblinkoffdur)
		elif cursortype == 3 :
			custchar=this.knob('typewriter_customcursor').value()
			cursor=custchar * cblink_value(cursorblinkondur,cursorblinkoffdur)
		textout=''.join(textout)+cursor if idx>=0 else ""  #blank if idx is negative value
		ret=textout
		}]
		'''
		expr=expr.replace('__TEXT__',this.knob('message').value())
		expr=trim_header_space(expr)
		this.knob('message').setValue(expr)


def replace_string_increment(source,srctext,replaceprefix,replacesuffix,startnumber,digit,filemode=1) :
	#mode=1 : from file input , mode=0 : from string variable 
	id=startnumber
	digitformat='%0'+str(digit)+'d'	
	if filemode :
		import fileinput
		file= fileinput.FileInput(source, inplace=True, backup='.bak') 
		for line in file:
			#print(line.replace(srctext, replaceprefix + digitformat%id + replacesuffix  ), end=' ')
			print(line.replace(srctext, replaceprefix + digitformat%id + replacesuffix  ))
			id+=1
		file.close()
	else :
		newstr=''
		lines=source.split(srctext)
		newstr += lines[0]
		for line in lines[1:] :
			newstr+= ( replaceprefix + ( (digitformat%id + replacesuffix) if startnumber>0 else '') ) + line 
			id+=1
		return newstr



def scripting_template(template):
	if template=='class' :
		string="""
		class xx(nukescripts.PythonPanel):
			''' doc '''    
			def __init__(self):
				nukescripts.PythonPanel.__init__(self, 'xx panel', 'claystudio.nuke.xx_panel')

				# CREATE KNOBS
				self.input= nuke.String_Knob('x')
				self.addKnob(self.input)

		x=xx()
		x.show()
		"""
	else :
		None
	string=trim_header_space(string)
	print(string)

def textcustom_getoutputlist():
	import os 
	selected = nuke.selectedNodes('Write')
	num=len(selected)
	if selected :
		i=0
		msg='fullpath :\n-------------\n'
		msg2='basename :\n-------------\n'
		while i < num :
			file =selected[i].knob('file').value()
			msg+=file
			msg2+=os.path.basename(file)
			i=i+1  
		msg+='\n\n'+msg2
	else :
		msg='pls select write node.'
	nuke.thisNode().knob('message').setValue(msg)

def list_filter(datalist,includelist,excludelist=['<<!--emptylist--!>>'],matchall=0,case=0,strip=1,removempty=1) :
	#matchall=1 match all includelist, matchall=0 match any includelist
	includelist=[''] if includelist==[] else includelist
	excludelist=['<<!--emptylist--!>>'] if excludelist==[''] else excludelist
	orilist=datalist[:]
	if not case :
		datalist=[i.lower() for i in datalist]    
		includelist=[i.lower() for i in includelist]    
		excludelist=[i.lower() for i in excludelist]    
	if strip:
		datalist=[i.strip() for i in datalist]
		includelist=[i.strip() for i in includelist]    
		excludelist=[i.strip() for i in excludelist]    
	if matchall :
		outlist = [i for i in datalist if not any(j in i for j in excludelist) and all(j in i for j in includelist)]
	else :
		outlist = [i for i in datalist if not any(j in i for j in excludelist) and any(j in i for j in includelist)]
	if removempty :
		outlist=[i for i in outlist if i.strip()!='']
	if not case :
		outlist=[i for i in orilist if i.lower() in outlist]

	return outlist


def textcustom_fitbox_to_input():
	this=nuke.thisNode()
	if this.input(0) :
		w=this.input(0).width()
		h=this.input(0).height()
		this.knob('box').setValue([0,0,w,h])
		this.knob('center').setValue([w/2,h/2])


def textcustom_matrix(textcustom_util):
	x=nuke.createNode('Text', textcustom_util)
	x.knob('yjustify').setValue('top')
	x.knob('textmatrixexpr').execute()	

def textcustom_number(textcustom_util):
	param='''
	message "[frame]"
	size 200
	xjustify "center"
	'''
	param=trim_header_space(param)
	x=nuke.createNode('Text', param+textcustom_util)

def merge_this():
	''' create 2d OR 3d transform, based on type of selected Node '''
	try:
		node=nuke.selectedNode()
	except ValueError:
		return nuke.createNode( 'Merge2' )
	else:
		if 'render_mode' in node.knobs():
				return nuke.createNode( 'MergeGeo' )
		else:
				return nuke.createNode( 'Merge2' )

def go_render():
	import os
	nodes = nuke.selectedNodes()
	
	def disable_reading(n):
		reading = n.knob('reading').value()
		autodisable = n.knob('cxautodisable').value()
		if reading :
			n.knob('reading').setValue(0)
			n.knob('cxreading').setValue(1)
			if autodisable :
				n.knob('disable').setValue(0)
		
		

	for n in nodes:
		if n.Class()=='Write' :
			proxyon=nuke.root().proxy()
			name=n.name()
			pathtcl=n.knob('file').evaluate() if not proxyon else n.knob('proxy').evaluate()
			if pathtcl :
				path=nuke.tcl("set x \""+pathtcl+"\"")
				dirname=os.path.dirname(path)
				direxists=1
				if not os.path.exists(dirname):
					if nuke.ask('Folder does not exist. Do you want to create ?') :
						os.makedirs(dirname)
					else :
						direxists=0
				if direxists :		
					first = n.firstFrame()
					last = n.lastFrame()
					disable_reading(n)
					try :
						nuke.render( n.name(), first, last, 1 )
					except Exception as e :
						nuke.message("ERR : "+str(e))
			else :
				nuke.message("Proxy path is empty." if proxyon else "File path is empty")

def textcustom_textmatrix_expr():
	this=nuke.thisNode()
	if not this.knob('textmatrix_tab') :
		this.addKnob(nuke.Tab_Knob("textmatrix_tab","text matrix"))
		this.addKnob(nuke.Double_Knob("textmatrix_count","count"))    
		this.addKnob(nuke.String_Knob("textmatrix_word","word"))
		this.knob('textmatrix_count').setValue(300)
	if this.knob('message').toScript().find('###textmatrix_expr_id###')<0 :
		expr ='''[python -execlocal {
		###textmatrix_expr_id###
		count=int(nuke.thisNode().knob('textmatrix_count').value())
		word=nuke.thisNode().knob('textmatrix_word').value()
		ret=cxdef.randchars(0,0,count,word)
		}]
		'''
		expr=trim_header_space(expr)
		this.knob('message').setValue(expr)

def textcustom_remtextmatrix_knobs():
	this=nuke.thisNode()
	textmatrixknobs=[]
	for knob in this.allKnobs() :
		textmatrixknobs.append(knob) if knob.name().find('textmatrix_')>=0 else None
	for knob in textmatrixknobs :
		this.removeKnob(knob)

def textcustom_texttc_expr():
	this=nuke.thisNode()
	texttc_expr='''
	[metadata input/timecode]
	[python -exec {
	import cdefinition
	fps=24
	tc=nuke.tcl('metadata input/timecode')
	frame=cdefinition.ctctoframe(tc,fps)
	}]frame :[python frame]	([python fps] fps)
	'''
	texttc_expr=trim_header_space(texttc_expr)
	this['message'].setValue(texttc_expr)


def textcustom_timecode():
	this=nuke.thisNode()
	this['bboxparent'].execute()
	this['message'].setValue('TC [metadata input/timecode]\nFRAME [python ctctoframe("[metadata input/timecode]",[metadata input/frame_rate])]\nFPS [metadata input/frame_rate]')
	this['font'].setValue('/Library/Fonts/Arial Black.ttf')
	this['yjustify'].setValue(3)



def paste(branch=0,src='') :

	def paste_branch(n):
		dot=nuke.createNode('Dot')
		nukescripts.remove_inputs()
		n.setSelected(True)
		nuke.nodePaste("%clipboard%")
		dot.setInput(0,n)
		nuke.delete(dot)


	selection = nuke.selectedNodes()
	src='%clipboard%' if src=='' else src
	if not selection:
		nuke.nodePaste(src)
		return
	for node in selection:
		node['selected'].setValue(0)
	for node in selection:
		node['selected'].setValue(1)
		nuke.nodePaste(src) if not branch else paste_branch(node)
		node['selected'].setValue(0)

def cross():
	n=nuke.createNode('ccross')
	input=n.input(0)
	tx= input.width()/2 if input else nuke.root().width()/2
	ty= input.height()/2 if input else nuke.root().height()/2
	n.knob('translate').setValue([tx,ty])

def ramp():
	x='''
	addUserKnob {20 util_tab l cx}
	addUserKnob {22 util_hor l Horizontal T "w=nuke.root().width()\nh=nuke.root().height()\nnuke.thisNode()\['p0'].clearAnimated()\nnuke.thisNode()\['p0'].setValue((0,0))\nnuke.thisNode()\['p0'].setExpression('0',1)\nnuke.thisNode()\['p1'].clearAnimated()\nnuke.thisNode()\['p1'].setValue((w,0))\nnuke.thisNode()\['p1'].setExpression('0',1)" +STARTLINE}
	addUserKnob {22 util_ver l Vertical -STARTLINE T "w=nuke.root().width()\nh=nuke.root().height()\nnuke.thisNode()\['p0'].clearAnimated()\nnuke.thisNode()\['p1'].clearAnimated()\nnuke.thisNode()\['p0'].setValue((0,h))\nnuke.thisNode()\['p1'].setValue((0,0))\nnuke.thisNode()\['p0'].setExpression('0',0)\nnuke.thisNode()\['p1'].setExpression('0',0)"}
	addUserKnob {22 util_free l Free -STARTLINE T "w=nuke.root().width()\nh=nuke.root().height()\nnuke.thisNode()\['p0'].clearAnimated()\nnuke.thisNode()\['p1'].clearAnimated()\nnuke.thisNode()\['p0'].setValue((0,0))\nnuke.thisNode()\['p1'].setValue((w,h))"}
	addUserKnob {22 util_invert l Invert -STARTLINE T "buffer1x=float(nuke.tcl('value this.p0.x'))\nbuffer1y=float(nuke.tcl('value this.p0.y'))\nbuffer2x=float(nuke.tcl('value this.p1.x'))\nbuffer2y=float(nuke.tcl('value this.p1.y'))\nnuke.thisNode()\['p0'].setValue((buffer2x,buffer2y))\nnuke.thisNode()\['p1'].setValue((buffer1x,buffer1y))"}
	'''
	nuke.createNode('Ramp',x)

def radial():
	x='''
	area {{-radius+shift.x} {(-radius2*pixel_aspect)+shift.y} {radius+shift.x} {(radius2*pixel_aspect)+shift.y}}
	softness 0
	addUserKnob {20 cxutil l cx}
	addUserKnob {22 squareexpr l "inject radius expr" -STARTLINE T "this=nuke.thisNode()\nradius=this.knob('radius')\nx1='-radius+shift.x'\nx2='(-radius2*pixel_aspect)+shift.y'\nx3='radius+shift.x'\nx4='(radius2*pixel_aspect)+shift.y'\nthis.knob('area').setExpression(x1,0)\nthis.knob('area').setExpression(x2,1)\nthis.knob('area').setExpression(x3,2)\nthis.knob('area').setExpression(x4,3)"}
	addUserKnob {22 linkhv l " link hv " -STARTLINE T "this=nuke.thisNode()\nthis.knob('radius2').setExpression('useaspect?radius/pixel_aspect:radius')"}
	addUserKnob {22 unlinkhv l " unlink hv " -STARTLINE T nuke.thisNode().knob('radius2').clearAnimated()}
	addUserKnob {26 ""}
	addUserKnob {7 radius l "radius h" R 0 2000}
	radius 200
	addUserKnob {7 radius2 l "radius v" R 0 2000}
	radius2 {{useaspect?radius/pixel_aspect:radius}}
	addUserKnob {12 shift l center}
	shift {320 240}
	addUserKnob {22 setcenterinput l " input center " -STARTLINE T "this=nuke.thisNode()\nif this.input(0) :\n        x=this.input(0).width()/2\n        y=this.input(0).height()/2\nelse:\n        x=nuke.root().width()/2\n        y=nuke.root().height()/2\nthis.knob('shift').clearAnimated()\nthis.knob('shift').setValue(\[x,y])"}
	addUserKnob {22 setcenterinputexpr l " input center expr " -STARTLINE T "this=nuke.thisNode()\nx='input.width/2'\ny='input.height/2'\nthis.knob('shift').setExpression(x,0)\nthis.knob('shift').setExpression(y,1)\n"}
	addUserKnob {22 setcenterroot l " root center " -STARTLINE T "this=nuke.thisNode()\nx=nuke.root().width()/2\ny=nuke.root().height()/2\nthis.knob('shift').clearAnimated()\nthis.knob('shift').setValue(\[x,y])"}
	addUserKnob {6 useaspect l "use pixel aspect" +STARTLINE}
	useaspect true
	'''
	nuke.createNode('Radial', x)

def multiply():
	x='''
	addUserKnob {20 cx}
	addUserKnob {7 opacity l "opacity (max)"}
	opacity 1
	addUserKnob {3 inp l IN}
	inp 1
	addUserKnob {22 setinp l set -STARTLINE T "n=nuke.thisNode()\nlock=n.knob('lockindur').value()\nn.knob('inp').setValue(nuke.frame())\ninp=n.knob('inp').value()\nif lock :\n   dur=n.knob('indur').value()\n   n.knob('inp2').setValue(inp+dur)\nelse :\n   inp2=n.knob('inp2').value()\n   dur= inp2 -inp\n   n.knob('indur').setValue(dur)"}
	addUserKnob {22 decinp l < -STARTLINE T "n=nuke.thisNode()\nlock=n.knob('lockindur').value()\n\nval=n.knob('inp').value()\nval=val-1\nval2=n.knob('inp2').value()\nval2=val2-1\nval3=n.knob('indur').value()\nval3=val3+1\nn.knob('inp').setValue(val)\nif lock :\n   n.knob('inp2').setValue(val2)\nelse :\n   n.knob('indur').setValue(val3)"}
	addUserKnob {22 incinp l > -STARTLINE T "n=nuke.thisNode()\nlock=n.knob('lockindur').value()\n\nval=n.knob('inp').value()\nval=val+1\nval2=n.knob('inp2').value()\nval2=val2+1\nval3=n.knob('indur').value()\nval3=val3-1\nn.knob('inp').setValue(val)\nif lock :\n   n.knob('inp2').setValue(val2)\nelse :\n   n.knob('indur').setValue(val3)"}
	addUserKnob {22 grabinp l "grab input" -STARTLINE T "n=nuke.thisNode()\ninput=n.input(0)\nif input :\n   inp=input.firstFrame()\nelse :\n   inp=nuke.root().firstFrame()\n\nn.knob('inp').setValue(inp)\nn.knob('inp2').setValue(inp)"}
	addUserKnob {3 inp2 l IN2}
	inp2 1
	addUserKnob {22 setinp2 l set -STARTLINE T "\nn=nuke.thisNode()\nlock=n.knob('lockindur').value()\nn.knob('inp2').setValue(nuke.frame())\ninp2=n.knob('inp2').value()\nif lock :\n   dur=n.knob('indur').value()\n   n.knob('inp').setValue(inp2-dur)\nelse :\n   inp=n.knob('inp').value()\n   dur= inp2 -inp\n   n.knob('indur').setValue(dur)"}
	addUserKnob {22 decinp2 l < -STARTLINE T "n=nuke.thisNode()\nlock=n.knob('lockindur').value()\n\nval2=n.knob('inp2').value()-1\nval=n.knob('inp').value()-1\nval3=n.knob('indur').value()-1\nn.knob('inp2').setValue(val2)\nif lock :\n   n.knob('inp').setValue(val)\nelse :\n   n.knob('indur').setValue(val3)"}
	addUserKnob {22 incinp2 l > -STARTLINE T "n=nuke.thisNode()\nlock=n.knob('lockindur').value()\n\nval2=n.knob('inp2').value()+1\nval=n.knob('inp').value()+1\nval3=n.knob('indur').value()+1\nn.knob('inp2').setValue(val2)\nif lock :\n   n.knob('inp').setValue(val)\nelse :\n   n.knob('indur').setValue(val3)"}
	addUserKnob {7 indur l "fadein dur" R 0 50}
	addUserKnob {6 lockindur l lock -STARTLINE}
	addUserKnob {26 ""}
	addUserKnob {3 outp2 l OUT2}
	outp2 100
	addUserKnob {22 setoutp2 l set -STARTLINE T "n=nuke.thisNode()\nlock=n.knob('lockoutdur').value()\nn.knob('outp2').setValue(nuke.frame())\noutp2=n.knob('outp2').value()\nif lock :\n   dur=n.knob('outdur').value()\n   n.knob('outp').setValue(outp2+dur)\nelse :\n   outp=n.knob('outp').value()\n   dur= outp - outp2\n   n.knob('outdur').setValue(dur)"}
	addUserKnob {22 decoutp2 l < -STARTLINE T "n=nuke.thisNode()\nlock=n.knob('lockoutdur').value()\n\nval=n.knob('outp').value()-1\nval2=n.knob('outp2').value()-1\nval3=n.knob('outdur').value()+1\nn.knob('outp2').setValue(val2)\nif lock :\n   n.knob('outp').setValue(val)\nelse :\n   n.knob('outdur').setValue(val3)"}
	addUserKnob {22 incoutp2 l > -STARTLINE T "n=nuke.thisNode()\nlock=n.knob('lockoutdur').value()\n\nval=n.knob('outp').value()+1\nval2=n.knob('outp2').value()+1\nval3=n.knob('outdur').value()-1\nn.knob('outp2').setValue(val2)\nif lock :\n   n.knob('outp').setValue(val)\nelse :\n   n.knob('outdur').setValue(val3)"}
	addUserKnob {3 outp l OUT}
	outp 100
	addUserKnob {22 setoutp l set -STARTLINE T "n=nuke.thisNode()\nlock=n.knob('lockoutdur').value()\nn.knob('outp').setValue(nuke.frame())\noutp=n.knob('outp').value()\nif lock :\n   dur=n.knob('outdur').value()\n   n.knob('outp2').setValue(outp-dur)\nelse :\n   outp2=n.knob('outp2').value()\n   dur= outp - outp2\n   n.knob('outdur').setValue(dur)"}
	addUserKnob {22 decoutp l < -STARTLINE T "n=nuke.thisNode()\nlock=n.knob('lockoutdur').value()\n\nval=n.knob('outp').value()-1\nval2=n.knob('outp2').value()-1\nval3=n.knob('outdur').value()-1\nn.knob('outp').setValue(val)\nif lock :\n   n.knob('outp2').setValue(val2)\nelse :\n   n.knob('outdur').setValue(val3)"}
	addUserKnob {22 incoutp l > -STARTLINE T "n=nuke.thisNode()\nlock=n.knob('lockoutdur').value()\n\nval=n.knob('outp').value()+1\nval2=n.knob('outp2').value()+1\nval3=n.knob('outdur').value()+1\nn.knob('outp').setValue(val)\nif lock :\n   n.knob('outp2').setValue(val2)\nelse :\n   n.knob('outdur').setValue(val3)"}
	addUserKnob {22 graboutp l "grab input" -STARTLINE T "n=nuke.thisNode()\ninput=n.input(0)\nif input :\n   outp=input.lastFrame()\nelse :\n   outp=nuke.root().lastFrame()\n\nn.knob('outp').setValue(outp)\nn.knob('outp2').setValue(outp)"}
	addUserKnob {7 outdur l "fadeout dur" R 0 50}
	addUserKnob {6 lockoutdur l lock -STARTLINE}
	addUserKnob {26 ""}
	addUserKnob {22 fadescript l "fade script" -STARTLINE T "n=nuke.thisNode()\nscr='valfadein*valfadeout  * opacity'\nn.knob('value').setExpression(scr)\nfadeinscr='frame<inp?0:(frame>=inp+indur)?1:(1/(indur+1))*(frame+1-inp)'\nfadeoutscr='frame>outp?0:(frame<=outp-outdur?1: (1/(outdur+1)*abs(outp-frame+1)))'\nn.knob('valfadein').setExpression(fadeinscr)\nn.knob('valfadeout').setExpression(fadeoutscr)"}
	addUserKnob {22 getrange l "get range from input" -STARTLINE T "n=nuke.thisNode()\ninput=n.input(0)\nif input :\n   inp=input.firstFrame()\n   outp=input.lastFrame()\nelse :\n   inp=nuke.root().firstFrame()\n   outp=nuke.root().lastFrame()\n\nn.knob('inp').setValue(inp)\nn.knob('inp2').setValue(inp)\nn.knob('outp').setValue(outp)\nn.knob('outp2').setValue(outp)"}
	addUserKnob {7 valfadein l INVISIBLE +INVISIBLE}
	valfadein {{frame<inp?0:(frame>=inp+indur)?1:(1/(indur+1))*(frame+1-inp) x16 0 x38 1}}
	addUserKnob {7 valfadeout l INVISIBLE +INVISIBLE}
	valfadeout {{"frame>outp?0:(frame<=outp-outdur?1: (1/(outdur+1)*abs(outp-frame+1)))" x73 1 x100 0}}
	'''
	nuke.createNode('Multiply',x)	

def grid():
	x='''
	addUserKnob {20 User l cx}
	addUserKnob {22 squaregridexpr l "  square grid expr  " T "nuke.thisNode().knob('number').setValue(0,1)\nnuke.thisNode().knob('number').setExpression('number.0*height/width',1)\n" +STARTLINE}
	'''	
	nuke.createNode('Grid', x)

def frame_hold():
	x='''
	addUserKnob {20 cx}
	addUserKnob {41 first_frame_1 l "first frame" T this.first_frame}
	addUserKnob {22 set -STARTLINE T nuke.thisNode().knob('first_frame').setValue(nuke.frame())}
	addUserKnob {22 goto l "go to" -STARTLINE T "frame=nuke.thisNode().knob('first_frame').value()\nnuke.frame(frame)"}
	addUserKnob {41 increment_1 l increment T this.increment}
	'''
	hold=nuke.createNode('FrameHold',x   )
	hold.knob('first_frame').setValue(nuke.frame())
	
def particleEmitter():
	param='''
	addUserKnob {20 "cx"}
	addUserKnob {26 onepulse T " "}
	addUserKnob {3 onepulse_rate l "rate"}
	onepulse_rate 1
	addUserKnob {3 onepulse_first l "at frame"}
	addUserKnob {22 onepulse_setfirst l "set" -STARTLINE T "nuke.thisNode().knob('onepulse_first').setValue(nuke.frame())"}
	addUserKnob {3 onepulse_dur l "   duration" }
	onepulse_first 0
	onepulse_dur 1
	addUserKnob {22 onepulse_setexpr l "  inject expr  "  +STARTLINE}
	addUserKnob {22 onepulse_auto l "  auto template  " -STARTLINE}
	'''
	
	scr1='''
	this=nuke.thisNode()
	rate=this.knob('onepulse_rate').value()
	first=this.knob('onepulse_first').value()
	init=first-1
	dur=this.knob('onepulse_dur').value()
	second=first+dur
	scr="{curve L x"+str(init)+" 0 x"+str(first)+" "+str(rate)+" x"+str(second)+" 0}"
	this.knob('rate').fromScript(scr)
	'''
	
	scr2='''
	this=nuke.thisNode()
	this.knob('onepulse_rate').setValue(1)
	this.knob('onepulse_first').setValue(0)
	this.knob('onepulse_dur').setValue(1)
	'''
	
	scr1=trimHeaderSpace(scr1)
	scr2=trimHeaderSpace(scr2)
	node=nuke.createNode('ParticleEmitter', param )
	node['onepulse_setexpr'].setValue(scr1)
	node['onepulse_auto'].setValue(scr2)
	return node
	
	
def crop():
	param='''
	addUserKnob {20 cx}
	addUserKnob {41 preset_1 l preset T this.preset}
	addUserKnob {41 reset_1 l Reset -STARTLINE T this.reset}
	addUserKnob {41 box_1 l box T this.box}

	addUserKnob {41 softness_1 l softness T this.softness}
	addUserKnob {7 shrinkh l "shrink H" R -1000 1000}
	addUserKnob {7 shrinkoldh l INVISIBLE +INVISIBLE}
	addUserKnob {7 shrinkv +DISABLED R -1000 1000}
	addUserKnob {7 shrinkoldv +INVISIBLE}
	addUserKnob {6 linkhv l "link HV" +STARTLINE}
	linkhv true

	addUserKnob {26 space1 " " T " " +STARTLINE}

	addUserKnob {7 outratiow ratio }
	addUserKnob {7 outratioh " : " -STARTLINE}
	addUserKnob {7 rc l "ratio control" +INVISIBLE}
	rc {{"(outratiow/outratioh) / (this.width/this.height)"}}
	addUserKnob {22 apply T "n=nuke.thisNode()\nbox=n.knob('box')\nrc = n.knob('rc').value()\nbox.clearAnimated()\n\nval0 = 0 if (rc > 1 ) else  ((n.width() -   n.width() * (rc) )/2) \nval1 =  0 if rc<1 else ((n.input(0).height() - (   n.input(0).height() * (1/(rc)) ) ) /2)\nval2 = n.input(0).width() if rc > 1 else  ((n.input(0).width() -   n.input(0).width() * (rc) )/2) + ( n.input(0).width() * (rc) )\nval3 = n.input(0).height() if rc<1 else (( n.input(0).height() -( n.input(0).height() *(1/ (rc)) )   ) /2) + ( n.input(0).height() *(1/ (rc)) )\n\nbox.setValue(val0, 0)\nbox.setValue(val1, 1)\nbox.setValue(val2, 2)\nbox.setValue(val3, 3)" +STARTLINE}
	addUserKnob {22 expratio l "expr ratio" -STARTLINE T "n=nuke.thisNode()\nbox=n.knob('box')\noutratiow=n.knob('outratiow').value()\noutratioh=n.knob('outratioh').value()\nbox.clearAnimated()\n\nscr0 = '(rc) > 1 ? 0 : ((input.width -   input.width * (rc) )/2) '\nscr1 = '(rc) < 1 ? 0 : ((input.height - (   input.height * (1/(rc)) ) ) /2) '\nscr2 = '(rc) > 1 ?input.width : ((input.width -   input.width * (rc) )/2) + ( input.width * (rc) )'\nscr3 = '(rc) < 1 ? input.height : (( input.height -( input.height *(1/ (rc)) )   ) /2) + ( input.height *(1/ (rc)) )'\n\nbox.setExpression(scr0,0)\nbox.setExpression(scr1,1)\nbox.setExpression(scr2,2)\nbox.setExpression(scr3,3)"}

	outratiow 2
	outratioh 1
	addUserKnob {26 "" +STARTLINE}
	addUserKnob {22 resetprojectwh l INVISIBLE +INVISIBLE T "n=nuke.thisNode()\n\n\n\nn.knob('box').clearAnimated()\nn.knob('box').setValue(0,0)\nn.knob('box').setValue(0,1)\nn.knob('box').setValue(nuke.toNode('root').width(),2)\nn.knob('box').setValue(nuke.toNode('root').height(),3)\n\n" +STARTLINE}
	addUserKnob {22 resetwh l "WH " T "n=nuke.thisNode()\n\n\nif n.input(0) != None :\n  n.knob('box').clearAnimated()\n  n.knob('box').setValue(0,0)\n  n.knob('box').setValue(0,1)\n  n.knob('box').setValue(n.input(0).width(),2)\n  n.knob('box').setValue(n.input(0).height(),3)\nelse :\n  nuke.message('connect input first ...')\n\n\n" +STARTLINE}
	addUserKnob {22 resetbbox l "BBOX    " -STARTLINE T "n=nuke.thisNode()\n\n\nif n.input(0)!=None :\n  n.knob('box').clearAnimated()\n  n.knob('box').setValue(n.input(0).bbox().x(),0)\n  n.knob('box').setValue(n.input(0).bbox().y(),1)\n  n.knob('box').setValue(n.input(0).bbox().x()+n.input(0).bbox().w(),2)\n  n.knob('box').setValue(n.input(0).bbox().y()+n.input(0).bbox().h(),3)\nelse :\n  nuke.message('connect input first ...')\n\n\n"}
	addUserKnob {22 resetexpandbbox l "expand BBOX" -STARTLINE T "n=nuke.thisNode()\nni=n.input(0)\nif ni !=None:\n    width=ni.width()\n    height=ni.height()\n    boxx=ni.bbox().x()\n    boxy=ni.bbox().y()\n    boxr=ni.bbox().w()+boxx\n    boxt=ni.bbox().h()+boxy\n    box= (boxx,boxy,boxr,boxt)\n    marginh=-box\[0] if -box\[0]>box\[2]-width else  box\[2]-width\n    marginv=-box\[1]  if -box\[1]>box\[3]-height else  box\[3]-height\n\n\n\n    b=1 if n.knob('crop').value() else 0\n    newbox=(-marginh-b,-marginv-b,width+marginh+b,height+marginv+b)\n    n.knob('box').clearAnimated()\n    n.knob('box').setValue(newbox)\nelse :\n  nuke.message('connect input first ...')"}
	addUserKnob {22 resetexprwh l "expr input WH  " T "n=nuke.thisNode()\n\n\nif n.input(0) !=None:\n  n.knob('box').clearAnimated()\n  n.knob('box').setValue(0,0)\n  n.knob('box').setValue(0,1)\n  n.knob('box').setExpression(\\\"input.width\\\",2)\n  n.knob('box').setExpression(\\\"input.height\\\",3)\nelse :\n  nuke.message('connect input first ...')\n\n" +STARTLINE}
	addUserKnob {22 resetexprbbox l "expr BBOX    " -STARTLINE T "n=nuke.thisNode()\n\n\nif n.input(0) !=None:\n  n.knob('box').clearAnimated()\n  n.knob('box').setExpression(\\\"input.bbox.x\\\",0)\n  n.knob('box').setExpression(\\\"input.bbox.y\\\",1)\n  n.knob('box').setExpression(\\\"input.bbox.r\\\",2)\n  n.knob('box').setExpression(\\\"input.bbox.t\\\",3)\nelse :\n  nuke.message('connect input first ...')\n\n\n"}
	addUserKnob {22 resetexprexpandbbox l "expr expand BBOX" -STARTLINE T "\nn=nuke.thisNode()\nif n.input(0) !=None:\n  exprbase=\\\"\\\"\\\"\n\[python -execlocal  \{\nn=nuke.thisNode()\nni=n.input(0)\nwidth=ni.width()\nheight=ni.height()\nboxx=ni.bbox().x()\nboxy=ni.bbox().y()\nboxr=ni.bbox().w()+boxx\nboxt=ni.bbox().h()+boxy\nbox= (boxx,boxy,boxr,boxt)\nmarginh=-box\[0] if -box\[0]>box\[2]-width else  box\[2]-width\nmarginv=-box\[1]  if -box\[1]>box\[3]-height else  box\[3]-height \nb=1 if n.knob('crop').value() else 0\nnewbox=(-marginh-b,-marginv-b,width+marginh+b,height+marginv+b)\n\\\"\\\"\\\"\n  exprend='\}]'\n  expr1=exprbase +'\\\\n'+'ret=newbox\[0]' +exprend\n  expr2=exprbase +'\\\\n'+'ret=newbox\[1]' +exprend\n  expr3=exprbase +'\\\\n'+'ret=newbox\[2]' +exprend\n  expr4=exprbase +'\\\\n'+'ret=newbox\[3]' +exprend\n  n.knob('box').clearAnimated()\n  n.knob('box').setExpression(expr1,0)\n  n.knob('box').setExpression(expr2,1)\n  n.knob('box').setExpression(expr3,2)\n  n.knob('box').setExpression(expr4,3)\nelse :\n  nuke.message('connect input first ...') \n\n\n"}
	addUserKnob {22 resetexprrootwh l "expr root WH  " T "n=nuke.thisNode()\nn.knob('box').clearAnimated()\nn.knob('box').setValue(0,0)\nn.knob('box').setValue(0,1)\nn.knob('box').setExpression(\\\"input.width\\\",2)\nn.knob('box').setExpression(\\\"input.height\\\",3)\n" +STARTLINE}
														  
	'''
	scr='''
	n=nuke.thisNode()
	k=nuke.thisKnob()
	if k.name()=='shrinkh' :
		valin=n.knob('box').value()
		shrink=k.value()
		shrinkold=n.knob('shrinkoldh').value()
		shrinkval=shrink-shrinkold
		if n.knob('linkhv').value() :
			val1=valin[0]-shrinkval
			val2=valin[1]-shrinkval
			val3=valin[2]+shrinkval
			val4=valin[3]+shrinkval
		else :
			val1=valin[0]-shrinkval
			val2=valin[1]
			val3=valin[2]+shrinkval
			val4=valin[3]

		valout=[val1,val2,val3,val4]
		n.knob('box').setValue(valout)
		n.knob('shrinkoldh').setValue(shrink)
		if n.knob('linkhv').value() :
			n.knob('shrinkv').setValue(shrink)
			n.knob('shrinkoldv').setValue(shrink)

	if k.name()=='shrinkv' :
		valin=n.knob('box').value()
		shrink=k.value()
		shrinkold=n.knob('shrinkoldv').value()
		shrinkval=shrink-shrinkold
		if n.knob('linkhv').value() :
			val1=valin[0]-shrinkval
			val2=valin[1]-shrinkval
			val3=valin[2]+shrinkval
			val4=valin[3]+shrinkval
		else :
			val1=valin[0]
			val2=valin[1]-shrinkval
			val3=valin[2]
			val4=valin[3]+shrinkval

		valout=[val1,val2,val3,val4]
		n.knob('box').setValue(valout)
		n.knob('shrinkoldv').setValue(shrink)
		if n.knob('linkhv').value() :    
			n.knob('shrinkh').setValue(shrink)
			n.knob('shrinkoldh').setValue(shrink)

	if k.name()=='linkhv' :
		if k.value() :
			n.knob('shrinkv').setEnabled(False)
			val=n.knob('shrinkh').value()
			n.knob('shrinkv').setValue(val)
			valin=n.knob('box').value()
			shrink=n.knob('shrinkv').value()
			shrinkold=n.knob('shrinkoldv').value()
			shrinkval=shrink-shrinkold

			val1=valin[0]
			val2=valin[1]-shrinkval
			val3=valin[2]
			val4=valin[3]+shrinkval

			valout=[val1,val2,val3,val4]
			n.knob('box').setValue(valout)
			n.knob('shrinkoldv').setValue(shrink)    
		else :
			n.knob('shrinkv').setEnabled(True)

	if k.name() in ['preset' , 'reset','resetprojectwh','resetwh','resetbbox','resetexprwh','resetexprbbox','reset235','reset169','reset43','resetratio']:
		n.knob('shrinkv').setValue(0)
		n.knob('shrinkoldv').setValue(0)    
		n.knob('shrinkh').setValue(0)    
		n.knob('shrinkoldh').setValue(0)
	'''
	scr=trimHeaderSpace(scr)
	c=nuke.createNode('Crop', param   )
	c.knob('knobChanged').fromScript(scr)
	return c



def bakeKnob(knob,first=nuke.root().frameRange().first(),last=nuke.root().frameRange().last(),asize=1,ask=0):
	cancel=0
	if ask :    
		frange = nuke.getFramesAndViews('get range', '1-100')    
		if frange :
		   first=int(frange[0].split('-')[0].strip())
		   last=int(frange[0].split('-')[1].strip())
		else :
		   cancel=1

	if not cancel :
		for index in range(asize):
			nuke.animation(knob.node().name()+'.'+knob.name()+'.'+str(index), "generate", (str(first), str(last), "1", "y", knob.node().name()+'.'+knob.name()+'.'+str(index))) 
		#knob.setExpression('')

	return 0 if cancel else 1



def getAnimationCurveObjFromTracker(n,indexlist):
	# indexlist=index list of tracker starts from 1 , ex:[2,3,5]
	# indexlist=[-1] : all tracker
	ok_tracker=['Tracker4']
	ok=1 if n.Class() in ok_tracker else 0
	if ok :
		allnodes=nuke.allNodes()
		for node in allnodes :
			node.setSelected(0)
		n.setSelected(1)
		tracker=nuke.createNode('Tracker4',inpanel=True)
		tracker['tracks'].fromScript(n['tracks'].toScript())
		numtracker=len(getTrackNames(tracker))
		datarow=31
		if indexlist != [-1] :

			# turn off all TRS data
			for i in range(numtracker):
				tracker['tracks'].setValue( 0, (i*datarow)+6 )    
				tracker['tracks'].setValue( 0, (i*datarow)+7 )    
				tracker['tracks'].setValue( 0, (i*datarow)+8 )    

			# turn on selected T data
			for i in range(numtracker):
				if i+1 in indexlist:
					tracker['tracks'].setValue( 1, (i*datarow)+6 )

		else :
			# turn on all T data , and turn off all RS data
			for i in range(numtracker):
				tracker['tracks'].setValue( 1, (i*datarow)+6 )    
				tracker['tracks'].setValue( 0, (i*datarow)+7 )    
				tracker['tracks'].setValue( 0, (i*datarow)+8 )
		# preset
		tracker['transform'].setValue('none')
		tracker['reference_frame'].setValue(1)
		tracker['jitter_period'].setValue(10)
		tracker['smoothT'].setValue(0)
		tracker['smoothR'].setValue(0)
		tracker['smoothS'].setValue(0)
		tracker['livelink_transform'].setValue(False)

		tracker.addKnob(nuke.XY_Knob('data'))
		tracker['data'].copyAnimations(tracker['translate'].animations())
		offset= [tracker['center'].value()[0] , tracker['center'].value()[1]  ]
		anim0=tracker['data'].animations()[0] ; anim1=tracker['data'].animations()[1]
		for i in list(anim0.keys()):
			anim0.setKey(i.x,i.y+offset[0])
		for i in list(anim1.keys()):
			anim1.setKey(i.x,i.y+offset[1])
		animcurve=tracker['data'].animations()
		nuke.delete(tracker)
		return animcurve
	else :
		print('Error. wrong node type.')



def getTrackNames(node):
	k=node['tracks']
	s=node['tracks'].toScript().split(' \n} \n{ \n ')
	s.pop(0)
	ss=str(s)[2:].split('\\n')
	ss.pop(-1)
	ss.pop(-1)
	outList=[]
	for i in ss:
		outList.append(i.split('"')[1])
	return outList


def inverseAxisMatrix(ns=nuke.selectedNodes()):
	if ns :
		n=ns[0]
		if n.Class().startswith('Camera') or n.Class().startswith('Axis') :
			import numpy as np    
			matrixknob=    n['matrix']
			asize=matrixknob.arraySize()
			first=nuke.root().frameRange().first()
			last=nuke.root().frameRange().last()
			matrixknob.setKeyAt(first)
			bakeKnob(matrixknob,first,last,asize)    
			n['useMatrix'].setValue(1)
			row=4 ; col=4
			for frame in range(first,last+1):
				nuke.frame(frame)
				matrixstr=[]
				for i in range(col):
						arrow=[str(n.knob('matrix').valueAt(frame,(i*4)+j)) for j in range(row)]
						matrixrow=','.join(arrow)
						matrixstr.append(matrixrow)
				matrixstr=';'.join(matrixstr)
				matrix=np.mat(matrixstr)    
				imatrix=np.linalg.inv(matrix)

				for i in range(col) :
					for j in range(row):
						n.knob('matrix').setValueAt(imatrix[i,j],frame, (i*4)+j)


def getUpstreamNode(n,inputindex,upnodelist):
	# get unpstream node for specific index (inputindex)
	# run recursively to deeper level
	upnode=n.input(inputindex)
	if upnode : 
		upnodelist.append(upnode)
		getUpstreamNode(upnode,inputindex,upnodelist)


def bakeMatrixData(ns=nuke.selectedNodes(),first=nuke.root().frameRange().first(),last=nuke.root().frameRange().last(), ask=0,delupstream=0):
	# combine transformation (bake) and create a new axis/camera for the new transform data.
	# ask = prompt frame range
	# delupstream = delete the upstreamnode (no new axis will be created)
	if ns :
		for n in ns :
			n.setSelected(0)
		n=ns[0]
		xpos=n.xpos()
		ypos=n.ypos()
		if  n.Class().startswith('Camera') or  n.Class().startswith('Axis') :
			if n.Class().startswith('Camera')  :
				obj=nuke.createNode('Camera2')
			else :
				obj=nuke.createNode('Axis2')
			obj.setXpos(xpos+75); obj.setYpos(ypos)
			obj['useMatrix'].setValue(1)
			matrixknob=obj['matrix']
			matrixknob.setExpression(n.name()+'.world_matrix')
			asize=matrixknob.arraySize()
			ok=bakeKnob(matrixknob,asize=asize,ask=ask)
			outnode=obj
			if delupstream :
				upstream_node_list=[]
				getUpstreamNode(n,0,upstream_node_list)
				for node in upstream_node_list :
					nuke.delete(node)
				n['matrix'].copyAnimations(obj['matrix'].animations())
				n['useMatrix'].setValue(1)
				nuke.delete(obj)
				outnode=n
			return outnode
		else :
			print('Pls select Axis or Camera node')


def frame_range():
	x='''
	addUserKnob {20 cx}
	addUserKnob {41 first_frame_1 l In T this.first_frame}
	addUserKnob {32 pin l set -STARTLINE T "knob first_frame \[python nuke.frame()]"}
	addUserKnob {32 pindec l < -STARTLINE T "set cfi \[value cfi]\nset value \[value knob.first_frame]\nset step \[value ptrimstep]\nset value \[expr \$value-\$step]\nknob first_frame \$value\nif \{\$cfi==true\} \{frame \$value\}"}
	addUserKnob {32 pininc l > -STARTLINE T "set cfi \[value cfi]\nset value \[value knob.first_frame]\nset step \[value ptrimstep]\nset value \[expr \$value+\$step]\nknob first_frame \$value\nif \{\$cfi==true\} \{frame \$value\}"}
	addUserKnob {22 pgotoin l "go to" -STARTLINE T nuke.frame(nuke.thisNode().knob('first_frame').value())}
	addUserKnob {22 presetin l R -STARTLINE T "n=nuke.thisNode()\nn.knob('first_frame').clearAnimated()\ninput=n.input(0)\nfirst=nuke.root().firstFrame()\nfirst2=input.firstFrame() if input else first\nn.knob('first_frame').setValue(first2)\n"}
	addUserKnob {41 last_frame_1 l Out T this.last_frame}
	addUserKnob {32 pout l set -STARTLINE T "knob last_frame \[python nuke.frame()]"}
	addUserKnob {32 poutdec l < -STARTLINE T "set cfi \[value cfi]\nset value \[value knob.last_frame]\nset step \[value ptrimstep]\nset value \[expr \$value-\$step]\nknob last_frame \$value\nif \{\$cfi==true\} \{frame \$value\}"}
	addUserKnob {32 poutinc l > -STARTLINE T "set cfi \[value cfi]\nset value \[value knob.last_frame]\nset step \[value ptrimstep]\nset value \[expr \$value+\$step]\nknob last_frame \$value\nif \{\$cfi==true\} \{frame \$value\}"}
	addUserKnob {22 pgotoout l "go to" -STARTLINE T nuke.frame(nuke.thisNode().knob('last_frame').value())}
	addUserKnob {22 presetout l R -STARTLINE T "n=nuke.thisNode()\nn.knob('last_frame').clearAnimated()\ninput=n.input(0)\nlast=nuke.root().lastFrame()\nlast2=input.lastFrame() if input else last\nn.knob('last_frame').setValue(last2)"}
	addUserKnob {26 x l "" +STARTLINE T " "}
	addUserKnob {4 ptrimstep l "     Trim step" M {1 10 50 100 ""}}
	addUserKnob {26 space1 l "" -STARTLINE T "     "}
	addUserKnob {6 cfi l "Adjust CFI" -STARTLINE}
	addUserKnob {26 text l " " T " "}
	addUserKnob {6 applyhandles l "apply handles" +STARTLINE}
	addUserKnob {22 setinput l "input" t "set in/out to match input or global range. If input is not connected then use global range" T "n=nuke.thisNode()\nn.knob('first_frame').clearAnimated()\nn.knob('last_frame').clearAnimated()\ninput=n.input(0)\nfirst = input.firstFrame() if input else nuke.root().firstFrame()\nlast = input.lastFrame() if input else nuke.root().lastFrame()\napplyhandles = n.knob('applyhandles').value()\nif applyhandles :\n    first +=  nuke.root().knob('cxhandles').value()\n    last -=  nuke.root().knob('cxhandles').value()\n\nn.knob('first_frame').setValue(first)\nn.knob('last_frame').setValue(last)" +STARTLINE}
	addUserKnob {22 proot l "root" t "set in/out to match input or global range. If input is not connected then use global range" T "n=nuke.thisNode()\nn.knob('first_frame').clearAnimated()\nn.knob('last_frame').clearAnimated()\nn.knob('first_frame').setValue(nuke.root().firstFrame())\nn.knob('last_frame').setValue(nuke.root().lastFrame())" +STARTLINE}
	addUserKnob {22 setinout l "viewer's in/out" -STARTLINE t "set in/out to match the active viewer in/out" T "n=nuke.thisNode()\nn.knob('first_frame').clearAnimated()\nn.knob('last_frame').clearAnimated()\ninout=nuke.activeViewer().node().knob('frame_range').getValue()\ninoutstate=nuke.activeViewer().node().knob('frame_range_lock').getValue()\nif inoutstate :\n  inp=int(inout.partition('-')\[0])\n  outp=int(inout.partition('-')\[2])\n  n.knob('first_frame').setValue(inp)\n  n.knob('last_frame').setValue(outp)\nelse :\n  nuke.message('please activate in/out in viewer first.')"}
	addUserKnob {22 setexprinput l "EXPR : input" -STARTLINE t "set in/out to match input/global range + handles by expression. If input is not connected then use global range" T "n=nuke.thisNode()\napplyhandles = n.knob('applyhandles').value()\nn.knob('first_frame').clearAnimated()\nn.knob('last_frame').clearAnimated()\nif applyhandles :\n    scr1='\[exists input0]?input.first_frame+root.cxhandles:root.first_frame+root.cxhandles'\n    scr2='\[exists input0]?input.last_frame-root.cxhandles:root.last_frame-root.cxhandles'\nelse :\n    scr1='\[exists input0]?input.first_frame:root.first_frame'\n    scr2='\[exists input0]?input.last_frame:root.last_frame'\n\nn.knob('first_frame').setExpression(scr1)\nn.knob('last_frame').setExpression(scr2)"}
	addUserKnob {22 setexprcf l "EXPR : current frame" t "set in/out to match current frame by expression" T "n=nuke.thisNode()\nn.knob('first_frame').fromScript('frame')\nn.knob('last_frame').fromScript('frame')" }
	
	'''
	return nuke.createNode('FrameRange',x   )


def time_offset():
	x='''
	addUserKnob {20 cx}
	addUserKnob {41 time_offset_1 l Offset T this.time_offset}
	addUserKnob {32 reset l "     Reset offset      " T "knob time_offset 0" +STARTLINE}
	addUserKnob {32 prev1 l < -STARTLINE T "set inc \[value inc]\nset val \[ expr (\[value time_offset] - \$inc)]\nknob time_offset \$val"}
	addUserKnob {32 next1 l > -STARTLINE T "set inc \[value inc]\nset val \[ expr (\[value time_offset] +\$inc)]\nknob time_offset \$val"}
	addUserKnob {4 inc l "   inc" -STARTLINE M {1 5 10 50 100 200 "" "" ""}}
	addUserKnob {22 offsettocur l " In " T "input=nuke.thisNode().input(0)!=None\nt=nuke.thisNode()\nif input :\n inp=t.input(0).firstFrame()\n offsetold=t.knob('time_offset').value()\n offset=-inp+nuke.frame()\n #cfi=nuke.frame()+(nuke.frame()-(inp+offsetold))\n t.knob('time_offset').setValue(offset)\n #nuke.frame(cfi)" +STARTLINE}
	addUserKnob {22 offsetto1 l " In point -> frame 1 " -STARTLINE T "input=nuke.thisNode().input(0)!=None\nt=nuke.thisNode()\nif input :\n inp=t.input(0).firstFrame()\n offsetold=t.knob('time_offset').value()\n offset=-t.input(0).firstFrame()+1\n t.knob('time_offset').setValue(offset)\n cfi=nuke.frame()-((inp+offsetold)-1)\n nuke.frame(cfi)\n"}
	addUserKnob {32 offsetcurto1 l " Current frame -> frame 1 " -STARTLINE T "knob time_offset \[expr (\[value time_offset]-(\[value frame]-1))]\nframe 1"}
	addUserKnob {32 offsetcurtotargetframe l " Current frame -> frame : " T "knob time_offset \[expr (\[value time_offset]-(\[value frame]-1)+ (\[value targetframe]-1) )]\nframe \[knob targetframe]" +STARTLINE}
	addUserKnob {3 targetframe l "" -STARTLINE}
	addUserKnob {22 settargetframe l " set " -STARTLINE T nuke.thisNode().knob('targetframe').setValue(nuke.frame())}
	addUserKnob {32 gotoin l "go to IN" T "frame \[expr \[value first_frame] + \[value time_offset]]\n" +STARTLINE}
	addUserKnob {32 gotoout l "go to OUT" -STARTLINE T "frame \[expr \[value last_frame] + \[value time_offset]]\n"}
	'''
	nuke.createNode('TimeOffset', x   )

def disconnectAllInputs():
	ns=nuke.selectedNodes()
	if ns :
		for n in ns :
			n.setInput(0,None)	


def transform():
	def apply_cycle_expr(ts):
		import cxdef
		scr="""
		n=nuke.thisNode()
		if  not n.knob('cxexpr') :
			scr=\"\"\"
			addUserKnob {20 cxexpr l "cycle expr"}
			addUserKnob {4 chan l channel M {X Y "" ""}}
			addUserKnob {4 mode l "   mode" -STARTLINE M {Repeat Bounce Random "" "" ""}}
			addUserKnob {4 direction l "   direction" -STARTLINE M {A B}}
			addUserKnob {22 inject -STARTLINE T "n=nuke.thisNode()\\nchan=0 if n\['chan'].value()=='X' else 1\\nmode=n\['mode'].value()\\ndirection=n\['direction'].value()\\nsticky=n\['stickybounce'].value()\\nexprrepeat='(int((((frame-pframestart)%(pmaxtime*(phold+1))))/(phold+1)))' \\nexprbounce='(int((((abs(((frame-pframestart-(pmaxtime*(phold+1)))%(2*pmaxtime*(phold+1)))- (((2*pmaxtime*(phold+1))-1)/2))-.5)))/(phold+1)))' if sticky else '(int((abs(((frame-pframestart-((pmaxtime*(phold+1))-(phold+1)))%   ((2*(pmaxtime-1)*(phold+1))) )- (  (((phold+1)*pmaxtime)-1) - (phold/2)) )+(phold/2))    /(phold+1))) '\\nexprrandom='(int((random(int(frame/(phold+1))+seed)*100)%(pmaxtime*(phold+1))/(phold+1)))'\\n\\nexpr=exprrepeat if mode=='Repeat' else exprbounce if mode=='Bounce' else exprrandom\\n\\nn\['pexpr'].setExpression(expr)\\nn\['pdata'].setExpression('abs(pexpr-(pmaxtime-1))' if (direction =='B' and mode!='Random' ) else 'pexpr')\\nn\['translate'].setExpression('pdata*pdist',chan)"}
			addUserKnob {6 stickybounce +STARTLINE}
			addUserKnob {3 phold}
			knob phold 2
			addUserKnob {7 pdist R 0 200}
			knob pdist 50
			addUserKnob {3 pframestart}
			knob pframestart 1
			addUserKnob {3 pmaxtime l "x time"}
			knob pmaxtime 6
			addUserKnob {7 seed l "random seed" R 1 100}
			knob seed 100
			addUserKnob {26 ""}
			addUserKnob {3 pexpr l INVISIBLE +INVISIBLE}
			addUserKnob {3 pdata l data}
			\"\"\"
			nuke.tcl(scr)		
				"""
		scr=cxdef.trim_header_space(scr)
		for t in ts :
			t.knob('cycleexpr').setCommand(scr)
		
		
	x="""
	addUserKnob {20 cxutil l cx}
	addUserKnob {22 reset_center l "reset center" T "n = nuke.thisNode()\ninput = n.input(0)\n\nw = n.input(0).width() if input else nuke.root().width()\nh = n.input(0).height() if input else nuke.root().height()\n\nn\['center'].setValue(\[w/2, h/2])" +STARTLINE}
	addUserKnob {26 div l "    " -STARTLINE T " "}
	addUserKnob {22 recenter l "re-center to " T cxdef.transformrecenter() -STARTLINE}
	addUserKnob {17 format l "" -STARTLINE}
	addUserKnob {22 cycleexpr l "create cycle expr utility"  +STARTLINE}
	"""
	nodes=nuke.selectedNodes()
	if nodes :
		if 'render_mode' in nodes[0].knobs() :
			ts=multinode( 'TransformGeo' )
		else :
			ts=multinode( 'Transform',x)
			apply_cycle_expr(ts)
	else :
		ts=multinode( 'Transform',x)
		apply_cycle_expr(ts)

def transformrecenter():
	this=nuke.thisNode()
	formatw=this['format'].value().width()
	formath=this['format'].value().height()
	px=this['center'].value()
	this['translate'].setValue(((formatw/2)-px[0],(formath/2)-px[1]))

def multinode(name,param='',mode=0): #return list type
	#mode 0=normal , 1=cxdef, 2=copypaste#
	ns=nuke.selectedNodes()
	nodelist=[]
	if len(ns) == 1 :
		node=nuke.createNode(name,param) 	if not mode else eval(name)
		nodelist.append(node)
	else :
		if ns :
			for n in ns :
				n.setSelected(False)
			for n in ns :
				n.setSelected(True)
				node=nuke.createNode(name,param) if not mode else eval(name)
				n.setSelected(False)
				node.setSelected(False)
				nodelist.append(node)
		else :
			node=nuke.createNode(name,param) if not mode else eval(name)		
			nodelist.append(node)
	for node in nodelist:
		node.setSelected(True)		
	return nodelist	
		



def duplicate_write_increment():
	panel=nuke.Panel('duplicate write increment')
	panel.addSingleLineInput('start index', '1')
	panel.addBooleanCheckBox('use start',0)
	panel.addSingleLineInput('num', '')
	panel.show()
	num=panel.value('num')

	if num is not None  :
		num=int(num)
		startnum=int(panel.value('start index'))
		usestart=panel.value('use start')
		ns=nuke.selectedNodes()
		if ns :
			for n in ns :
				n.setSelected(False)
			n=ns[0]
			if n.Class()=='Write' :
				n.setSelected(True)
				path=n.knob('file').value()
				file=path.rpartition('.')[0]
				ext=path.rpartition('.')[2]
				fileindex= int(re.search('(\d+)$', file).group(0)) 
				filename=file.rpartition(str(fileindex))[0]
				fileindex=fileindex if not usestart else startnum-1
				xpos=n.knob('xpos').value()
				ypos=n.knob('ypos').value()
				nuke.nodeCopy("%clipboard%")
				n.setSelected(False)
				for j in range(num) :
					node=nuke.nodePaste("%clipboard%")
					node.setSelected(False)
					node.knob('xpos').setValue(xpos+(120*(j+1)))
					node.knob('ypos').setValue(ypos)
					fileindex+=1
					node.knob('file').setValue(filename+str(fileindex)+'.'+ext)




def writefromread():
	# add write node to each selected nodes (multiple write node) #
	nodes=nuke.selectedNodes()
	if nodes :
		readmode=0    
		movietype=['mov']
		movie=0
		result =0
  
		for n in nodes :
			if n.Class()=='Read' :
				if n.knob('file').value().rpartition('.')[2] in movietype : movie=1
				readmode=1
				break
 
		if readmode :
			panel=nuke.Panel('CLAYFX PANEL')
			panel.addEnumerationPulldown('channels', 'rgb rgba')    
			if movie : panel.addEnumerationPulldown('fps', '25 24 23.98')    
			panel.addSingleLineInput('suffix/name', '')
			panel.addSingleLineInput('subfolder', 'fix')
			if movie : panel.addBooleanCheckBox('png mov32',False)
			panel.addBooleanCheckBox('replace name sequence',False)
			panel.addSingleLineInput('start seq', '1')
			panel.addBooleanCheckBox('branch',False)
			panel.addButton('skip')
			panel.addButton('ok')
			result=panel.show()

		if result :
			branch=panel.value('branch')
			subfolder=panel.value('subfolder').strip()
			idx=panel.value('start seq')
			idx=int(idx) if idx.isdigit() else 1
			replace=panel.value('replace name sequence')
			fps=25;png=0    
			if movie :
				fps=panel.value('fps')
				png=panel.value('png mov32')
			fps=25 if fps is None else fps
			png=0 if png is None else png    
			suffix=panel.value('suffix/name').strip()   
			channels=panel.value('channels')    
			suffix='' if suffix is None else suffix
			channels='rgb' if channels is None else channels

			for node in nodes :
				node.setSelected(False)

			for node in nodes :
				xpos=node.xpos()
				ypos=node.ypos()+120
				if node.Class()=='Read' :
					if not branch:
						node.setSelected(True)    
					path=node.knob('file').value()
					filename, extension = os.path.splitext(path)    
					write=nuke.createNode('Write')
					write.knob('file_type').setValue(extension[1:])
					if extension.lower()=='.mov' :
						if png :
							write.knob('meta_codec').setValue('png')
							write.knob('meta_encoder').setValue('mov32')
						write.knob('mov32_fps').setValue(float(fps))
						write.knob('mov64_fps').setValue(float(fps))

					if subfolder != '' or subfolder is not None :
						folder=os.path.dirname(filename)
						filen=os.path.basename(filename)    
						filename =folder+('/' if subfolder !='' else '')+subfolder+'/'+filen
					if replace :
						suffix = 'file' if (suffix =='' or suffix is None) else suffix 
						folder=os.path.dirname(filename)
						filename=folder+'/'+suffix+'-'+str(idx)
						idx+=1
					else :
						if suffix != '' or suffix is not None :
							filename+=suffix    
					write.knob('file').setValue(filename + extension)
					write.knob('channels').setValue(channels)

				else :
					write=nuke.createNode('Write')
				write.setInput(0,node)
				write.setXpos(xpos)
				write.setYpos(ypos)
				node.setSelected(False)
				write.setSelected(False)
		else :
			nuke.createNode('Write')
	else :    
		nuke.createNode('Write')


def checkFtype(filename):
	# returnn ftype ---> 1:mov 2:sequence 3:still
	import re
	import os
	from cxsetting import __movlist__

	ext=os.path.splitext(filename)[1][1:]
	if ext in __movlist__ :
		ftype=1 # --- MOV
	else :
		filename=os.path.splitext(filename)[0] #filename w/o extension
		findlist1=re.findall('#+',filename) # search '#'
		findlist2=re.findall('%0[0-9]+d',filename) # search %0xd format
		findlist3=re.findall('%d',filename) # search %d format
		if findlist1 or findlist2 or findlist3 :
			ftype=2 # --- SEQ
		else :
			ftype=3 # --- STILL
	return ftype

def revealFinder(fullpath, matchdir = False):
	from claystudio import __cserverstat__,__cmsg__
	if not(__cserverstat__) : nuke.message(__cmsg__) ; return
	from cxsetting import   __osnum__,__nukeremapid__,__platform__
	import subprocess , os


	def openlocation(platform,fullpath):
		if platform == "win":
			fullpath=fullpath.replace('/','\\')
			subprocess.Popen(r'explorer /select,'+ fullpath)
		else :
			subprocess.call(["open", "-R", fullpath])

	def reducedir(path):
		path = os.path.dirname(path)
		if os.path.exists(path) or path == "" :
			return path
		else :
			return reducedir(path)

	fullpath=nuke.tcl("set x "+'"'+fullpath+'"').strip() #convert tcl fullpath to real fullpath

	if __nukeremapid__ >= 0 :
		# OS is recognized
		# Remap if other OS
		remaps=nuke.toNode('preferences').knob("platformPathRemaps").toScript().split(';')
		remapnum=len(remaps)-1
		if remapnum > 0 :
			for i in range(remapnum):
				if fullpath.startswith(remaps[i]) and remaps[i].strip() != "" :
					if (i % __osnum__ ) != __nukeremapid__ : 
						row = int(i / __osnum__)
						fullpath=fullpath.replace(remaps[i],remaps[(row*__osnum__)+__nukeremapid__])
					break

		filename=os.path.basename(fullpath)
		ftype=checkFtype(filename)
		if ftype ==1 or ftype==3 :
			# if mov or still
			if os.path.exists(fullpath):
				openlocation( __platform__ ,fullpath)
			else :
				if matchdir : 
					fullpath = reducedir(fullpath)
					openlocation( __platform__ ,fullpath)
				else :
					nuke.message("File doesn't exist")
		else :
			# sequence
			# MODIFY FILENAME IF FILES ARE SEQUENCES
			path=os.path.dirname(fullpath)
			filename=os.path.basename(fullpath)
			filename=re.sub('[#]+',lambda x : '(\d{'+str(len(x.group()))+'})',filename)
			filename=re.sub('%0(\d+)d',lambda x : '(\d{'+str(x.group(1))+'})',filename)
			filename=re.sub('%d','(\\\d+)',filename)
			files=[i for i in os.listdir(path) if (os.path.isfile(os.path.join(path,i)) and re.search(filename,i) )]
   
			if files :
				files=sorted(files)
				filename=files[0]
				fullpath=path+"/"+filename
	

				if os.path.exists(fullpath):
					openlocation( __platform__ ,fullpath)
				else :
					if matchdir : 
						fullpath = reducedir(fullpath)
						openlocation( __platform__ ,fullpath)
					else :
						nuke.message("File/Folder doesn't exist")
			else :
				# if empty list then send err msg and exit
				nuke.message("File doesn't exist")
	else :
		nuke.message('Unknown OS')


def revealFinderNode():
	#reveal in finder the path from write/read/precomp node
	ns=nuke.selectedNodes()
	filenodelist=['Write','Read','Precomp','ReadGeo','ReadGeo2'] #define nodes here
	if ns :
		for n in ns :
			if n.Class() in filenodelist :
				node=n.name()
				path=nuke.tcl('knob '+node+'.file')
				if not path :
					nuke.message('Path is empty.')
				else :
					revealFinder(path) 
			else :
				nuke.message('Please select a Node with the "file" knob.')
	else :
		nuke.message('Please select a Node with the "file" knob.')

def createAssistFile():
	import nuke
	import re 
	import os
	import subprocess

	def render(n):
		first=n.firstFrame()
		last=n.lastFrame()
		nuke.execute(n,first,last)

	def save(path,formatstr,n):
		def addheader(path,formatstr,first,last):	
			with open(path, "r+") as f:
				fps=str(nuke.root().knob('fps').value())	
				old = f.read() 
				head=old.partition('Group')[0]
				tail='Group '+old.partition('Group')[2]
				insert='Root {\n format "'+formatstr+'"\n first_frame '+str(first)+'\n last_frame '+str(last)+'\n fps '+fps+'\n}\n'
				f.seek(0)
				f.write(head+insert+tail) 

		w=n.width()
		h=n.height()		
		first=n.firstFrame()
		last=n.lastFrame()
		ftype = checkFtype(path)

		colorspace=n.knob('colorspace').value()
		dur=(last-first)+1
		dirpath=os.path.dirname(path)
		filename=os.path.basename(path)
		assistfile=re.sub("v\d+","assist",filename)
		assistfile=os.path.splitext(assistfile)[0]+'.nk'

		if assistfile:
			scriptpath=dirpath+'/script/' if (ftype==1 or ftype==3) else os.path.dirname(dirpath)+'/script/'
			if not os.path.exists(scriptpath) : os.mkdir(scriptpath)
			newfile=scriptpath+assistfile
			cont=1
			if os.path.exists(newfile):	cont=nuke.ask(newfile+'\nis alredy exist.\nDo you want to replace?')		
			if cont :
				g=nuke.nodes.Group()
				g.knob('postage_stamp').setValue(1)
				g.addKnob(nuke.Boolean_Knob('texton','Text On/Off'))
				g.addKnob(nuke.Double_Knob('textsize','Text size'))
				g.knob('textsize').setRange(1,100)
				g.knob('texton').setValue(1)

				g.knob('textsize').setValue(30)	
				g.begin()
				#read node
				readnode=nuke.nodes.Read(file="[file dirname [value root.name]]/../"+( "seq/" if ftype==2 else "")+filename)
				readnode.knob('first').setValue(1 if (ftype==1 or ftype==3) else first)
				readnode.knob('last').setValue(dur if (ftype==1 or ftype==3) else last)
				#readnode.knob('colorspace').setValue(colorspace)
				#offset node
				offsetnode=nuke.nodes.TimeOffset(time_offset=first-1)
				offsetnode.setInput(0,readnode)
				offsetnode.knob('disable').setValue(0 if (ftype==1 or ftype==3) else 1)
				#text node
				textnode=nuke.nodes.Text(message="\n [basename [value "+readnode.name()+".file]]\n Fps : [value root.fps]   Res: [value root.width]x[value root.height]    In:[value root.first_frame]    Out:[value root.last_frame]    Frame : [frame]", yjustify='bottom', size="parent.textsize")
				textnode.setInput(0,offsetnode)
				textnode.knob('box').setValue([0,0,w,h])
				textnode.knob('font').setValue("/Library/Fonts/Arial.ttf")
				textnode.knob('disable').setExpression('!parent.texton')
				textnode.knob('leading').setValue(.3)

				lastnode=textnode
				o=nuke.nodes.Output()
				o.setInput(0,lastnode)
				offsetnode.setYpos(offsetnode.ypos()+50)
				textnode.setYpos(textnode.ypos()+50)	
				o.setYpos(o.ypos()+50)							
				g.end()

				g.knob('selected').setValue(1)
				d1=nuke.createNode('Dot','label "start"')
				d1.setYpos(d1.ypos()+100)
				[i.knob('selected').setValue(False) for i in nuke.allNodes()]						
				g.knob('selected').setValue(1)
				rp=nuke.createNode('RotoPaint')
				d1.setInput(0,g)
				rp.setYpos(g.ypos()+32)
				rp.setXpos(g.xpos()+200)
				tx=nuke.createNode('Text2')
				d2=nuke.createNode('Dot','label info')

				g.knob('label').setValue('[basename [value this.'+readnode.name()+'.file]]\n '+str(first)+' - '+str(last)+' \['+ str((last-first)+1) +']')
				[i.knob('selected').setValue(False) for i in nuke.allNodes()]	

				nodelist=[g,d1,rp,tx,d2] #node to be pasted into new file assist
				for node in nodelist:
					node.knob('selected').setValue(1)

				nuke.nodeCopy(newfile)
				addheader(newfile,formatstr,first,last)

				for node in nodelist :
					nuke.delete(node)

		else :
			nuke.message("knob assistfile is empty.")



	ns=nuke.selectedNodes()
	validclass=['Read','Write']
	if ns :
		for n in ns :
			if n.Class() in validclass :
				w=n.width()
				h=n.height()
				pa=n.pixelAspect()
				pa = str(int(pa)) if int(pa)==pa else '{0:.2f}'.format(pa)
				formattype=''
				for format in nuke.formats() :
					if format.width() ==w and format.height()==h :
						w=str(w)
						h=str(h)
						formatstr=w+" "+h+" 0 0 "+w+" "+h+" "+pa+" "+format.name()

				node=n.name()
				pathtcl=nuke.tcl('knob '+node+'.file')	
				path=nuke.tcl("set xfile "+'"'+pathtcl+'"') # convert tcl path into full real path
				filename=os.path.basename(path)
				ftype = checkFtype(path)
	
				if (ftype==1 or ftype==3) :
					# STILL IMAGE OR MOV
					if  os.path.exists(path) :
						save(path,formatstr,n)
						n.knob('selected').setValue(1)
					else :
						if n.Class()=='Write' :
							render(n)
							save(path,formatstr,n)
							n.knob('selected').setValue(1)
						else :
							nuke.message("Render file doesn't exist.")
				else :
					# SEQUENCES
					first=n.firstFrame()
					last=n.lastFrame()
					dirname=os.path.dirname(path)
					filename= os.path.splitext(os.path.basename(path))[0]
					ext=os.path.splitext(os.path.basename(path))[1]
					pad1=re.findall('#+',filename)
					pad2=re.findall('%0[0-9]+d',filename)					
					strtemp=filename
					out=''
					missingframe=0
					for num in range(first,last+1):
						for s in pad1 :
							strpart=strtemp.partition(s)
							out=out+strpart[0]+(str(num).zfill(len(strpart[1])))
							strtemp=strpart[2]
						strtemp=out+strtemp if pad1 else strtemp
						out=''
						for s in pad2 :
							strpart=strtemp.partition(s)
							print(strpart[0])
							digit=int(s[:-1][2:])
							out=out+strpart[0]+(str(num).zfill(digit))
							strtemp=strpart[2]
						newpath=dirname+'/'+((out+strtemp) if pad2 else strtemp)+ext
						out=''
						strtemp=filename
						if not os.path.exists(newpath):
							if n.Class()=='Write' :
								nuke.execute( n, num,num)
							else :
								nuke.message('Some frames are missing from the sequence. Pls re-render.')
								missingframe=1
								num=last+1 #exit loop
					if not missingframe:
						save(path,formatstr,n)

	else :
		nuke.message('Pls select a Write or a Read node.')	

	#reselect previous selected.
	for n in ns :
		n.knob('selected').setValue(1)	
	


def setProjectRangefromNode():
	ns=nuke.selectedNodes()
	if ns :
		n=ns[0]
		first=n.firstFrame()
		last=n.lastFrame()
		r=nuke.root()
		r.knob('first_frame').setValue(first)
		r.knob('last_frame').setValue(last)		


def cprint_list(listx,mode=0,header='',showtotal=1,showheader=1,joiner='',subjoiner='',raw=1):
	'''
	print input list , mode-> 0:normal 1:one line with single space separator 2:one line with no separator
	'''
	if listx:
		if not subjoiner: subjoiner=partition02
		if showheader :
			print(clinebr) 
			if header : print(header)
			if header : print(clinebr) 
		if raw :
			listx=[(x.__repr__() if type(x).__name__ in cdagobj else (  [ ( y.__repr__() if type(y).__name__ in cdagobj else y)  for y in x] if  type(x).__name__=='list'  else str(x))) for x in listx]
		else :    
			listx=[(x.name() if type(x).__name__ in cdagobj else (  [ ( y.name() if type(y).__name__ in cdagobj else y)  for y in x] if  type(x).__name__=='list'  else str(x))) for x in listx]
		listx=[subjoiner.join([str(xx) for xx in x ]) if type(x).__name__ == 'list' else str(x) for x in listx]
		if not joiner :
			if mode==0 : joiner=cbr
			elif mode==1: joiner=' '
			elif mode==2: joiner=''

		listxstr=joiner.join(listx)
		print(listxstr)
		print(cbr+'** TOTAL : '+str(len(listx)) if showtotal else None)
		if showheader :print(clinebr) 
	else:
		print('<empty>')

def cprint_fullname():
	nodes=ccollect_nodes(1,run=2)
	node=nodes[0] if nodes else None
	if node :
		print(clinebr)
		print('Name : %s' % node.name())
		print('Fullname : root.%s' % node.fullName())
		print('Level : %s' % ccurlevel(node))
		print(clinebr)
	else :
		cerr()


def ccollect_nodes(sel=0,classx=[],classxmode=0,classxcase=0,pattern=[],patternmode=0,patterncase=0,unsort=0,sortcase=0,level='',externalblock=0,recursive=0,invmatchclass=0,invmatchpat=0,inputidx=-1,diglevel=100,tonodeinout='',run=0):
	'''
	COLLECT SELECTED OR ALL NODES 
	classx= filter by class, classx can be list or string 
	classxcase= case sensitivity when filtering 0:ignore 1:case sensitive 
	classxmode= mode how the classx is used-> 0:any 1:head 2:tail 3:match all
	sel= 0:all 1:selected 2:thisNode().input() 3:thisNode().dependent() 4:selectedNode().input() 5:selectedNode().dependent() 
	6: toNode().input() 7:toNode().dependent().
	level= set level to work with 
	unsort= sort the final output list 0:sort 1:no sort 
	sortcase= use or ignore case sensitivity when sorting -> 0:ignore 1:sensitive 
	patternmode= like classxmode but for pattern    
	patterncase= like classxcase but for pattern    
	pattern= pattern to match node's name , can be list or string     
	externalblock-> 1:use external block .begin() and end() and disable internal block 
	recursive->search node recursively when select nodes from output (dig down output tree) 
	invmatchclass/invmatchpat = mode to inverse the match logic (=> exclude vs include)
	inputidx = input index when grab from input , negative value means grab all input.
	diglevel-> how deep to dig recursively
	tonodeinout-> source for input/output stream, no need to write fullname.
	run-> 0:node 1:se 2:menu/panel
	'''

	# level process
	if run==0 : 
		levelx=nuke.thisParent()
		runfrom='dag'
	elif run==1 : 
		levelx=nuke.toNode(level)
		runfrom='se'
	else : 
		levelx=''
		runfrom='menu'
	oricurlevel=ccurlevel()
	if type(nuke.toNode(oricurlevel)).__name__ =='Node' :
		oricurlevel=ccurlevel().rpartition('.')[0]

	_sel_with_no_workinglevel_ = [2,3] #this value will run without working level
	_start_working_level_=(levelx!='' and sel not in _sel_with_no_workinglevel_ and not externalblock)
	levelx.begin() if _start_working_level_ else None 

	# get nodes list
	nodes=[]
	curlevel=ccurlevel()
	if sel==0: # all
		nodes=nuke.allNodes()
		if not nodes : cerr(msg="there's no node at all @%s"%curlevel)
	elif sel==1: # selected
		nodes =nuke.selectedNodes()
		if not nodes : cerr(msg="no selected node @%s"%curlevel)
	elif sel==2: # thisNode().input()
		if runfrom=='dag' :
			node=nuke.thisNode() 
			if node :
				nodes=ccollect_nodes_from_inout(node,recursive,diglevel=diglevel,inputidx=inputidx)
				if nodes :
					nodes=list(set(nodes)) 
				else :
					cerr(msg='node %s got no input stream'%('root.'+node.fullName()))
			else :
				cerr(msg='thisNode() execute:fail')
		else :
			cerr('(sel=3) thisNode() is N/A in non-DAG mode')
	elif sel==3: # thisNode().dependent() / output
		if runfrom=='dag' :
			node=nuke.thisNode() 
			if node :
				nodes=ccollect_nodes_from_inout(node,recursive,frominput=0,diglevel=diglevel)
				if nodes :
					nodes=list(set(nodes)) 
				else :
					cerr(msg='node %s got no output/dependent stream'%('root.'+node.fullName()))
			else :
				cerr(msg='thisNode() execute:fail')
		else :
			cerr('(sel=3) thisNode() is N/A in non-DAG mode')
	elif sel==4: # selectedNode().input()
		nodes=nuke.selectedNodes()
		if nodes :
			node=nodes[0] 
			nodes=ccollect_nodes_from_inout(node,recursive,diglevel=diglevel,inputidx=inputidx)
			if nodes :
				nodes=list(set(nodes)) 
			else :
				cerr(msg='node %s got no input stream'%('root.'+node.fullName()))
		else :
			cerr(msg="no selected node @%s"%curlevel)
	elif sel==5: # selectedNode().dependent() / output
		nodes=nuke.selectedNodes()
		if nodes :
			node=nodes[0] 
			nodes=ccollect_nodes_from_inout(node,recursive,frominput=0,diglevel=diglevel)
			if nodes :
				nodes=list(set(nodes)) 
			else :
				cerr(msg='node %s got no output/dependent stream'%('root.'+node.fullName()))
		else :
			cerr(msg="no selected node @%s"%curlevel)
	elif sel==6: # toNode().input()
		node = nuke.toNode(tonodeinout)
		if node :
			nodes=ccollect_nodes_from_inout(node,recursive,diglevel=diglevel,inputidx=inputidx)
			if nodes :
				nodes=list(set(nodes)) 
			else :
				cerr(msg='node %s got no input stream'%('root.'+node.fullName()))
		else : 
			cerr(msg="node %s doesn't exist " %tonodeinout)
	elif sel==7: # toNode().dependent() / output
		node = nuke.toNode(tonodeinout)
		if node :
			nodes=ccollect_nodes_from_inout(node,recursive,frominput=0,diglevel=diglevel)
			if nodes :
				nodes=list(set(nodes)) 
			else :
				cerr(msg='node %s got no output/dependent stream'%('root.'+node.fullName()))
		else : 
			cerr(msg="node %s doesn't exist " %tonodeinout)
	# levelx.end() if _start_working_level_ else None 
	#nuke.toNode(oricurlevel).end()

	# filtering
	if nodes :
		if classx in ['__all__','__ALL__',['__all__'],['__ALL__']] : classx=[]
		nodes=cremitem_from_list(nodes,'item.Class()',classx,classxmode,classxcase,not invmatchclass) # filter classx
		nodes=cremitem_from_list(nodes,'item.name()',pattern,patternmode,patterncase,not invmatchpat) # filter pattern
		if not unsort: 
			if sortcase:
				nodes.sort(key=lambda x:x.name()) #sort case sensitive
			else :
				nodes.sort(key=lambda x:x.name().lower()) #sort ignore case   
	return nodes


def print_knobs():
	nodes=ccollect_nodes(1,run=2)
	node=nodes[0] if nodes else None
	if node :
		knobs=node.allKnobs()
		knobs=[[knob.name(),knob.Class(),knob.value() if type(knob).__name__ not in ['PyScript_Knob'] and type(knob).__name__.find('String_Knob')<0 else '[hidden]'] for knob in knobs]
		knobs=cremitem_from_list(knobs,'item[0]',[''],3,1)
		cprint_list(knobs)
	else :
		cerr()


def toggle_cam_display():
	#show/hide camera object in 3d viewer
	global cam_display_state
	cam_class = 'Camera2'
	if cam_display_state :
		for m in nuke.allNodes(cam_class):
			m['display'].setValue('off')
		cam_display_state = 0
	else:
		for m in nuke.allNodes(cam_class):
			m['display'].setValue('wireframe')
		cam_display_state = 1


# def add_in_out_label():
# 	ns=nuke.selectedNodes()
# 	if ns :
# 		for n in ns :
# 			labelori=n.knob('label').value()
# 			labelx=labelori+"[value first_frame] - [value last_frame] \[ [expr [value last_frame] - [value first_frame] + 1 ] \]"
# 			n.knob('label').setValue(labelx)


def print_knob_list():
	#displaying knob type list#
	knobs = {
	0 : "Obsolete_knob" ,
	1 : "String_knob" ,
	2 : "File_knob, Write_File_knob" ,
	3 : "Int_knob, MultiInt_knob" ,
	4 : "Enumeration_knob" ,
	5 : "Bitmask_knob" ,
	6 : "Bool_knob" ,
	7 : "Double_knob" ,
	8 : "Float_knob, MultiFloat_knob" ,
	9 : "Array_knob" ,
	10 : "ChannelSet_knob, ChannelMask_knob, Input_ChannelSet_knob, Input_ChannelMask_knob" ,
	11 : "Channel_knob, Input_Channel_knob" ,
	12 : "XY_knob" ,
	13 : "XYZ_knob" ,
	14 : "WH_knob" ,
	15 : "BBox_knob" ,
	17 : "Format_knob" ,
	18 : "Color_knob" ,
	19 : "AColor_knob" ,
	20 : "Tab_knob, BeginGroup/EndGroup, BeginClosedGroup/EndGroup" ,
	21 : "Custom_knob" ,
	22 : "PyScript_knob" ,
	24 : "Transform2d_knob" ,
	25 : "Spacer" ,
	26 : "Text_knob, Named_Text_knob, Divider" ,
	27 : "Help_knob" ,
	28 : "MultiLine_String_knob" ,
	29 : "Axis_knob" ,
	30 : "UV_knob" ,
	31 : "Box3_knob" ,
	32 : "Button, Script_knob" ,
	33 : "LookupCurves_knob" ,
	35 : "Pulldown_knob" ,
	36 : "Eyedropper_knob" ,
	37 : "Range_knob" ,
	38 : "Histogram_knob" ,
	39 : "Keyer_knob" ,
	40 : "ColorChip_knob" ,
	41 : "Link_knob" ,
	42 : "Scale_knob" ,
	43 : "Multiline_Eval_String_knob()" ,
	44 : "OneView_knob" ,
	45 : "MultiView_knob" ,
	46 : "ViewView_knob" ,
	47 : "PyPulldown_knob" ,
	48 : "GPUEngine_knob" ,
	49 : "MultiArray_knob" ,
	50 : "ViewPair_knob" ,
	51 : "List_knob" ,
	52 : "Python_knob" ,
	53 : "MetaData_knob" ,
	54 : "PixelAspect_knob" ,
	55 : "CP_knob" ,
	56 : "BeginToolbar/EndToolbar" ,
	57 : "BeginTabGroup/EndTabGroup" ,
	59 : "BeginExoGroup/EndExoGroup" ,
	60 : "Menu_knob" ,
	61 : "Password_knob" ,
	62 : "Toolbox_knob" ,
	63 : "Table_knob" ,
	64 : "GeoSelect_knob" ,
	65 : "InputOnly_ChannelSet_knob, InputOnly_ChannelMask_knob" ,
	66 : "InputOnly_Channel_knob" ,
	67 : "ControlPointCollection_knob" ,
	68 : "CascadingEnumeration_knob" ,
	69 : "Dynamic_Bitmask_knob" ,
	70 : "MetaKeyFrame_knob" ,
	71 : "PositionVector_knob" ,
	72 : "Cached_File_knob" ,
	73 : "TransformJack_knob" ,
	74 : "Ripple_knob" 
	}
	print(' -- knob list --\n')
	for i in list(knobs.keys()) :
		print(( str(i) + " : " +knobs[i]))

def renameClipToFolder(level=1):
	# from hiero.core import *
	import hiero.core
	import hiero.ui
	import os
	seq= hiero.ui.activeSequence()
	te = hiero.ui.getTimelineEditor(seq)
	my_track_items=te.selection() 
	for ti in my_track_items:
		if isinstance(ti, hiero.core.TrackItem):
			media_source = ti.source().mediaSource()
			fi = media_source.fileinfos()[0] # assuming single file infos object
			if level==1 :
				folder_name = os.path.basename(os.path.dirname(fi.filename()))
			elif level==2 :
				folder_name = os.path.basename(os.path.dirname(os.path.dirname(fi.filename())))
			else :
				None
			ti.setName(folder_name)








def ibkStack():
	ns=nuke.selectedNodes()
	if ns :
		n=ns[0]
		ibkclass="IBKColourV3"
		if n.Class()== ibkclass:
			nodename=n.name()
			n['multi'].setValue(0)
			for i in range(9):
				ibk=nuke.createNode(ibkclass)
				ibk['off'].setSingleValue(False)
				ibk['mult'].setSingleValue(False)
				ibk['screen_type'].setExpression(nodename+'.screen_type')
				ibk['Size'].setExpression(nodename+'.Size')
				ibk['off'].setExpression(nodename+'.off')
				ibk['mult'].setExpression(nodename+'.mult')
				ibk['erode'].setValue(0)
				ibk['multi'].setValue(pow(2,i))




def writenode_dynamic_version():
	wnodes=nuke.selectedNodes("Write")
	wnodes=wnodes+nuke.selectedNodes("Read")
	for wnode in wnodes:
		#if wnode.name() == 'write_final' :
			node= wnode.name()
			pathtcl=nuke.tcl('knob '+node+'.file')	
			path=nuke.tcl("set xfile "+'"'+pathtcl+'"') # convert tcl path into full real path
			path=re.sub("_v\d+","_[lindex [split [lindex [split [lindex [split [value root.name] /] end] .] 0] _] end]", path)
			wnode.knob('file').setValue(path)



def batch_render_per_frame(n=None):
	def rendering(w):
		wname=w.name()
		first=w.firstFrame()
		last=w.lastFrame()
		curframe=first
		print("")
		print("render "+wname+"...")
		while curframe <=last :
				nuke.render(w,curframe,curframe,1)
				print("frame "+ str(curframe))
				curframe+=1
	if n :
		w=n
		rendering(w)
	else :
		ns=nuke.selectedNodes()
		ws=collect(ns,"Write")
		print("\n")
		print("Batch Rendering per single frame")
		print("--------------------------------")        
		if ws :
			for w in ws :
					rendering(w)
		else :
			print("Please select Write node(s) selected.")


def collect(ns=[],classname=None):
	#collect selected type of Node class from array of Nodes
	#return array type of Nuke node or None if no collection
	if not classname :
		print("\n")
		print("DOCS")
		print("collect selected type of Node class")
		print("and return array of Nuke nodes")
		print("")
		print("usage:")
		print("collect(selected_nodes,classname)")
		print("example : collect(nuke.selectedNodes(),\"Write\")")
	else :
		collectarr=[]
		for n in ns :
			if n.Class()== classname :
				collectarr.append(n)
		if collectarr :
			return collectarr
		else:
			return None		


def shuffle_nodes():
	def getminx(nodes):
		minx=nodes[0].xpos()
		for node in nodes :
			minx=min(minx,node.xpos())
		return minx

	def getminy(nodes):
		miny=nodes[0].ypos()
		for node in nodes :
			miny=min(miny,node.ypos())
		return miny
	

	nodes=nuke.selectedNodes()
	if nodes :
		spacex=100
		spacey=180
		maxcol=8
		initx=getminx(nodes)
		inity=getminy(nodes)
		print(initx, inity)
		row=0; col=0
		for node in nodes :
				if row==maxcol: 
					row=0
					col+=1
				xx=initx+(row*spacex)
				yy=inity+(col*spacey)
				node.setXpos(xx)
				node.setYpos(yy)
				row+=1    			


def pullmissingfiles():
	#pull missing files from claynet
	def issequence(path):
		return 1

	ns=nuke.selectedNodes("Read")
	if ns :
		for n in ns :
			path=n['file'].value()
			path=nuke.tcl('set x "'+path+'"') #evaluate path if it's script
		issequence=issequence(path)
		if issequence :
			print("seq")        
	else :
		print("no selected Node(s)")




def copyRecentFiles():
	import subprocess
	from cxsetting import  __platform__ , __nukefolder__
	from shutil import copyfile,move
	from claystudio import __cwinroot__, __cmacroot__

	if __platform__ == "mac" :
		dest=__cmacroot__ +"/projects/"
	else :
		dest=__cwinroot__+"/projects/"
		
	src = __nukefolder__ + "/recent_files"
	dest+="SyncToy_90191031-203845.dat"
	if os.path.isfile(dest):
		os.remove(dest)
		copyfile(src,dest)  
		subprocess.check_call(["attrib","+H",dest])



def align_nodes(alignmode) :
	ns=nuke.selectedNodes()
	align=alignmode #0-horizontal, 1-vertical , 2-follow ref
	# for follow ref , select last 2 nodes as reference
	if ns :
		if align==2 :
			if len(ns)>2:
				refnode=ns[0]
				xref=refnode.xpos()
				yref=refnode.ypos()
				refnode2=ns[1]
				xref2=refnode2.xpos()
				yref2=refnode2.ypos()
				deltax=xref2-xref
				deltay=yref2-yref        
				ns=ns[2:]
				count=1
				for n in ns :
					n.setXpos(xref2+(deltax*count))
					n.setYpos(yref2+(deltay*count))
					count+=1

		else :
			if len(ns)>1 :
				refnode=ns[0]
				xref=refnode.xpos()
				yref=refnode.ypos()
				ns=ns[1:]

				for n in ns:

					if align==0 : #horizontal
						n.setYpos(yref)
					elif align==1 : #vertical
						n.setXpos(xref)

	else :
		print('Please select node(s).\nLast node will be the reference.\nFor 2ref mode, the last 2 nodes will be references.')



def textnode_script_template():
	t=nuke.createNode('Text2')
	msg="""
[file dirname [value root.name]]  #getting the folder for current project/script.
[getenv HOME] #user home folder

	"""
	t.knob('message').setValue(msg)


def ccopy_file(srcfile, destfolder):
	# COPY FILE TO DESTINATION FOLDER AND 
	# IF SUCCEEDED THEN RETURNS THE NEW DEST FILES WITH GENERATED INCREMENT NUMBER IF FILES EXIST.
	# IF FAIL RETURNS NONE/NULL
	import os
	from shutil import copyfile
	from claystudio import __cserverstat__, __cmsg__
	if not(__cserverstat__) : nuke.message(__cmsg__) ; return
 
	log = ""
	line = "--------------------------------------------------------------------"
	errmsg0 = "\n\n"+line+"\nERROR : " 

	if not os.path.exists(destfolder) :
		try :
			os.mkdir(destfolder)
			log += "\n+ Folder doesn't exist. Creating new one : "+destfolder
		except Exception as e :
			errmsg = "Can't create directory. "+str(e)
			return ["", log + errmsg0+ errmsg]
	else :
		if not os.path.isdir(destfolder) :
			errmsg = "Can't copy images. '"+ destfolder+"' exists but it's not a folder."
			return ["", log + errmsg0+ errmsg]
	
	filename = os.path.basename(srcfile)
	dest = os.path.join(destfolder,filename)
	dest = dest.replace( '\\' , '/' )  # internal nuke to work with  
	if srcfile != dest :
		if os.path.isfile(srcfile):
			if not os.path.exists(dest) :
				try :
					copyfile(srcfile,dest)
					log += "\n+ copy successful"
				except Exception as e :
					errmsg = "Can't copy file. "+str(e)
					return ["", log + errmsg0+ errmsg]
			else :
				i =1
				while (True) :
					base , ext = os.path.splitext(filename)
					filename2 = base+"_"+str(i)+ext
					dest =os.path.join(destfolder,filename2)
					dest = dest.replace( '\\' , '/' )  # internal nuke to work with  
					if not os.path.exists(dest) :
						try :
							copyfile(srcfile,dest)
							log += "\n+ copy successful"
						except Exception as e :
							errmsg = "Can't copy file. "+ str(e)
							return ["", log + errmsg0+ errmsg]
						break
					else :
						i += 1
		else :
			# SKIPPED : SOURCE DOESN'T EXIST
			errmsg = srcfile+" -> Source doesn't exist."
			return ["", log + errmsg0+ errmsg]
	else :
		# SKIPPED : SOURCE AND DEST ARE THE SAME.
		errmsg = srcfile+" -> --SKIPPED-- : Destination and source are the same."
		return [dest, log + errmsg0+ errmsg]

	return [dest, log]



def ccollect_images(auto=0 , na=None) :
	# auto = 1 will use projectvol
	# na = list of nodes to be processed.

	from cxsetting import __root__
	from claystudio import __celementdir__
	import os , re
	line = "--------------------------------------------------------------------"
	errmsg0 = "\n\n"+line+"\nERROR : "
	log = "\n\nCOLLECT IMAGES\nclaystudio.2021\n"
	projectvol = nuke.root()['projectvol'].value()
	
	if na :
		if projectvol != "" :
			if not auto :
				# CREATE PANEL
				p = cxclass.CollectImagesPanel()
				ret = p.showModalDialog()
				if not ret : return # user has cancelled the process.
				usepvol = p.usepvol.value()
				relyes = p.relyes.value()
				relfolder = p.relfolder.value()
				step = str(p.step.value())
				abso = p.abs.value()
			else :
				usepvol =1

			# BEGIN
			# GENERATE DESTFOLDER

			# RUN IF AUTO OR IF IT'S CONFIRMED USING PANEL (OK)
			if not usepvol :
				log += "\n- Not using PROJECTVOL"
				if relyes :
					log += "\n- Using relative path"
					curpath = os.path.dirname(nuke.root().name()).strip()
					if curpath :
						log += "\n- Current script path : "+curpath
						targetfolder= relfolder.strip()
						if targetfolder :
							log += "\n- Target : "+targetfolder
							if step.strip().isdigit() :
								stepup = int(step)
								goup = ""
								for i in range(stepup):  
									goup = os.path.join(goup,'..') if goup else '..'
								destfolder = os.path.abspath(os.path.join(curpath, goup ,targetfolder))
								
							else :
								errmsg = "Step has to be numeric."
								nuke.message(errmsg)
								print((log + errmsg0+ errmsg))
								return
						else :
							errmsg = "Relative folder is empty."
							nuke.message(errmsg)
							print((log + errmsg0+ errmsg))
							return
					else :
						errmsg = "Please save the project first.\nRelative folder can't be used\nwithout saving the project."
						nuke.message(errmsg)
						print((log + errmsg0+ errmsg))
						return

				else :
					log += "\n- Using Absolute path"
					destfolder = abso.strip()
					if destfolder :
						if not os.path.exists(destfolder) :
							errmsg = "Folder doesn't exist : " + destfolder
							nuke.message(errmsg)
							print((log + errmsg0+ errmsg))
							return
						else :
							if os.path.isfile(destfolder) :
								destfolder = os.path.dirname(destfolder)
						
					else :
						errmsg = "Abs folder is empty."
						nuke.message(errmsg)
						print((log + errmsg0+ errmsg))
						return
					
	
			else :
				log += "\n- Using PROJECTVOL"
				destfolder = os.path.join(projectvol,__celementdir__)
	
			log += "\n- Dest : "+ destfolder
	

			# COPYING FILES
			err = 0
			skip = 0
			copy = 0
			for n in na :
				file = n['file'].value()
				log += "\n"+line+"\n+ Process : "+n.name()
				log += "\n+ from : "+ file
				if not file.startswith(projectvol) and not file.startswith(__root__) :
					if not nuke.tcl('set x ' + file ).startswith(projectvol) and not nuke.tcl('set x ' + file ).startswith(__root__) : # for filename using script/expression
						if (os.path.dirname(file)) != (destfolder) :
							srcfile = n['file'].value()
							seq = re.search( r'(\w*)(.*)%0([1-9]+)d(.*?)(\w*)$'  , os.path.basename(srcfile) )
							if seq :
								base = seq.groups()[0]
								dlm1 = seq.groups()[1]
								digit = int(seq.groups()[2])
								dlm2 = seq.groups()[3]
								ext = seq.groups()[4]
								startfrm = n['origfirst'].value()
								lastfrm = n['origlast'].value()
								i = 0
								subfolder = base+"_"+str(i).zfill(3)
								destfolder2 = destfolder + "/" + subfolder
			
								# CREATE NEW FOLDER IF EXISTS.
								while os.path.exists(destfolder2) : 
									i += 1
									subfolder = base+"_"+str(i).zfill(3)
									destfolder2 = destfolder + "/" + subfolder
			
								# LOOPING THROUGH SEQUENCES TO COPY
								log2="" 
								dest = destfolder2 +"/"+base+dlm1+"%0"+str(digit)+"d"+dlm2+ext
								for i in range(startfrm, lastfrm +1) :
									srcfolder = os.path.dirname(srcfile)
									srcfilename = base+dlm1 + str(i).zfill(digit) + dlm2 + ext
									srcfile = srcfolder + "/" + srcfilename 
									if not ccopy_file(srcfile,destfolder2)[0] : 
										dest = "" # set dest to "" if fail copying.
									log2 += "\n"+ccopy_file(srcfile,destfolder2)[1]
									
								n.knob('file').setValue(dest)  
			
							else :
								dest,log2 = ccopy_file(srcfile,destfolder)
								n.knob('file').setValue(dest)  
							log += ("\n+ to : "+dest) 
							log += "\n"+log2
							if  dest == "" :
								err += 1
								log+= "\n+ "+ file + " -> Error copying files."
							else :
								copy +=1

						else :
							skip += 1
							log += "\n\n+ --SKIPPED-- source and target folder are the same"
				else :
					skip += 1
					log += "\n\n+ --SKIPPED-- File already in PROJECTVOL"

			log += "\n"+line+"\n"
			logprint = "\nTotal process : "+ str(len(na))
			logprint += "\nCopy : " + str(copy)
			logprint += "\nSkip : " + str(skip)
			logprint += "\nError : "+ str(err)
			log += logprint

			# IF ANY ERRORS
			if err :
				errmsg = "\nThere are "+str(err)+" errors."
				nuke.message(errmsg+"\nPls check the logs on script editor.")
				log += errmsg
			else : 
				log += "\n"+str(copy)+" file(s) has been successfully copied." if copy >0 else ""

		else :
			# PROJECTVOL IS NULL OR EMPTY OR NOT SET
			errmsg = "PROJECTVOL has not been set.\nPlese create PROJECTVOL from CLAY menu first."
			nuke.message(errmsg)
			print((log + errmsg0+ errmsg))
			return
	else :
		# NO NODES
		errmsg = "No Read Nodes"
		nuke.message(errmsg)
		print((log + errmsg0+ errmsg))
		return		

	print(log)
	nuke.message("Collect Images\nclaystudio@2021\n"+ logprint+ ("\n\nPlease check the error logs " if err else "") )




def cclayserver_info():
	from claystudio import __clayservers__ , __cserverips__, __cserverfolder__, scheck,__cname__
	from cxsetting import __platformlabel__, __home__,__user__
	text = ""
	br= "\n"
	text += __cname__ + br+br

	text += "IP ADDRESS : " + ','.join(__cserverips__) + br
	text += "NET FOLDER : " + __cserverfolder__ + br + br
	text += "HOME : " + __home__ + br
	text += "USER : " + __user__ + br
	text += "PLATFORM : " + __platformlabel__ + br + br

	text += "SERVER LIST :" + br
	for i in range(len(__clayservers__)):
		text += "\t"+str(i+1)+". "+__clayservers__[i] + br
	text +=  br *2
	text += "--------------------------------------------" + br
	text += "STATUS : "+ ("CONNECTED" if scheck() else "DISCONNECTED")+br
	text += "--------------------------------------------" + br
	nuke.message(text)



def cset_remaps() :
	from claystudio import  __cwinroot__, __cmacroot__,__clinuxroot__, __cwinuser__,__cmacuser__,__clinuxuser__,__cwinfont__,__cmacfont__,__clinuxfont__
	# import string
	# windrive = ' '.join(list(string.ascii_uppercase))
	# p = nuke.Panel('CLAYFX REMAPS')
	# #p.addEnumerationPulldown('Windows Project Root Drive : ', windrive)
	# p.addSingleLineInput("User Name : ","")
	# ret = p.show()

	# if ret :
	#oldremaps = nuke.toNode('preferences').knob('platformPathRemaps').toScript()
	winroot = __cwinroot__+"/"
	macroot = __cmacroot__+"/"
	linuxroot = __clinuxroot__+"/"
	winfont = __cwinfont__+"/"
	macfont = __cmacfont__+"/"
	linuxfont = __clinuxfont__+"/"
	winuser = __cwinuser__+"/"
	macuser = __cmacuser__+"/"
	linuxuser = __clinuxuser__+"/"
	
	# PROJECT VOL
	newremaps = winroot + ";" + macroot + ";" + linuxroot + ";"

	# USER HOME DIR
	newremaps += winuser+";" + macuser+";" + linuxuser + ";"

	# FONTS DIR
	newremaps += winfont+ ";" + macfont+ ";" + linuxfont + ";"
	nuke.toNode('preferences').knob('platformPathRemaps').fromScript(newremaps)
	





def cset_localization(projectvol):
	from claystudio import __cserverfolder__ , __clocalization__ 
	from cxsetting import __root__
	p = nuke.toNode('preferences')
	auto_local_cache_path = __root__ + "/" + __cserverfolder__ + "/"
	local_cache_path = __root__ + "/" + __clocalization__ + "/"
	p.knob('LocalizationPolicyDefault').setValue('fromAutoLocalizePath')
	p.knob('autoLocalCachePath').setValue(auto_local_cache_path)
	p.knob('localCachePath').setValue(local_cache_path)



def create_projectvol():
	from sys import platform
	from cxsetting import __osdict__ , __home__
	from claystudio import   __cprojectvol__, __cuserpref__
	from os import mkdir
	from os.path import basename,dirname, exists, isfile,isdir

	# ask to input project location
	p = nuke.Panel('CFX PROJECT SETUP')
	p.addFilenameSearch('Project Location', __home__.replace("\\", "/") + "/Desktop/" + __cprojectvol__  )
	p.setWidth(500)
	ret = p.show()
	e = None ; log = "" ; pathvol = None
	if ret :
		path = p.value('Project Location').strip()
		path = path[:-1] if path[-1] == "/" else path	
	
		if exists(path) :
			# Path exists (folders or files)
			if isfile(path) :
				# is file
				#log += path+" is a file.\n"
				path = dirname(path)
				pathvol = path+ "/" +__cprojectvol__
				if exists(pathvol) :
					# Project folder exist
					log += __cprojectvol__ + " already exists.\n"
					log +=  pathvol
				else :
					# Create new one.
					try :
						mkdir(pathvol)
						log += __cprojectvol__ + " has been created.\n"
						log +=  pathvol 
					except Exception as e :
						log += "status : ERROR\nCan't create folder :" + str(e)+ "/"

			
			else :
				# is folder
				#log += path+" is a folder.\n"
				if (basename(path) != __cprojectvol__):
					# if curr dir is not PROJECT vol
					pathvol = path+"/"+__cprojectvol__
					if exists(pathvol) :
						# Project folder exists.
						log += __cprojectvol__ + " already exists.\n"
						log +=  pathvol
					else :
						# Create Project vol
						try :
							mkdir(pathvol)
							log += __cprojectvol__ + " has been created.\n"
							log +=  pathvol
						except Exception as e :
							log += "status : ERROR\nCan't create folder :" + str(e)+ "/"
				else :
					# cur dir is PROJECT vol.
					log += __cprojectvol__ + " already exists.\n"
					log += path
					pathvol = path

			# write to file
			cwrite_userpref('projectvol',pathvol)

			# set localization folder
			cset_localization(pathvol)
	
		else :
			# Path is Invalid
			e = "Path doesn't exist"
			log = "ERROR\n\n" + path + " does not exist."

		log += "\nstatus : OK"
  
	else :
		# user cancel
		e = -1
  
	return e,log, pathvol



def clayenv_setup():
	# claystudio environment setup
	# run this on first studio setup
	from PySide2 import QtWidgets
	
	proc = nuke.ask("Claystudio environment setup\n-------------------------------------------\n\nPlease save your project !\n\nNuke will be restarted after this process.\n\nThis process will also reset :\n   - Project location\n   - Directory Remaps\n   - Localization\n\n\nContinue ?")

	if proc :    
		log = "Claystudio environment setup\n\n"

		# create projectvol
		log += "> Creating Projectvol :\n"
		err, log2, pathvol = create_projectvol()
		log += log2

		# if user cancel then exit
		if err == -1 :
			return
			
		# if projectvol succeeded, set remaps
		if not err :
			log += "\n\n\n> Remaps and Localization :\n"
			try :
				cset_remaps()
				cset_localization(pathvol)
				csave_preferences_to_file()
				log += "Status : OK"
			except Exception as e :
				log += "Status : Error\n" + str(e)
				err = 1

		# print log and show message
		print(log)	
		messageBox = QtWidgets.QMessageBox()
		messageBox.setText(log)
		messageBox.exec_()

		# restart if successful or no error
		if not err :
			messageBox = QtWidgets.QMessageBox()
			messageBox.setText("The setup has been done.\n\nNuke will restart now.")
			messageBox.exec_()
			nuke.scriptNew()
			quit()



def cwrite_userpref(key,value):
	# import pickle
	from os.path import isfile
	from claystudio import  __cuserpref__
	from cxsetting import __home__

	userpref = __home__+"/.nuke/"+ __cuserpref__
	userdict ={}
	if isfile(userpref) :
		with open(userpref,'r') as pref :
			userdata = pref.read().strip()
			

		if  userdata != "" :
			userdata = userdata.split('\n')
			for i in userdata :
				j = i.split('::')
				userdict[j[0]]=j[1]

	userdict[key] = value
	datastring = ""
	for key in list(userdict.keys()) :
		datastring += key + "::" + userdict[key]+"\n"
	datastring = datastring.strip()

	with open(userpref,'w') as pref :
		pref.write(datastring)
		# pickle.dump(datastring,pref)




def cread_userpref(key) :
	from os.path import isfile
	from claystudio import  __cuserpref__
	from cxsetting import __home__
 
	userpref = __home__+"/.nuke/"+ __cuserpref__

	userdict ={}
	if isfile(userpref) :
		with open(userpref,'r') as pref :
			userdata = pref.read().strip()

		if userdata != "" :
			userdata = userdata.split('\n')
			for i in userdata :
				j = i.split('::')
				userdict[j[0]]=j[1]
			return userdict[key]
		else :
			return ""
	return ""




def move_backdrop(bd,xNew,yNew) :
	#Old position of Backdrop#
	positionX = bd.xpos()
	positionY = bd.ypos()   

	#Select nodes in Backdrop#
	nukescripts.clear_selection_recursive()
	bd.selectNodes(True)

	#Move Backdrop to new position#
	bd.setXYpos(xNew, yNew)

	#Calculate offset between new and old Backdrop position#
	offsetX = positionX - bd.xpos()
	offsetY = positionY - bd.ypos()

	### Set new position for nodes in Backdrop ###
	for n in nuke.selectedNodes():
			curXpos = n.xpos()
			curYpos = n.ypos()
			n.setXYpos(curXpos - offsetX , curYpos - offsetY)  
	nukescripts.clear_selection_recursive()



def viewer_handles() :
	firstFrame = int(nuke.Root()['first_frame'].value())
	lastFrame = int(nuke.Root()['last_frame'].value())
	inhandles = outhandles = int(nuke.root().knob('cxhandles').value())
	viewer_range = str(int(firstFrame)+ inhandles) + '-' + str(int(lastFrame)-outhandles) 
	viewer_node = nuke.activeViewer().node()

	viewer_node['frame_range_lock'].setValue(True)
	viewer_node['frame_range'].setValue(viewer_range)


def colorspace_outputrec709() :
	# set colorspace to 'output rec709' for ACES workflow
	ns = nuke.selectedNodes()
	for i in ns :
		i.knob('colorspace').setValue("Output - Rec.709")


def hex_to_rgb(val):
	# val = integer value from colorchip format
	# return array of 2 list format : 0-255 and 0-1 
	hexval =hex(val)[2:-2].zfill(6).upper()
	rgbrval = float(int(hexval[0:2] , 16)) # red
	rgbgval = float(int(hexval[2:4] , 16)) # green
	rgbbval = float(int(hexval[4:6] , 16)) # blue

	# rgb 0 - 255
	rgbval1 =  [int(rgbrval) , int(rgbgval) , int(rgbbval) ]

	# rgb 0 -1
	rgbval2 = [ 1 if (rgbrval/255)==1 else ( 0 if (rgbrval/255)==0 else round(rgbrval/255,3)  ) , 1 if (rgbgval/255) ==1 else ( 0 if (rgbgval/255) ==0 else round(rgbgval/255,3) ) , 1 if (rgbbval/255)==1 else ( 0 if (rgbbval/255)==0 else round(rgbbval/255,3) ) ]
	
	# output 2 list format 
	# [ [r1,g1,b1] of 0-255 , [r2,g2,b2] of 0-1]
	return [rgbval1, rgbval2]


def tempfunction() :
	ws = nuke.allNodes('Write')
	for w in ws :
		file = w.knob('file').value()
		file = file.replace('andi', 'ponco')
		w.knob('file').setValue(file)


def label_as_name():
	ns = nuke.selectedNodes()
	if ns :
		val = ns[0].knob('autolabel').value()
		val = "nuke.thisNode().knob('label').value()" if val=="" else ""
		for n in ns :
			n.knob('autolabel').setValue(val)

def readwrite_showhide_path():
	ns = nuke.selectedNodes()
	if ns :
		val = not ns[0].knob('cxshowdir').value()
		for n in ns :
			n.knob('cxshowdir').setValue(val)


def node_tree_list():
	pathlist = []
	filename = os.path.basename(nuke.root().knob('name').value())
	parent = ""
	parent = nuke.thisNode().parent()

	while os.path.basename(parent.name()) != filename :
		pathlist.append(  ( os.path.basename( parent.name()) )  )
		parent = parent.parent()
		
	pathlist.reverse()
	return(pathlist)
