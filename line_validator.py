from constants import INTETRVAL

def is_line_valid(line):
    if (line.startswith('0') or line.startswith('1') or line.startswith('2') or
        line.startswith('3') or line.startswith('4') or
        line.startswith('5') or line.startswith('6') or
        line.startswith('7') or line.startswith('8') or
        line.startswith('9') or line.startswith('a')):
        return True
    return False


def parse_line(line, base_time):
    strs = line.replace('\n', '').split(',')
    if line.startswith('a'):
        base_time = int(strs[0][1:])
        time = base_time
    else:
        time = base_time + int(strs[0]) * INTETRVAL

    data = {
        'Time': time,
        'Close': strs[1],
        'High': strs[2],
        'Low': strs[3],
        'Open': strs[4],
        'Volumn': strs[5] 
    }
    return data, base_time