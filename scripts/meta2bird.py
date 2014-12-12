#!/usr/bin/env python2.7

import yaml
import string
import logging
import argparse


TEMPLATE_NAME = 'template'
IP_VERSION = 'ipv4'


def get_meta_dict(filename):
    with open(filename) as f:
        try:
            return yaml.load(f)
        except:
            logging.warning("Can't read file {}".format(filename))
            return {}


def get_peer_entries(meta_dict, ip_version='ipv4'):
    if 'bgp' in meta_dict.keys():
        for peerid in meta_dict['bgp'].keys():
            try:
                asn = meta_dict['asn']
                peer_entry = {
                    'peerid':   peerid,
                    'ip': meta_dict['bgp'][peerid][ip_version],
                    'asn':      asn,
                    }
                yield peer_entry
            except:
                logging.warning("Can't add peer {}".format(peerid))


def render_template(peer_entry, template=TEMPLATE_NAME):
    with open(template) as tmpl_f:
        tmpl = string.Template(tmpl_f.read())
        return tmpl.substitute(peer_entry)


def get_files(path):
    from os import listdir
    from os.path import isfile, join
    return (join(path, f) for f in listdir(path) if isfile(join(path, f)))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("peer_directory", help="Directory with peer files")
    parser.add_argument(
        "-i",
        "--ipv",
        help="Set ip version 4 or 6",
        # action="store_true",
        default=4,
        type=int,
        choices=[4, 6])
    parser.add_argument(
        "-j",
        "--json",
        help="Output a json list with a dictionary for each entry",
        action="store_true")

    args = parser.parse_args()
    ip_version = "ipv" + str(args.ipv)

    peer_files = get_files(args.peer_directory)
    peer_entries = (gen for f in peer_files
                    for gen in (get_peer_entries(get_meta_dict(f), ip_version)))

    if args.json is True:
        import json
        print(json.dumps(list(peer_entries)))
    else:
        for config in peer_entries:
            print(render_template(config))


if __name__ == '__main__':
    main()
