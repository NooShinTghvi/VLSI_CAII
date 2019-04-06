import re
import json
import time

global timescale
global endtime

class Nodes:
    def __init__(self, name):
        self.name = name
        self.path = ""
        self.time0 = 0
        self.time1 = 0
        self.timex = 0


class VCDParseError(Exception):
    pass


def list_sigs(file):
    """Parse input VCD file into data structure,
    then return just a list of the signal names."""

    vcd = parse_vcd(file, only_sigs=1)

    sigs = []
    for k in vcd.keys():
        v = vcd[k]
        nets = v['nets']
        sigs.extend(n['hier'] + '.' + n['name'] for n in nets)

    return sigs


def parse_vcd(file, only_sigs=0, use_stdout=0, siglist=[], opt_timescale=''):
    """Parse input VCD file into data structure.
    Also, print t-v pairs to STDOUT, if requested."""

    global endtime

    usigs = {}
    for i in siglist:
        usigs[i] = 1

    if len(usigs):
        all_sigs = 0
    else:
        all_sigs = 1

    node = []
    data = {}
    mult = 0
    num_sigs = 0
    hier = []
    time = 0

    with open(file, 'r') as fh:
        while True:
            line = fh.readline()
            if line == '':  # EOF
                break

            # chomp
            # s/ ^ \s+ //x
            line = line.strip()

            # if nothing left after we strip whitespace, go to next line
            if line == '':
                continue

            # put most frequent lines encountered at start of if/elif, so other
            #   clauses usually don't need to be tested
            if line[0] in ('b', 'B', 'r', 'R'):
                (value, code) = line[1:].split()
                if (code in data):
                    if (use_stdout):
                        print(time, value)
                    else:
                        if 'tv' not in data[code]:
                            data[code]['tv'] = []
                        data[code]['tv'].append((time, value))

            elif line[0] in ('0', '1', 'x', 'X', 'z', 'Z'):
                value = line[0]
                code = line[1:]
                if (code in data):
                    if (use_stdout):
                        print(time, value)
                    else:
                        if 'tv' not in data[code]:
                            data[code]['tv'] = []
                        data[code]['tv'].append((time, value))

            elif line[0] == '#':
                time = mult * int(line[1:])
                endtime = time

            elif "$enddefinitions" in line:
                num_sigs = len(data)
                if (num_sigs == 0):
                    if (all_sigs):
                        VCDParseError("Error: No signals were found in the "
                                      "VCD file " + file + ". Check the VCD file for "
                                                           "proper var syntax.")

                    else:
                        VCDParseError("Error: No matching signals were found "
                                      "in the VCD file " + file + ". Use list_sigs to "
                                                                  "view all signals in the VCD file.")

                if ((num_sigs > 1) and use_stdout):
                    VCDParseError("Error: There are too many signals "
                                  "(num_sigs) for output to STDOUT.  Use list_sigs "
                                  "to select a single signal.")

                if only_sigs:
                    break

            elif "$timescale" in line:
                statement = line
                if not "$end" in line:
                    while fh:
                        line = fh.readline()
                        statement += line
                        if "$end" in line:
                            break

                mult = calc_mult(statement, opt_timescale)

            elif "$scope" in line:
                # assumes all on one line
                #   $scope module dff end
                hier.append(line.split()[2])  # just keep scope name

            elif "$upscope" in line:
                hier.pop()

            elif "$var" in line:
                # assumes all on one line:
                #   $var reg 1 *@ data $end
                #   $var wire 4 ) addr [3:0] $end
                ls = line.split()
                type = ls[1]
                size = ls[2]
                code = ls[3]
                name = "".join(ls[4:-1])
                path = '.'.join(hier)
                full_name = path + '.' + name
                if (full_name in usigs) or all_sigs:
                    if code not in data:
                        data[code] = {}
                    if 'nets' not in data[code]:
                        data[code]['nets'] = []
                    var_struct = {
                        'type': type,
                        'name': name,
                        'size': size,
                        'hier': path,
                    }
                    if var_struct not in data[code]['nets']:
                        data[code]['nets'].append(var_struct)
                        node.append(Nodes(code))

    fh.close()

    return data, node


def calc_mult(statement, opt_timescale=''):
    """
    Calculate a new multiplier for time values.
    Input statement is complete timescale, for example:
      timescale 10ns end
    Input new_units is one of s|ms|us|ns|ps|fs.
    Return numeric multiplier.
    Also sets the package timescale variable.
    """

    global timescale

    fields = statement.split()
    fields.pop()  # delete end from array
    fields.pop(0)  # delete timescale from array
    tscale = ''.join(fields)

    new_units = ''
    if (opt_timescale != ''):
        new_units = opt_timescale.lower()
        new_units = re.sub(r"\s", '', new_units)
        timescale = "1" + new_units

    else:
        timescale = tscale
        return 1

    mult = 0
    units = 0
    ts_match = re.match(r"(\d+)([a-z]+)", tscale)
    if ts_match:
        mult = int(ts_match.group(1))
        units = ts_match.group(2).lower()

    else:
        VCDParseError("Error: Unsupported timescale found in VCD "
                      "file: " + tscale + ".  Refer to the Verilog LRM.")

    mults = {
        'fs': 1e-15,
        'ps': 1e-12,
        'ns': 1e-09,
        'us': 1e-06,
        'ms': 1e-03,
        's': 1e-00,
    }
    mults_keys = mults.keys()
    mults_keys.sort(key=lambda x: mults[x])
    usage = '|'.join(mults_keys)

    scale = 0
    if units in mults:
        scale = mults[units]

    else:
        VCDParseError("Error: Unsupported timescale units found in VCD "
                      "file: " + units + ".  Supported values are: " + usage)

    new_scale = 0
    if new_units in mults:
        new_scale = mults[new_units]

    else:
        VCDParseError("Error: Illegal user-supplied "
                      "timescale: " + new_units + ".  Legal values are: " + usage)

    return ((mult * scale) / new_scale)


def get_timescale():
    return timescale


def get_endtime():
    return endtime


def writeInFile_listSigs():
    start = time.time()
    input_listSigs = list_sigs('myFinalTest.vcd')
    end = time.time()
    print("Run Function(list_sigs): ", end - start)

    start = time.time()
    with open('demofile_listSigs.json', 'w') as file_listSigs:
        json.dump(input_listSigs, file_listSigs,
                  indent=4, separators=(". ", " = "))
    end = time.time()
    print("demofile_listSigs.json: ", end - start)

def calculteTimeANDProbability(node,vcd_data):
    finalTime = 2650001800
    file = open('P.txt', 'w')
    file.write("* * * * * * " + str(node[0].name) + " * * * * * *\n")
    file.write("* * * * * * " + str(node[1].name) + " * * * * * *\n")
    for i in range(2, len(node)):
        file.write("* * * * * * " + str(node[i].name) + " * * * * * *\n")
        tv_wave = vcd_data[node[i].name]["tv"]
        # firstTime = tv_wave[0][0]
        # firstValue = tv_wave[0][1]
        lastTime = tv_wave[1][0]
        lastValue = tv_wave[1][1]

        if (len(tv_wave) == 1):
            node[i].timex = finalTime
        else:
            node[i].timex = lastTime

        for j in range(2, len(tv_wave)):
            if (tv_wave[j][1] == "1"):
                newTime = tv_wave[j][0] - lastTime
                node[i].time0 = node[i].time0 + newTime
                lastTime = tv_wave[j][0]
                lastValue = tv_wave[j][1]

            elif (tv_wave[j][1] == "0"):
                newTime = tv_wave[j][0] - lastTime
                node[i].time1 = node[i].time1 + newTime
                lastTime = tv_wave[j][0]
                lastValue = tv_wave[j][1]
            else:
                newTime = tv_wave[j][0] - lastTime
                node[i].timex = node[i].timex + newTime
                lastTime = tv_wave[j][0]
                lastValue = tv_wave[j][1]

            if (i == len(tv_wave) - 1):
                if (lastValue == "1"):
                    newTime = finalTime - lastTime
                    node[i].time1 = node[i].time1 + newTime
                if (lastValue == "0"):
                    newTime = finalTime - lastTime
                    node[i].time0 = node[i].time0 + newTime

        file.write("Probability of Time = 0 :" + str(node[i].time0 / finalTime) + "\n")
        file.write("Probability of Time = 1 :" + str(node[i].time1 / finalTime) + "\n")
        # file.write("Probability of Time = x OR Z :" + str(node[i].timex/finalTime) + "\n")
        file.write("Probability of Total :" + str(
            node[i].time1 / finalTime + node[i].time0 / finalTime + node[i].timex / finalTime) + "\n")
        file.write("a : " + str((node[i].time0 / finalTime) * (node[i].time1 / finalTime)) + "\n")

if __name__ == '__main__':
    start = time.time()
    vcd_data, node = parse_vcd('myFinalTest.vcd')
    end = time.time()
    print("Run Function(parse_vcd): ", end - start)

    start = time.time()
    calculteTimeANDProbability(node,vcd_data)
    end = time.time()
    print("Run Function(calculteTimeANDProbability): ", end - start)