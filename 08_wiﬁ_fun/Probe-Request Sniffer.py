 #!/usr/bin/python 2 3 from datetime import datetime 4 from scapy.all import * 5 6 iface = "wlan0" 7 8 # Print ssid and source address of probe requests
8.6 Hidden SSID 119
9 def handle_packet(packet): 10 if packet.haslayer(Dot11ProbeResp): 11 print str(datetime.now()) + " " + packet[Dot11].addr2 + \ 12 " searches for " + packet.info 13 14 # Set device into monitor mode 15 os.system("iwconfig " + iface + " mode monitor") 16 17 # Start sniffing 18 print "Sniffing on interface " + iface 19 sniff(iface=iface, prn=handle_packet)