import re
__FLOAT_REG=r"\d+.\d+|\d+"
__SIZE_REG=r"\d+[p|n]"

def base_parser(regex, line):
    matches = re.finditer(regex, line)
    groups = []
    for match in matches:
        for groupNum in range(0, len(match.groups())):
            groupNum = groupNum + 1
            groups.append(match.group(groupNum))
    return groups

def parse_guassian_distribution(line):
    regex = r".param\s+([a-zA-Z_\d]+)\s*=\s*(GAUSS)\s*\(\s*({float})\s*,\s*({float})\s*,\s*({float})\s*\)".format(float=__FLOAT_REG)
    return base_parser(regex, line)

def parse_monte(line):
    regex = r".tran\s+({size})\s+({size})\s+sweep\s+monte\s*=\s*(\d+)".format(size=__SIZE_REG)
    return base_parser(regex, line)



if __name__ == "__main__":
    test_str = ".param myVariable_23 = GAUSS (1 , 0.20 , 1)"
    g_dist = parse_guassian_distribution(test_str)
    print(g_dist)

    test_str = ".tran 10p 40n sweep monte=10"
    monte = parse_monte(test_str)
    print(monte)