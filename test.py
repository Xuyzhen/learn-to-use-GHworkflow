from solution import Solution

s = Solution()

cmds1 = [
    'interface GigabitEthernet0/0/1 port trunk allow-pass vlan 1 to 10',
    'interface GigabitEthernet0/0/2 port trunk allow-pass vlan 5 to 15',
    'interface GigabitEthernet0/0/3 port trunk allow-pass vlan 20',
]
print('Test 1:', s.merge_cmds(cmds1))

cmds2 = [
    'interface GigabitEthernet0/0/1 port trunk allow-pass vlan 1 to 10',
    'interface GigabitEthernet0/0/1 undo port trunk allow-pass vlan 5 to 7',
]
print('Test 2:', s.merge_cmds(cmds2))

cmds3 = [
    'interface GigabitEthernet0/0/1 port trunk allow-pass vlan 100',
]
print('Test 3:', s.merge_cmds(cmds3))

cmds4 = [
    'interface GigabitEthernet0/0/1 port trunk allow-pass vlan 1 to 4096',
]
print('Test 4:', s.merge_cmds(cmds4))

cmds5 = []
print('Test 5:', s.merge_cmds(cmds5))

cmds6 = [
    'interface GigabitEthernet0/0/1 port trunk allow-pass vlan 1 to 10',
    'interface GigabitEthernet0/0/1 undo port trunk allow-pass vlan 1 to 10',
]
print('Test 6:', s.merge_cmds(cmds6))

cmds7 = [
    'interface GigabitEthernet0/0/1 port trunk allow-pass vlan 5',
    'interface GigabitEthernet0/0/2 port trunk allow-pass vlan 10',
    'interface GigabitEthernet0/0/3 port trunk allow-pass vlan 20',
]
print('Test 7:', s.merge_cmds(cmds7))

print(1)
