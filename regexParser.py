import re
__FLOAT_REG=r"\d+.\d+|\d+"
__SIZE_REG=r"\d+[p|n]"
__VARIABLE_NAME=r"[a-zA-Z_\d]"

def base_parser(regex, line):
    matches = re.finditer(regex, line)
    groups = []
    for match in matches:
        for groupNum in range(0, len(match.groups())):
            groupNum = groupNum + 1
            groups.append(match.group(groupNum))
    return groups

def parse_guassian_distribution(line):
    regex = r".param\s+({variable}+)\s*=\s*(GAUSS)\s*\(\s*({float})\s*,\s*({float})\s*,\s*({float})\s*\)".format(float=__FLOAT_REG, variable=__VARIABLE_NAME)
    return base_parser(regex, line)

def parse_monte(line):
    regex = r"(.tran\s+{size}\s+{size})\s+sweep\s+monte\s*=\s*(\d+)".format(size=__SIZE_REG)
    return base_parser(regex, line)

def parse_sizing_monte(line):
    regex = r"([\w\d\s]+)([L|W]\s*=)\s*(\d+[p|n]*)\s*\*\s*([a-zA-Z_\d]+)"
    return base_parser(regex, line)

def parse_tran_size(line):
    regex = r"(\d+)([n|p])"
    return base_parser(regex, line)

def parse_include(line):
    regex = r"(.include\s*)(')([\w.]*')"
    return base_parser(regex, line)

def parse_aging_part(content):
    regex = r"([\s\S]*\*<---BeginAging--->)([\s\S]*)?(\*<---EndAging--->[\s\S]*)"
    return base_parser(regex, content)

def parse_measure(line):
    regex = r".measure\s*tran\s*([a-zA-Z_\d]*)"
    return base_parser(regex, line)

def parse_lis_delay(variable_names, line):
    variables = '|'.join(variable_names)
    regex = r"({vars})\s*=\s*(\d+.\d+|\d+)([p|n])".format(vars=variables)
    return base_parser(regex, line)

if __name__ == "__main__":
    test_str = ".param myVariable_23 = GAUSS (1 , 0.20 , 1)"
    g_dist = parse_guassian_distribution(test_str)
    print(g_dist)

    test_str = ".tran 10p 40n sweep monte=10"
    monte = parse_monte(test_str)
    print(monte)

    test_str = ("M1 ss ina 0 0  nmos L=32n*c W=64n*d\n")
    monte_s = parse_sizing_monte(test_str)
    print(monte_s)

    test_str = "32n"
    size = parse_tran_size(test_str) 
    print(size)

    test_str = ".include '32nm_LP.pm'"
    include = parse_include(test_str)
    print(include)

    test_str = ".measure tran tpd param='(tlh+thl/2)'"
    measure = parse_measure(test_str)
    print(measure)

    test_str = "tlh=  29.7972p  targ=   1.0323n   trig=   1.0025n"
    delay = parse_lis_delay(['tlh', 'thl', 'tpd'], test_str)
    print(delay)