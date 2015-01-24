InterCityVPN meta information
-----------------------------
.. image:: https://travis-ci.org/freifunk/icvpn-meta.svg
    :alt: Build Status
    :target: https://travis-ci.org/freifunk/icvpn-meta
    :height: 20

The data in this repository can be used for automatic configuration of
routing daemons and DNS servers.  You may leave out fields that do not
apply to your community (e.g. `domains` and `nameservers`).

One file per community. You may add stub DNS zones (e.g. dn42, rzl,
hack) by leaving out everything but `domains` and `nameservers`.

Scripts for auto-generating various config files (bird, bind, dnsmasq,
...) are kept in a separate repository:
https://github.com/freifunk/icvpn-scripts

::

  # This is your ASN.
  asn: 65052

  # A list of people to contact in case of technical emergency.
  # Automated monitoring systems might use this.
  tech-c:
    - nils@nilsschneider.net
    - mschiffer@universe-factory.net
  
  # Prefixes announced by your AS. This may be used for filtering
  # routes. Keep the prefixes a short as possible. If you're
  # assigned 10.130.0.0/16 while you're using just a subnet of it
  # (e.g. 10.130.0.0/20) you must include 10.130.0.0/16 here. The details
  # will be taken care of by the routing daemons.
  networks:
    ipv4:
      - 10.130.0.0/16
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
