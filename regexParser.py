import re
__FLOAT_REG=r"\d+.\d+|\d+"
def parse_guassian_distribution(line):
    regex = r".param\s+([a-zA-Z_\d]+)\s*=\s*GAUSS\s*\(\s*({float})\s*,\s*({float})\s*,\s*({float})\s*\)".format(float=__FLOAT_REG)
    matches = re.finditer(regex, line)
    groups = []
    for match in matches:
        for groupNum in range(0, len(match.groups())):
            groupNum = groupNum + 1
            groups.append(match.group(groupNum))
    return groups
    



if __name__ == "__main__":
    test_str = ".param myVariable_23 = GUSS (1 , 0.20 , 1)"
    a = parse_guassian_distribution(test_str)
    print(a)