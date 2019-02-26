from apex_legends import ApexLegends

apex = ApexLegends("af6873a1-ef18-4ea4-aced-143ba5b6eb5d")

player = apex.player('SirMammington')

print(player)

# for legend in player.legends:
#     print(legend.legend_name)
#     print(legend.icon)
#     print(legend.damage)
#     print(legend.kills)
b={}
for legend in player.legends:
	for a in dir(legend):
		if a == 'damage' or 'kills' in a:
			b[a] = player.__dict__[a]
# b.append([player.__dict__[a] for a in dir(legend) if a == 'damage' or 'kills' in a])
print(b)
print(player.__dict__.keys())
print(player.legends[0].__dict__.keys())
print(player.legends[0].__dict__['specific2'])
