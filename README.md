# InterCityVPN meta information
[![Build Status](https://travis-ci.org/freifunk/icvpn-meta.svg?branch=master)](https://travis-ci.org/freifunk/icvpn-meta)

The data in this repository can be used for automatic configuration of
routing daemons and DNS servers.  You may leave out fields that do not
apply to your community (e.g. `asn`, `domains` and `nameservers`).

Stick to one file per community. The filename must match your communityname
on the [freifunk-api](https://github.com/freifunk/api.freifunk.net).
You may add stub DNS zones (e.g. dn42, rzl, hack) by leaving out
everything but `domains` and `nameservers`.

Scripts for the automatic configuration generation and provisioning of various services (bird, bind, dnsmasq,
...) are kept in a separate repository: [icvpn-scripts](https://github.com/freifunk/icvpn-scripts)

Notes on IPv4 allocations
-------------------------

* There is only a limited amount of usuable IPv4 space available.
* 10/8 is used for connections between community networks across the ICVPN.
* Previously, people just took a /16, which means space is exhausted after 255 communites picked a network.
* Thus: think before you allocate a v4 network here: do you really *need* IPv4 connectivity between your and other Freifunk networks? If not, consider to use IPs from 172.16.0.0/12 or 198.18.0.0/15 internally and do NOT announce them to ICVPN.
* If you think you do, please be conservative; rule of thumb: Meshes might not size well beyond 2000 concurrent users, double that for decent DHCP timings => a /20 (4k IPs) per Mesh sounds reasonable. For additional systems outside the Mesh, an additional /22 (1024 IPv4 addresses) might be sufficient.
* If you use mostly routing (OLSR), things might look different, you might look into e. g. an /21 to distribute to clients and another /22 for p2p-links if needed.
* Again, please plan ahead, than take your pick. Be prepared to be questioned on why, if you took e. g. more than /18 directly. But remember as well, that renumbering IS a pain.
* If you need more than a /18 in one community or city you need a _very_ good explaination, why you do need it.
* Minimum net size is /22, round up if you need less.

Example
-------

```
  # This is your ASN.
  asn: 65052

  # A list of people to contact in case of technical emergency.
  # Automated monitoring systems might use this.
  tech-c:
    - nils@nilsschneider.net
    - mschiffer@universe-factory.net
  
  # Prefixes announced by your AS. This may be used for filtering
  # routes. Keep the prefixes a short as possible. If you're
  # assigned 10.130.0.0/20 while you're using just a subnet of it
  # (e.g. 10.130.0.0/21) you must include 10.130.0.0/20 here. The details
  # will be taken care of by the routing daemons.
  networks:
    ipv4:
      - 10.130.0.0/20
    ipv6:
      - fdef:ffc0:3dd7::/48
      - 2001:bf7:110::/44

  # A list of BGP peers in IC-VPN announcing your AS.
  bgp:
    luebeck1:
      ipv4: 10.207.0.130
      ipv6: fec0::a:cf:0:82
    luebeck2:
      ipv4: 10.207.0.131
      ipv6: fec0::a:cf:0:83

  # If you're using custom TLDs, include them here.
  # Don't forget reverse zones!
  domains:
    - ffhl
    - 7.d.d.3.0.c.f.f.f.e.d.f.ip6.arpa
    - 130.10.in-addr.arpa

  # A list of nameservers capable of resolving your domains. 
  # All nameservers must be able to handle all domains listed above!
  nameservers:
    - 10.130.10.1
    - 10.130.14.1
    - fdef:ffc0:3dd7::a01
    - fdef:ffc0:3dd7::e01

  # Delegate part of our network allocations to another community
  # this needs to be a subnet to an already allocated network in the
  # networks section.
  delegate:
    65038: # Darmstadt
      - 10.130.252.0/22
      - fdef:ffc0:3dd7:ffda::/64
```
