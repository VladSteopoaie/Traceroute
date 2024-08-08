# Traceroute

A simple traceroute application in python.

### Installation
```sh
cd /path/to/the/desired/directory
git clone https://github.com/VladSteopoaie/Traceroute
```
### Requirements
- Python must be installed on the machine.
- Administrative privileges (the script uses raw sockets to receive ICMP packets from nodes)

```sh
cd Traceroute
pip install -r requirements.txt
```
### Usage
```sh
# run with administrative privileges
python traceroute.py <IP address / domain> [number of hops] 
```
### Example
```sh
python traceroute.py google.com
```
Output:
```
[*] The domain google.com was resolve to address 142.250.180.238
1 192.168.227.39 private range
2 * * * 
3 172.18.216.66 private range
4 172.18.215.33 private range
5 10.220.153.20 private range
6 72.14.216.212 Country: United States | Region: California | City: Mountain View
7 * * * 
8 142.251.228.26 Country: United States | Region: Maryland | City: Gaithersburg
9 142.251.65.217 Country: United States | Region: California | City: Mountain View
10 142.250.180.238 Country: Hungary | Region: Budapest | City: Budapest
[~] Done!
```
Another example:
```sh
python traceroute.py yahoo.com 7
```
Output:
```
[*] The domain yahoo.com was resolve to address 98.137.11.163
1 192.168.227.39 private range
2 * 172.18.216.67 private range
3 172.18.215.1 private range
4 10.220.187.191 private range
5 80.249.209.110 Country: The Netherlands | Region: North Holland | City: Schiphol
6 209.191.112.37 Country: United Kingdom | Region: England | City: London
7 209.191.112.53 Country: United Kingdom | Region: England | City: London
```
