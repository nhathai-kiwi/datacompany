district_txt = 'district.txt'

f = open(district_txt, 'r')
for line in f:
    dis = line.split(' ')
    print dis[0], " ", dis[1]