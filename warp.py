import yaml, random, argparse
from helpers import *
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

def roll(dictionary, level):
	answer = ''
	for item in sections:
		answer += ('{}: '.format(item.capitalize()))
		if item == 'mind':
			answer += '{}.'.format(find_answer(dictionary,dictionary.get(item),level))
		elif item == 'special':
			c = 0
			for i in range(0,rolls[level]):
				text = find_answer(dictionary,dictionary.get(item),level)
				if text != 'None':
					if c != 0:
						answer += ', '
					answer += text
					c += 1
				if c == max_special[level]:
					answer += '.'
					break
				elif i+1 < rolls[level]:
					pass
				elif c < max_special[level] and c > 0:
					answer += '.'
				elif i+1 == rolls[level] and c == 0:
					answer += 'None.'
		else:
			for i in range(0,rolls[level]):
				answer += find_answer(dictionary,dictionary.get(item),level)
				if i+1 < rolls[level]:
					answer += ', '
				else:
					answer += '. '
		answer += ('\n')
	return answer

def get_count(dictionary):
	num = 0
	for k,v in dictionary.items():
		if type(v) is dict:
			num += v.get('freq')
	return num

def find_answer(raw_dict, dictionary, level=-1, sub=False):
	if level == -1 and not sub:
		d = dictionary
	elif level == -1 and sub:
		d = sub
	else:
		d = dictionary.get(scales[level])
	rand = random.randrange(0,get_count(d),1)
	num = 0
	for k,v in d.items():
		num += v.get('freq')
		if num >= rand:
			if 'name' in v:
				if 'roll' in v and not 'other' in v:
					subs = ''
					for i in range(0,v.get('roll')):
						if subs:
							subs += ', {}'.format(find_answer(raw_dict,dictionary,0))
						else:
							subs += find_answer(raw_dict,dictionary,0)
					return '{} ({})'.format(v.get('name'),subs)
				elif 'roll' in v and 'other' in v:
					subs = ''
					for i in range(0,v.get('roll')):
						if subs:
							subs += ', {}'.format(find_answer(raw_dict,raw_dict.get(v.get('other')),1))
						else:
							subs += find_answer(raw_dict,raw_dict.get(v.get('other')),1)
					return '{} ({})'.format(v.get('name'),subs)
				else:
					return v.get('name')
			elif v.get('move') == 'up' and level < 3:
				return find_answer(raw_dict,dictionary,level+1)
			elif v.get('move') == 'down' and level > 0:
				return find_answer(raw_dict,dictionary,level-1)
			elif 'subtable' in v:
				return find_answer(raw_dict,dictionary,-1,v.get('subtable'))
			else:
				return 'Panic at the Disco!'

if __name__ == '__main__':
	# Set up all of the stuff to read command line arguments
	parser = argparse.ArgumentParser()

	parser.add_argument('-i', '--intensity', help='specify intensity of warping (0-3)', type=check_range, default=0)
	parser.add_argument('-d', '--database', help='specifiy yaml file to use as source', type=str, default='data.yaml')
	parser.add_argument('-c', '--clean', help='removes duplicates', action='store_true')
	parser.set_defaults(clean=False)

	args = parser.parse_args()

	# Move this somewhere cleaner
	scales = 'minor', 'moderate', 'major', 'extreme'
	rolls = 1, 2, 3, 5
	sections = 'mind', 'special', 'material', 'theme', 'focus'
	max_special = 1, 1, 2, 3

	# Load database from the specified file
	with open(args.database, 'r') as file:
		raw_dict = yaml.load(file, Loader=Loader)

	print(roll(raw_dict,args.intensity))