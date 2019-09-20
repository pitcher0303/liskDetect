import os

myStr = "Object:Person,HardHatEnd"
search1 = "tt:"
rootPath = os.getcwd()

print(myStr.find(search1))
print(len(search1))
search1_len = len(search1)
start_slicing = myStr.find(search1)
end_slicing = search1_len
print(myStr[start_slicing:end_slicing])

f = open(rootPath + "/data/obj.names", 'r')
lines = f.read().splitlines()
lines.append("property")
name_dic = {}
for line in lines:
    name_dic[line] = 0
print(name_dic)
# print(name_dic['tt'])
print(lines)
f.close()

myStr = 'DS,person:O,chair:O,'
print(myStr.startswith('DS,'))
result_list = myStr.split(',')
print(result_list)
print(len(result_list))
print(result_list[0])

print()

for result in result_list:
    resultP = result.split(':')
    print(resultP)
    if len(resultP) == 2:
        try:
            name_dic[resultP[0]] = 1
        except KeyError:
            pass
print(name_dic)

num = 0.0
for line in lines:
    num += name_dic[line]
print(num/5)
