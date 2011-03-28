standard_options = (
    (0, "Pad"),
    (1, "Subnet Mask"),
    (2, "Time Offset (deprecated)"),
    (3, "Router"),
    (4, "Time Server"),
    (5, "Name Server"),
    (6, "Domain Name Server"),
    (7, "Log Server"),
    (8, "Quote Server"),
    (9, "LPR Server"),
    (10, "Impress Server"),
    (11, "Resource Location Server"),
    (12, "Host Name"),
    (13, "Boot File Size"),
    (14, "Merit Dump File"),
    (15, "Domain Name"),
    (16, "Swap Server"),
    (17, "Root Path"),
    (18, "Extensions Path"),
    (19, "IP Forwarding enable/disable"),
    (20, "Non-local Source Routing enable/disable"),
    (21, "Policy Filter"),
    (22, "Maximum Datagram Reassembly Size"),
    (23, "Default IP Time-to-live"),
    (24, "Path MTU Aging Timeout"),
    (25, "Path MTU Plateau Table"),
    (26, "Interface MTU"),
    (27, "All Subnets are Local"),
    (28, "Broadcast Address"),
    (29, "Perform Mask Discovery"),
    (30, "Mask supplier"),
    (31, "Perform router discovery"),
    (32, "Router solicitation address"),
    (33, "Static routing table"),
    (34, "Trailer encapsulation"),
    (35, "ARP cache timeout"),
    (36, "Ethernet encapsulation"),
    (37, "Default TCP TTL"),
    (38, "TCP keepalive interval"),
    (39, "TCP keepalive garbage"),
    (40, "Network Information Service Domain"),
    (41, "Network Information Servers"),
    (42, "NTP servers"),
    (43, "Vendor specific information"),
    (44, "NetBIOS over TCP/IP name server"),
    (45, "NetBIOS over TCP/IP Datagram Distribution Server"),
    (46, "NetBIOS over TCP/IP Node Type"),
    (47, "NetBIOS over TCP/IP Scope"),
    (48, "X Window System Font Server"),
    (49, "X Window System Display Manager"),
    (50, "Requested IP Address"),
    (51, "IP address lease time"),
    (52, "Option overload"),
    (53, "DHCP message type"),
    (54, "Server identifier"),
    (55, "Parameter request list"),
    (56, "Message"),
    (57, "Maximum DHCP message size"),
    (58, "Renew time value"),
    (59, "Rebinding time value"),
    (60, "Class-identifier"),
    (61, "Client-identifier"),
    (62, "NetWare/IP Domain Name"),
    (63, "NetWare/IP information"),
    (64, "Network Information Service+ Domain"),
    (65, "Network Information Service+ Servers"),
    (66, "TFTP server name"),
    (67, "Bootfile name"),
    (68, "Mobile IP Home Agent"),
    (69, "Simple Mail Transport Protocol Server"),
)

a="""
    70     4+     Post Office Protocol Server.     RFC 2132
    71     4+     Network News Transport Protocol Server.     RFC 2132
    72     4+     Default World Wide Web Server.     RFC 2132
    73     4+     Default Finger Server.     RFC 2132
    74     4+     Default Internet Relay Chat Server.     RFC 2132
    75     4+     StreetTalk Server.     RFC 2132
    76     4+     StreetTalk Directory Assistance Server.     RFC 2132
    77     Variable.     User Class Information.     RFC 3004
    78     Variable.     SLP Directory Agent.     RFC 2610
    79     Variable.     SLP Service Scope.     RFC 2610
    80    0    Rapid Commit.    RFC 4039
    81    4+.    FQDN, Fully Qualified Domain Name.    RFC 4702
    82    Variable.    Relay Agent Information.    RFC 3046, RFC 5010
    83    14+    Internet Storage Name Service.    RFC 4174
    84              RFC 3679
    85    Variable.    NDS servers.    RFC 2241
    86     Variable.     NDS tree name.     RFC 2241
    87     Variable.     NDS context.     RFC 2241
    88    Variable.    BCMCS Controller Domain Name list.    RFC 4280
    89    4+    BCMCS Controller IPv4 address list.    RFC 4280
    90     Variable.     Authentication.     RFC 3118
    91    4    client-last-transaction-time.    RFC 4388
    92    4n    associated-ip.    RFC 4388
    93    Variable.    Client System Architecture Type.    RFC 4578
    94     Variable.    Client Network Interface Identifier.    RFC 4578
    95     Variable.     LDAP, Lightweight Directory Access Protocol.     RFC 3679
    97    Variable.    Client Machine Identifier.    RFC 4578
    98           Open Group's User Authentication.     RFC 2485
    99         GEOCONF_CIVIC.    RFC 4776
    100         IEEE 1003.1 TZ String.    RFC 4833
    101         Reference to the TZ Database.    RFC 4833

    112     Variable.     NetInfo Parent Server Address.     RFC 3679
    113    Variable.    NetInfo Parent Server Tag.    RFC 3679
    114    Variable.    URL.    RFC 3679
    115              RFC 3679
    116    1    Auto-Configure    RFC 2563
    117    2+    Name Service Search.    RFC 2937
    118    4    Subnet Selection.    RFC 3011
    119    variable    DNS domain search list.    RFC 3397
    120    variable    SIP Servers DHCP Option.    RFC 3361
    121    5+    Classless Static Route Option.    RFC 3442
    122    variable    CCC, CableLabs Client Configuration.    RFC 3495, RFC 3594, RFC 3634
    123    16    GeoConf.    RFC 3825
    124         Vendor-Identifying Vendor Class.    RFC 3925
    125         Vendor-Identifying Vendor-Specific.    RFC 3925
    126              RFC 3679
    127              RFC 3679
    128         TFPT Server IP address.    RFC 4578
    129         Call Server IP address.    RFC 4578
    130         Discrimination string.    RFC 4578
    131         Remote statistics server IP address.    RFC 4578
    132         802.1P VLAN ID.    RFC 4578
    133         802.1Q L2 Priority.    RFC 4578
    134         Diffserv Code Point.    RFC 4578
    135         HTTP Proxy for phone-specific applications.    RFC 4578
    136    4+    PANA Authentication Agent.    RFC 5192
    137    variable    LoST Server.    RFC 5223
    138         CAPWAP Access Controller addresses.    RFC 5417
    139         OPTION-IPv4_Address-MoS.    RFC 5678
    140         OPTION-IPv4_FQDN-MoS.    RFC 5678
    141    2+    SIP UA Configuration Service Domains.    RFC 6011
    142         OPTION-IPv4_Address-ANDSF.     
    143         OPTION-IPv6_Address-ANDSF.     
    150         TFTP server address.    RFC 5859
    150         Etherboot.

    175         Etherboot.     
    176         IP Telephone.     
    177         Etherboot.
    PacketCable and CableHome.     

    208         pxelinux.magic (string) = F1:00:74:7E (241.0.116.126).    RFC 5071
    209         pxelinux.configfile (text).    RFC 5071
    210         pxelinux.pathprefix (text).    RFC 5071
    211         pxelinux.reboottime (unsigned integer 32 bits).    RFC 5071
    212    18+    OPTION_6RD.    RFC 5969
    213         OPTION_V4_ACCESS_DOMAIN.    RFC 5986
    220         Subnet Allocation.     
    221         Virtual Subnet Selection.     

                )"""