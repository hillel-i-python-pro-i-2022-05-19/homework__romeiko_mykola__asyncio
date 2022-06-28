import argparse


def get_args_from_cli():
    cli_parser = argparse.ArgumentParser()
    cli_parser.add_argument('-t',
                            '--target_file',
                            default='target_sites.txt',
                            help=r'set .txt file with target sites separated by \n (default: target_sites.txt)')
    cli_parser.add_argument('-ll',
                            '--links_limit',
                            type=int,
                            default=100,
                            help='set amount of urls to collect from the target site (default: 100)')
    cli_parser.add_argument('-d',
                            '--depth_level',
                            type=int,
                            default=2,
                            help='set depth level of crawling (default: 2)')
    cli_parser.add_argument('-c',
                            '--cores_amount',
                            type=int,
                            default=4,
                            help='set cpu cores amount (default: 4)')
    args = cli_parser.parse_args()
    return args
