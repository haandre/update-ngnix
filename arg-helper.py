import argparse

verbose_help_text= 'more verbose output'
dryrun_help_text='do nothing'
quite_help_text='output less'
mirrorlist='/etc/pacman.d/mirrorlist'
config_file='/etc/nginx/server.conf'

parser = argparse.ArgumentParser(description='update nginx config with mirrors from mirrorlist.')
parser.add_argument('-n','--dry-run',help="don't write config file", action='store_true')
parser.add_argument('-i','--mirror-list',help=f"mirrorlist file to be parsed. ({mirrorlist})",nargs=1,default=[mirrorlist])
parser.add_argument('-o','--config-file',help=f"config snip in to write to ({config_file})",nargs=1,default=[config_file])

group_status = parser.add_mutually_exclusive_group()
group_status.add_argument('-v','--verbose',help=verbose_help_text, action='count')
group_status.add_argument('-q','--quite',help=quite_help_text, action='store_true')


args = parser.parse_args()

print(args.dry_run)
print(args.mirror_list[0])
print(args.config_file[0])
print(args.verbose)