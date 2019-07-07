 #!/usr/bin/python 2 3 from pythonwifi.iwlibs import Wireless 4 5 frequency_channel_map = { 6 2412000000: "1", 7 2417000000: "2", 8 2422000000: "3", 9 2427000000: "4", 10 2432000000: "5", 11 2437000000: "6", 12 2442000000: "7", 13 2447000000: "8", 14 2452000000: "9", 15 2457000000: "10", 16 2462000000: "11", 17 2467000000: "12", 18 2472000000: "13", 19 2484000000: "14", 20 5180000000: "36", 21 5200000000: "40", 22 5220000000: "44", 23 5240000000: "48", 24 5260000000: "52", 25 5280000000: "56", 26 5300000000: "60", 27 5320000000: "64", 28 5500000000: "100", 29 5520000000: "104", 30 5540000000: "108", 31 5560000000: "112", 32 5580000000: "116", 33 5600000000: "120", 34 5620000000: "124", 35 5640000000: "128", 36 5660000000: "132", 37 5680000000: "136", 38 5700000000: "140", 39 5735000000: "147", 40 5755000000: "151", 41 5775000000: "155", 42 5795000000: "159",
8.4 Wiﬁ Sniffer 117
43 5815000000: "163", 44 5835000000: "167", 45 5785000000: "171" 46 } 47 48 wifi = Wireless("wlan0") 49 50 for ap in wifi.scan(): 51 print "SSID: " + ap.essid 52 print "AP: " + ap.bssid 53 print "Signal: " + str(ap.quality.getSignallevel()) 54 print "Frequency: " + str(ap.frequency.getFrequency()) 55 print "Channel: " + frequency_channel_map.get(ap.frequency.getFrequency()) 56 print "" 