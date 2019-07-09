#approach by splitting annotations (not images). Images can appear in multiple sets, but with different annotations.



import copy

import random

random.seed(30)

ann_path = "../datasets/coco/annotations/"

# 				  train val test
sets_percentages = [80, 20, 10]

import json
with open(ann_path + 'instances_all.json') as f:
    instances = json.load(f)

print("Annotations:" + str(len(instances['annotations'])))
print("Images:" + str(len(instances['images'])))

train_ann = {
	'year': instances['year'],
	'categories': instances['categories'],
	'annotations': [],
	'licenses': instances['licenses'],
	'type': instances['type'],
	'info': instances['info'],
	'images': []
}
val_ann = copy.deepcopy(train_ann)
test_ann = copy.deepcopy(train_ann)

if sum(sets_percentages) != 100:
	print("Values not valid, doing 80% train, 10 val and 10 test!")
	sets_percentages = [80, 10, 10]

split_percs = [0]
for perc in sets_percentages:
	#make it cumulative
	last_perc = split_percs.pop()
	split_percs.extend([last_perc + perc] * 2)
split_percs.pop()
# now is [80, 90, 100]

images = [ [None] * len(instances['images']) for i in range(3)]
# images has the images referenced by the annotations for each set

for cat in instances['categories']:
	cat_id = cat['id']
	cat_anns = [0, 0, 0] #annotations for this category per each set
	for ann in instances['annotations']:
		ann_cat_id = ann['category_id']
		ann_img_id = ann['image_id']
		if cat_id == ann_cat_id:
			p = random.random() * 100
			if p < split_percs[0]:
				train_ann['annotations'].append(ann)
				cat_anns[0] += 1
				if ann_img_id not in train_ann['images']:
					train_ann['images'].append(ann_img_id) #temporary, will add later the complete info
			elif split_percs[0] <= p < split_percs[1]:
				val_ann['annotations'].append(ann)
				cat_anns[1] += 1
				if ann_img_id not in val_ann['images']:
					val_ann['images'].append(ann_img_id) #temporary, will add later the complete info
			elif p <= split_percs[2]:
				test_ann['annotations'].append(ann)
				cat_anns[2] += 1
				if ann_img_id not in test_ann['images']:
					test_ann['images'].append(ann_img_id) #temporary, will add later the complete info
	print("Category ID: " + str(cat_id) + "\tCat Anns: " + str(sum(cat_anns)) + "\tCat Percs:" + str([i / sum(cat_anns) * 100 for i in cat_anns]))


print("Result sum annotations:" + str(sum([len(train_ann['annotations']), len(val_ann['annotations']), len(test_ann['annotations'])])))
print("Result sum images:" + str(sum([len(train_ann['images']), len(val_ann['images']), len(test_ann['images'])])))
print()
print("Replacing images..")
for img in instances['images']:
	# replace ids with images dictionaries
	img_id = img['id']
	for index, value in enumerate(train_ann['images']):
		if value == img_id:
			train_ann['images'][index] = img
	for index, value in enumerate(val_ann['images']):
		if value == img_id:
			val_ann['images'][index] = img
	for index, value in enumerate(test_ann['images']):
		if value == img_id:
			test_ann['images'][index] = img
print()
print("Now writing files..")
with open(ann_path + 'instances_train.json', 'w') as outfile:
	json.dump(train_ann, outfile)

with open(ann_path + 'instances_val.json', 'w') as outfile:
	json.dump(val_ann, outfile)

with open(ann_path + 'instances_test.json', 'w') as outfile:
	json.dump(test_ann, outfile)