#!/usr/bin/python 

import argparse
from os.path import isfile

def do_parse(mirrorlist,num=3,Verbose=None,quite=False):
    servers =[]
    if Verbose: print(f"Reading from mirrorlist {mirrorlist}")
    with open(mirrorlist) as reader:
        f = reader.read()
        f = f.split("\n")
        for line in f:
            if("Server =" in line):
                _,u = line.split(" = ")
                servers.append(u.replace("$repo/os/$arch","$request_uri"))
                if len(servers) == num: break
    if num > len(servers):
        if not(quite): print(f"number of mirrors keep to {len(servers)} as there are only that much in the mirrorlist! {num} where requested")
        num=len(servers)
    output = "upstream mirrors {\n"
    for i in range(num):
        output += f"\tserver\t127.0.0.1:{i + 8001}"
        if i > 0: output += "\tbackup"
        output +=";\n"
    output += "}\n"
    for i in range(num):
        output += "server\n{\n\tlisten\t127.0.0.1:"
        output += f"{i + 8001};\n\tlocation / "
        output += "{\n\t\tproxy_pass\t"
        output += f"{servers[i]};\n\t"
        output += "}\n}\n"
    return output


def parse_args():
    verbose_help_text= 'more verbose output'
    quite_help_text='output less'
    mirrorlist='/etc/pacman.d/mirrorlist'
    config_file='/etc/nginx/server.conf'
    default_num=3

    parser = argparse.ArgumentParser(description='update nginx config with mirrors from mirrorlist.')
    parser.add_argument('-n','--dry-run',help="don't write config file", action='store_true')
    parser.add_argument('-i','--mirror-list',help=f"mirrorlist file to be parsed. ({mirrorlist})",nargs=1,default=[mirrorlist])
    parser.add_argument('-o','--config-file',help=f"config snip in to write to ({config_file})",nargs=1,default=[config_file])
    parser.add_argument('-N','--mirrors',help=f"Number of mirrors to be used ({default_num})",nargs=1,default=[default_num])

    group_status = parser.add_mutually_exclusive_group()
    group_status.add_argument('-v','--verbose',help=verbose_help_text, action='count')
    group_status.add_argument('-q','--quite',help=quite_help_text, action='store_true')

    args = parser.parse_args()

    if args.verbose:
        print(f"""running script with the following parameters:
   dry-run: {args.dry_run}
Mirrorlist: {args.mirror_list[0]}
Configfile: {args.config_file[0]}
Number of Mirrors: {args.mirrors[0]}""")

    return args

def main():
    args = parse_args()
    if isfile(args.mirror_list[0]):
        result = do_parse(args.mirror_list[0],int(args.mirrors[0]),args.verbose,args.quite)
        if args.dry_run:
            if not(args.quite):
                print(result)
        else:
            if args.verbose: print(f"writing to configfile: {args.config_file[0]}")
            with open(args.config_file[0],"w") as writer:
                writer.write(result)            
    else:
        print(f"mirrorlist: {args.mirror_list[0]} does nit exist!")

if __name__ == "__main__": main()
