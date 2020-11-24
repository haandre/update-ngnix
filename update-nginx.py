#!/usr/bin/python 

from argparse import ArgumentParser
import logging
from os.path import isfile

def do_parse(mirrorlist,num=3):
    servers =[]
    logging.debug(f"Reading from mirrorlist {mirrorlist}")
    with open(mirrorlist) as reader:
        f = reader.read()
        f = f.split("\n")
        for line in f:
            # if("Server =" in line):
            if line.startswith("Server ="):
                _,u = line.split(" = ")
                servers.append(u.replace("$repo/os/$arch","$request_uri"))
                if len(servers) == num: break
    if num > len(servers):
        logging.warn(f"number of mirrors keep to {len(servers)} as there are only that much in the mirrorlist! {num} where requested")
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
    mirrorlist='/etc/pacman.d/mirrorlist'
    config_file='/etc/nginx/server.conf'

    parser = ArgumentParser(description='update nginx config with mirrors from mirrorlist.')
    parser.add_argument('-n','--dry-run',help="don't write config file", action='store_true')
    parser.add_argument('-i','--mirror-list',help=f"mirrorlist file to be parsed. ({mirrorlist})",nargs=1,default=[mirrorlist])
    parser.add_argument('-o','--config-file',help=f"config snip in to write to ({config_file})",nargs=1,default=[config_file])
    parser.add_argument('-N','--mirrors',help=f"Number of mirrors to be used (3) ({config_file})",nargs=1,default=[3])

    parser.add_argument("-l", "--log", dest="loglevel", choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'], help="Set the logging level")
    
    args = parser.parse_args()

    return args

def main():
    args = parse_args()
    if args.loglevel:
        logging.basicConfig(level=getattr(logging, args.loglevel))
        logging.info(f"Set loglevel to: {getattr(logging, args.loglevel)}")
 
    logging.debug("running script with the following parameters:")
    logging.debug(f"dry-run: {args.dry_run}")
    logging.debug(f"Mirrorlist: {args.mirror_list[0]}")
    logging.debug(f"Configfile: {args.config_file[0]}")
    logging.debug(f"Number of Mirrors: {args.mirrors[0]}")


    if isfile(args.mirror_list[0]):
        result = do_parse(args.mirror_list[0],int(args.mirrors[0]))
        if args.dry_run:
            logging.info(result)
        else:
            logging.info(f"writing to configfile: {args.config_file[0]}")
            with open(args.config_file[0],"w") as writer:
                writer.write(result)            
    else:
        logging.error(f"mirrorlist: {args.mirror_list[0]} does not exist!")

if __name__ == "__main__": main()
