from typing import List


class Solution:
    def merge_cmds(self, cmds: List[str]) -> str:
        id_range = [''] * 4097

        def en_cmd(cmd_port: List[str]):
            for element in range(len(cmd_port)):
                if cmd_port[element] == 'to':
                    for i in range(int(cmd_port[element - 1]), int(cmd_port[element + 1]) + 1):
                        id_range[i] = '1'
                    cmd_port[element], cmd_port[element + 1], cmd_port[element - 1] = '-1', '-1', '-1'
            for port in cmd_port:
                if port != '-1':
                    id_range[int(port)] = '1'

        def disa_cmd(cmd_port: List[str]):
            for element in range(len(cmd_port)):
                if cmd_port[element] == 'to':
                    for i in range(int(cmd_port[element - 1]), int(cmd_port[element + 1]) + 1):
                        id_range[i] = ''
                    cmd_port[element], cmd_port[element + 1], cmd_port[element - 1] = '-1', '-1', '-1'
            for port in cmd_port:
                if port != '-1':
                    id_range[int(port)] = ''

        for command in cmds:
            parts = command.split()
            vlan_idx = parts.index('vlan')
            cmd_port = parts[vlan_idx + 1:]

            if 'undo' in parts:
                disa_cmd(cmd_port)
            else:
                en_cmd(cmd_port)

        output_parts = []
        i = 1
        while i <= 4096:
            if id_range[i] == '1':
                start = i
                while i + 1 <= 4096 and id_range[i + 1] == '1':
                    i += 1
                end = i
                if start == end:
                    output_parts.append(str(start))
                else:
                    output_parts.append(f'{start} to {end}')
            i += 1

        return 'port trunk allow-pass vlan' + (' ' + ' '.join(output_parts) if output_parts else '')
