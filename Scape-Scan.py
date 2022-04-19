#!/usr/bin/python3

import argparse
import concurrent.futures
import shlex
from scapy.all import *
from termcolor import colored
import time
import random

TOP_PORTS = [1, 3, 4, 6, 7, 9, 13, 17, 19, 20, 21, 22, 23, 24, 25, 26, 30, 32, 33, 37, 42, 43, 49, 53, 70, 79, 80, 81,
             82, 83, 84, 85, 88, 89, 90, 99, 100, 106, 109, 110, 111, 113, 119, 125, 135, 139, 143, 144, 146, 161, 163,
             179, 199, 211, 212, 222, 254, 255, 256, 259, 264, 280, 301, 306, 311, 340, 366, 389, 406, 407, 416, 417,
             425, 427, 443, 444, 445, 458, 464, 465, 481, 497, 500, 512, 513, 514, 515, 524, 541, 543, 544, 545, 548,
             554, 555, 563, 587, 593, 616, 617, 625, 631, 636, 646, 648, 666, 667, 668, 683, 687, 691, 700, 705, 711,
             714, 720, 722, 726, 749, 765, 777, 783, 787, 800, 801, 808, 843, 873, 880, 888, 898, 900, 901, 902, 903,
             911, 912, 981, 987, 990, 992, 993, 995, 999, 1000, 1001, 1002, 1007, 1009, 1010, 1011, 1021, 1022, 1023,
             1024, 1025, 1026, 1027, 1028, 1029, 1030, 1031, 1032, 1033, 1034, 1035, 1036, 1037, 1038, 1039, 1040, 1041,
             1042, 1043, 1044, 1045, 1046, 1047, 1048, 1049, 1050, 1051, 1052, 1053, 1054, 1055, 1056, 1057, 1058, 1059,
             1060, 1061, 1062, 1063, 1064, 1065, 1066, 1067, 1068, 1069, 1070, 1071, 1072, 1073, 1074, 1075, 1076, 1077,
             1078, 1079, 1080, 1081, 1082, 1083, 1084, 1085, 1086, 1087, 1088, 1089, 1090, 1091, 1092, 1093, 1094, 1095,
             1096, 1097, 1098, 1099, 1100, 1102, 1104, 1105, 1106, 1107, 1108, 1110, 1111, 1112, 1113, 1114, 1117, 1119,
             1121, 1122, 1123, 1124, 1126, 1130, 1131, 1132, 1137, 1138, 1141, 1145, 1147, 1148, 1149, 1151, 1152, 1154,
             1163, 1164, 1165, 1166, 1169, 1174, 1175, 1183, 1185, 1186, 1187, 1192, 1198, 1199, 1201, 1213, 1216, 1217,
             1218, 1233, 1234, 1236, 1244, 1247, 1248, 1259, 1271, 1272, 1277, 1287, 1296, 1300, 1301, 1309, 1310, 1311,
             1322, 1328, 1334, 1352, 1417, 1433, 1434, 1443, 1455, 1461, 1494, 1500, 1501, 1503, 1521, 1524, 1533,
             1556, 1580, 1583, 1594, 1600, 1641, 1658, 1666, 1687, 1688, 1700, 1717, 1718, 1719, 1720, 1721, 1723, 1755,
             1761, 1782, 1783, 1801, 1805, 1812, 1839, 1840, 1862, 1863, 1864, 1875, 1900, 1914, 1935, 1947, 1971, 1972,
             1974, 1984, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2013, 2020, 2021,
             2022, 2030, 2033, 2034, 2035, 2038, 2040, 2041, 2042, 2043, 2045, 2046, 2047, 2048, 2049, 2065, 2068, 2099,
             2100, 2103, 2105, 2106, 2107, 2111, 2119, 2121, 2126, 2135, 2144, 2160, 2161, 2170, 2179, 2190, 2191, 2196,
             2200, 2222, 2251, 2260, 2288, 2301, 2323, 2366, 2381, 2382, 2383, 2393, 2394, 2399, 2401, 2492, 2500, 2522,
             2525, 2557, 2601, 2602, 2604, 2605, 2607, 2608, 2638, 2701, 2702, 2710, 2717, 2718, 2725, 2800, 2809, 2811,
             2869, 2875, 2909, 2910, 2920, 2967, 2968, 2998, 3000, 3001, 3003, 3005, 3006, 3007, 3011, 3013, 3017, 3030,
             3031, 3052, 3071, 3077, 3128, 3168, 3211, 3221, 3260, 3261, 3268, 3269, 3283, 3300, 3301, 3306, 3322, 3323,
             3324, 3325, 3333, 3351, 3367, 3369, 3370, 3371, 3372, 3389, 3390, 3404, 3476, 3493, 3517, 3527, 3546, 3551,
             3580, 3659, 3689, 3690, 3703, 3737, 3766, 3784, 3800, 3801, 3809, 3814, 3826, 3827, 3828, 3851, 3869, 3871,
             3878, 3880, 3889, 3905, 3914, 3918, 3920, 3945, 3971, 3986, 3995, 3998, 4000, 4001, 4002, 4003, 4004, 4005,
             4006, 4045, 4111, 4125, 4126, 4129, 4224, 4242, 4279, 4321, 4343, 4443, 4444, 4445, 4446, 4449, 4550, 4567,
             4662, 4848, 4899, 4900, 4998, 5000, 5001, 5002, 5003, 5004, 5009, 5030, 5033, 5050, 5051, 5054, 5060, 5061,
             5080, 5087, 5100, 5101, 5102, 5120, 5190, 5200, 5214, 5221, 5222, 5225, 5226, 5269, 5280, 5298, 5357, 5405,
             5414, 5431, 5432, 5440, 5500, 5510, 5544, 5550, 5555, 5560, 5566, 5631, 5633, 5666, 5678, 5679, 5718, 5730,
             5800, 5801, 5802, 5810, 5811, 5815, 5822, 5825, 5850, 5859, 5862, 5877, 5900, 5901, 5902, 5903, 5904, 5906,
             5907, 5910, 5911, 5915, 5922, 5925, 5950, 5952, 5959, 5960, 5961, 5962, 5963, 5987, 5988, 5989, 5998,
             5999, 6000, 6001, 6002, 6003, 6004, 6005, 6006, 6007, 6009, 6025, 6059, 6100, 6101, 6106, 6112, 6123, 6129,
             6156, 6346, 6389, 6502, 6510, 6543, 6547, 6565, 6566, 6567, 6580, 6646, 6666, 6667, 6668, 6669, 6689, 6692,
             6699, 6779, 6788, 6789, 6792, 6839, 6881, 6901, 6969, 7000, 7001, 7002, 7004, 7007, 7019, 7025, 7070, 7100,
             7103, 7106, 7200, 7201, 7402, 7435, 7443, 7496, 7512, 7625, 7627, 7676, 7741, 7777, 7778, 7800, 7911, 7920,
             7921, 7937, 7938, 7999, 8000, 8001, 8002, 8007, 8008, 8009, 8010, 8011, 8021, 8022, 8031, 8042, 8045, 8080,
             8081, 8082, 8083, 8084, 8085, 8086, 8087, 8088, 8089, 8090, 8093, 8099, 8100, 8180, 8181, 8192, 8193, 8194,
             8200, 8222, 8254, 8290, 8291, 8292, 8300, 8333, 8383, 8400, 8402, 8443, 8500, 8600, 8649, 8651, 8652, 8654,
             8701, 8800, 8873, 8888, 8899, 8994, 9000, 9001, 9002, 9003, 9009, 9010, 9011, 9040, 9050, 9071, 9080, 9081,
             9090, 9091, 9099, 9100, 9101, 9102, 9103, 9110, 9111, 9200, 9207, 9220, 9290, 9415, 9418, 9485, 9500, 9502,
             9503, 9535, 9575, 9593, 9594, 9595, 9618, 9666, 9876, 9877, 9878, 9898, 9900, 9917, 9929, 9943, 9944, 9968,
             9998, 9999, 10000, 10001, 10002, 10003, 10004, 10009, 10010, 10012, 10024, 10025, 10082, 10180, 10215,
             10243, 10566, 10616, 10617, 10621, 10626, 10628, 10629, 10778, 11110, 11111, 11967, 12000, 12174, 12265,
             12345, 13456, 13722, 13782, 13783, 14000, 14238, 14441, 14442, 15000, 15002, 15003, 15004, 15660, 15742,
             16000, 16001, 16012, 16016, 16018, 16080, 16113, 16992, 16993, 17877, 17988, 18040, 18101, 18988, 19101,
             19283, 19315, 19350, 19780, 19801, 19842, 20000, 20005, 20031, 20221, 20222, 20828, 21571, 22939, 23502,
             24444, 24800, 25734, 25735, 26214, 27000, 27352, 27353, 27355, 27356, 27715, 28201, 30000, 30718, 30951,
             31038, 31337, 32768, 32769, 32770, 32771, 32772, 32773, 32774, 32775, 32776, 32777, 32778, 32779, 32780,
             32781, 32782, 32783, 32784, 32785, 33354, 33899, 34571, 34572, 34573, 35500, 38292, 40193, 40911, 41511,
             42510, 44176, 44442, 44443, 44501, 45100, 48080, 49152, 49153, 49154, 49155, 49156, 49157, 49158, 49159,
             49160, 49161, 49163, 49165, 49167, 49175, 49176, 49400, 49999, 50000, 50001, 50002, 50003, 50006, 50300,
             50389, 50500, 50636, 50800, 51103, 51493, 52673, 52822, 52848, 52869, 54045, 54328, 55055, 55056, 55555,
             55600, 56737, 56738, 57294, 57797, 58080, 60020, 60443, 61532, 61900, 62078, 63331, 64623, 64680, 65000,
             65129, 65389]

TOP_STR = ",".join(str(i) for i in TOP_PORTS)


def title():
    title = """

███████╗ ██████╗ █████╗ ██████╗ ███████╗        ███████╗ ██████╗ █████╗ ███╗   ██╗
██╔════╝██╔════╝██╔══██╗██╔══██╗██╔════╝        ██╔════╝██╔════╝██╔══██╗████╗  ██║
███████╗██║     ███████║██████╔╝█████╗  ███████╗███████╗██║     ███████║██╔██╗ ██║
╚════██║██║     ██╔══██║██╔═══╝ ██╔══╝  ╚══════╝╚════██║██║     ██╔══██║██║╚██╗██║
███████║╚██████╗██║  ██║██║     ███████╗        ███████║╚██████╗██║  ██║██║ ╚████║
╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝     ╚══════╝        ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝

[*] A Python Port Scanner Using Scapy and Nmap

[*] v1.0 
[*] by csforza
"""

    print(colored(title, 'green'))


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", dest="ip", help="Target ip(s) to scan")
    parser.add_argument("-p", "--ports", dest="ports", help="Port range to scan.")
    # action=store_true -> if no value is necessary
    parser.add_argument("-q", "--top-1000", dest="tops", help="Quick top 1000 port scan.", action='store_true')
    parser.add_argument("-c", "--confirm-scan", dest="confirm",
                        help="Run an nmap scan on specified ports to confirm results", action='store_true')

    options = parser.parse_args()

    if not options.ip:
        parser.error(colored("\n[-] Please specify the ip\n"
                             "[-] Use either '-t <IP>' to specify a single target\n"
                             "[-] Or use '-t <IP>, <IP>, ....' to specify more than one target\n",
                             "red"))

    if not options.ports and not options.tops:
        parser.error(colored("\n[-] Please specify port(s) to scan...\n"
                             "[-] Use either '-p <port> - <port>' to specify a range\n"
                             "[-] Use either '-p <port> - <port>, <port> - <port>' to specify more than one range\n"
                             "[-] Use '-p <port>' or '-p <port>,<port>....' to specify specific port(s)\n"
                             "[-] Use '-p all' to specify all ports\n"
                             "[-] Use '-q' or '--top-1000' to scan the nmap top 1000 ports\n",
                             "red"))

    new_ports, new_ips = [], []

    # setup the ports so that they are returned to main() as a clean list like [1,2,3....]
    if options.ports:
        if options.ports == "all":
            options.ports = "1-65535"
        new_ports = list_ports(options.ports)

    # just in case any ports are not int's or are negative
    for i in new_ports:
        try:
            int(i)
        except ValueError:
            parser.error(colored("\n[-] Please specify port(s) to scan...\n"
                                 "[-] Use either '-p <port> - <port>' to specify a range\n"
                                 "[-] Use either '-p <port> - <port>, <port> - <port>' to specify more than one range\n"
                                 "[-] Use '-p <port>' or '-p <port>,<port>....' to specify specific port(s)\n"
                                 "[-] Use '-p all' to specify all ports\n"
                                 "[-] Use '-q' or '--top-1000' to scan the nmap top 1000 ports\n",
                                 "red"))
        if int(i) > 65535 or int(i) <= 0:
            parser.error(colored('[-] Please specify range between 1-65535', 'red'))

    # only doing comma-separated ip's input for now
    # put them all into a list
    if options.ip:
        if "," in options.ip:
            new_ips = list_ips(options.ip)
        else:
            new_ips = [options.ip]

    return new_ips, new_ports, options.tops, options.confirm


# so far, only doing comma-separated ip's
def list_ips(ips):
    if "," in ips:
        split_ips = ips.split(",")
    return split_ips


# takes the -p input and returns a list of comma-separated type int ports
# for each port within the user-specified range
def list_ports(p):
    if ',' in p:
        split_ports = p.split(',')
        new_ports = []
        # for each port, turn it into an int, and add to the ports list (new_ports)
        for i in split_ports:
            # in case user input looks something like: -p 1,2,3,10-20
            # separate those values out and add to list
            if '-' in i:
                ports_to_add = [x for x in range(int(i.split('-')[0]), int(i.split('-')[1]) + 1)]
                new_ports = new_ports + ports_to_add
            else:
                ports_to_add = [int(i)]
                new_ports = new_ports + ports_to_add
        return new_ports
    # if only a range is specified (ex. -p 100-1000)
    elif '-' in p:
        new_ports = [x for x in range(int(p.split('-')[0]), int(p.split('-')[1]) + 1)]
        return new_ports
    # if one port given
    else:
        new_ports = [int(p)]
        return new_ports


# this scans an ip and a port to see if the port is open on the ip
def scan(ip, port):
    src_port = random.randint(1025, 65534)
    # so we use sr1, looking for a single response, with the S (syn) flag to initiate the connection
    res = sr1(IP(dst=ip) / TCP(flags='S', sport=src_port, dport=port), timeout=.4, verbose=0)

    # do nothing if no response received
    # necessary, otherwise an error prints and stops the program
    if res is None:
        pass

    # if we receive a response...
    elif res.haslayer(TCP):
        # 18 == open
        if res.getlayer(TCP.flags == 18):  # or 0x12 instead of 18
            # terminates the connection and makes the scan more stealthy by using the R (rst) flag
            send_rst = sr1(
                IP(dst=ip) / TCP(sport=src_port, dport=port, flags='R'),
                timeout=1,
                verbose=0,
            )
            # hacky way to make sure we output ports as open if we get a syn and ack (SA), not rst and ack (RA)
            # some ips will give us RA's and will report them as open, despite not being truly open, so we check flags
            # normally closed will return us nothing...test in scapy shell to see...
            flags = {
                'F': 'FIN',
                'S': 'SYN',
                'R': 'RST',
                'P': 'PSH',
                'A': 'ACK',
                'U': 'URG',
                'E': 'ECE',
                'C': 'CWR',
            }
            s = [flags[x] for x in res.sprintf('%TCP.flags%')]
            if 'SYN' in s and 'ACK' in s:
                print(colored(f'[+] {ip}:{port} is open.', 'yellow'))
                return str(port)

    else:
        return None


# runs the full scan for the specified ip using multi-threading
def ip_scan(ip, ports, quick, open_ports=None):
    if open_ports is None:
        open_ports = []

    # in order that the referenced list of ports from main() do not get
    # changed when calling input_ports again in main()
    # Because a python parameter is passed by object reference, and lists are mutable objects,
    # once you pass a list into a function and change it, the original one would be changed too.
    ports = ports.copy()

    # begin the threading
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        # no need to scan ports already scanned
        if quick:
            for j in TOP_PORTS:
                if j in ports:
                    ports.remove(j)

        random.shuffle(ports)
        result = [executor.submit(scan, ip, i) for i in ports]
        count = 0
        result_count = 0

        for f in concurrent.futures.as_completed(result):
            # I add this little piece so the user has an idea of how far through the scanning has been performed
            count += 1
            if count % 10000 == 0:
                print(colored(f"===> Scanned {round(((count / len(ports)) * 100), 2)}% ports so far for {ip}.",
                              "yellow"))

            if f.result():
                open_ports.append(f.result())
                result_count += 1

        # if no results in the full/desired scan -> let user know
        if result_count == 0:
            print(colored("[-] No extra ports found in full scan.", "red"))

        # print out [ports]
        my_str = ','.join(open_ports)
        print(colored(f'\n[*] Open ports for {ip}: [{my_str}]\n\n', 'blue'))

    return open_ports


# the function name should explain what this does
def top_1000_port_scan(ip, full=True):
    open_ports = []
    result_count = 0
    random.shuffle(TOP_PORTS)

    print(colored(f"[*] Now performing a quick scan of top 1000 ports for: {ip}\n", "green"))

    # a cool way to do threading if you want to input different times for each thread
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        results = [executor.submit(scan, ip, i) for i in TOP_PORTS]

        for f in concurrent.futures.as_completed(results):
            if f.result():
                open_ports.append(f.result())
                result_count += 1

        # if no results in the scan -> let user know
        if result_count == 0:
            print(colored(f"[-] No ports found in full scan of {ip}.", "red"))

        # if only a quick scan with no ports specified - return [ports]
        if not full:
            open_str = ','.join(open_ports)
            print(colored(f'\n[*] Open ports for {ip}: [{open_str}]', 'blue'))

    return open_ports


# will run a nmap scan on the desired ports afterwards for more complete data output
# if quick only -> more detailed scan of found ports and nmap -T4 on top 1000 ports if option specified
def nmap(ip, quick, open_ports_to_scan=None, options_ports=None, confirm=None):
    # if there are ports to scan, run the nmap scan
    # else, do nothing, because nmap will error out with no ports listed
    if open_ports_to_scan:
        my_str = ','.join(open_ports_to_scan)
        print(colored(f'[+] Now running "nmap -sC -sV -oA" on the open ports for {ip}...\n', 'cyan'))

        cmd = f'/usr/bin/nmap -sC -sV -oA {ip} -p {my_str} {ip} -Pn'
        # The module shlex will take a string containing the whole shell command and split it up
        # exactly how Popen and check_output expect it
        args = shlex.split(cmd)
        # subprocess.check_output by default receives bytes, use text=True to convert
        print(subprocess.check_output(args, text=True))

        print(colored(f'[+] Nmap scan on {ip} is now finished. See {ip}.nmap for output.\n\n', 'cyan'))
    else:
        print(colored(f'[-] Since no open ports were found, no Nmap scan will be conducted on {ip}.\n\n', 'red'))

    # check to make sure the program got all the ports quickly if -c -> set --top-ports 1000
    # run them all with '-Pn' in case you get ping probes blocked
    if confirm:
        # if any ports were specified in the options then run with those ports, otherwise just run on top-1000
        if options_ports:
            # if -q and ports != all
            if quick and len(options_ports) != 65535:
                print(colored(f'[+] Now running a quick -T4 nmap scan on top 1000 plus specified ports on {ip} '
                              f'to confirm results.\n', 'cyan'))
                new_str = ",".join(str(i) for i in options_ports)
                # too lazy to fix potential duplicates...give me some coffee :)
                cmd = f'/usr/bin/nmap -T4 -p {TOP_STR},{new_str} {ip} -Pn'
                args = shlex.split(cmd)
                print(subprocess.check_output(args, text=True))
            else:
                # if -p = all
                if len(options_ports) == 65535:
                    print(colored(
                        f'[+] Now running a quick -T4 nmap scan on all ports on {ip} to confirm results.\n',
                        'cyan'))
                    cmd = f'/usr/bin/nmap -T4 -p- {ip} -Pn'
                    args = shlex.split(cmd)
                    print(subprocess.check_output(args, text=True))
                # if no -q and -p != all
                else:
                    new_str = ",".join(str(i) for i in options_ports)
                    print(colored(
                        f'[+] Now running a quick -T4 nmap scan on specified ports on {ip} to confirm results.\n',
                        'cyan'))
                    cmd = f'/usr/bin/nmap -T4 -p {new_str} {ip} -Pn'
                    args = shlex.split(cmd)
                    print(subprocess.check_output(args, text=True))
        else:
            print(colored(f'[+] Now running a quick -T4 nmap scan on top 1000 ports on {ip} to confirm results.\n',
                          'cyan'))
            cmd = f'/usr/bin/nmap -T4 {ip} -Pn'
            args = shlex.split(cmd)
            print(subprocess.check_output(args, text=True))

    return


def main():
    title()
    if len(sys.argv) < 2:
        print(f"[*] Usage: python Scape-Scan.py -t <TARGET IP> -p <PORT RANGE> [-q] [-c]")
        sys.exit(1)
    inputs = get_args()
    quick_scan = False
    input_ips, input_ports, confirm_scan = inputs[0], inputs[1], inputs[3]

    # by 'full scan', I mean scan with -p specified, regardless of the number of ports
    top_scan_ports, full_scan_ports = [], []

    # quick top 1000 port scan for each ip, so it can be viewed and begun to enumerate deeper if -q specified
    # each ip will have it own open ports stored in an element in top_scan_ports
    if inputs[2]:
        quick_scan = True
        for i in input_ips:
            if not input_ports:
                top_scan_ports.append(top_1000_port_scan(i, False))
            else:
                top_scan_ports.append(top_1000_port_scan(i))
            print("\n")
            # I find the scans are a little more accurate when I add this between ip's
            time.sleep(5)

    # if user does not specify a port range and wants only a quick scan, then nmap the results
    # otherwise scan the desired ports
    if quick_scan and not input_ports:
        for i in range(len(input_ips)):
            nmap(input_ips[i], quick_scan, top_scan_ports[i], full_scan_ports, confirm_scan)
    else:
        # for every ip, a separate port scan is conducted, the open ports for each ip are saved into a list
        # which will go into nmap() later
        for i in range(len(input_ips)):
            print(colored(f"[*] Performing full port scan of {input_ips[i]}\n", "green"))
            if len(top_scan_ports) > 0:
                # ip_line runs the full port scan, accepting the ip, ports, whether a quick scan has already
                # been done (boolean) and the open ports already found
                full_scan_ports.append(ip_scan(input_ips[i], input_ports, quick_scan, top_scan_ports[i]))
                time.sleep(5)
            # if no quick scan has been performed
            else:
                full_scan_ports.append(ip_scan(input_ips[i], input_ports, quick_scan))
                time.sleep(5)

        # do the nmap scans after all the ports have been scanned
        for i in range(len(input_ips)):
            nmap(input_ips[i], quick_scan, full_scan_ports[i], input_ports, confirm_scan)


if __name__ == "__main__":
    start = time.perf_counter()
    main()
    finish = time.perf_counter()
    print(f'Finished in {round(finish - start, 2)} second(s).')

# todo
# ping sweep functionality
# input nmap options
# allow <IP>-<IP> input so a user doesn't have to comma separate all possible targets to scan
