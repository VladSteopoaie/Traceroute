import socket
import sys
import random
import requests
from loguru import logger as logging

logging.remove()
logging.add(sys.stdout, colorize=True, format="<level>{level.icon}</level> <level>{message}</level>", level="TRACE")


# logging.level(name='TRACE', icon='>', color='<magenta><bold>')
logging.level(name='INFO', icon='[~]', color='<cyan><bold>')
logging.level(name='WARNING', icon='[!]', color='<yellow><bold>')
logging.level(name='DEBUG', icon='[*]', color='<blue><bold>')
logging.level(name='ERROR', icon='[X]', color='<red><bold>')
logging.level(name='SUCCESS', icon='[#]', color='<green><bold>')

# UDP socket
udp_send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, proto=socket.IPPROTO_UDP)

# RAW socket for receiving icmp packets
icmp_recv_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)

# timeout if no packet is received
icmp_recv_socket.settimeout(1)

# this is for api lookups
fake_HTTP_header = {
                    'referer': 'https://ip-api.com/',
                    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36'
                   }

# traceroute will increase the ttl for each packet sent by one until 
# it reaches the destination or hops (limit of hops)
def traceroute(ip, port, hops):
    hop = 1

    while hop <= hops:
        time_out_limit = 3 # we try to send the packet 3 times before going to the next one
        print(hop, end=" ", flush=True)
        
        # setting the TTL in the IP header
        TTL = hop
        udp_send_sock.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, TTL)

        while time_out_limit > 0:
            # sending an UDP message to the destination
            udp_send_sock.sendto(b'sup', (ip, port))

            try:
                # we wait for a response
                _, addr = icmp_recv_socket.recvfrom(63535)
                # if a response was given we lookup the ip address in the API and get the data
                response = requests.get(f'http://ip-api.com/json/{addr[0]}', headers=fake_HTTP_header).json()
                break # exiting if a response was given
            except Exception as e:
                # if we dont receive a packet we try again
                print ("*", end=" ", flush=True)
            
            time_out_limit -= 1
            if time_out_limit == 0:
                print()


        if time_out_limit > 0:
            # printing the results
            print (addr[0], end=" ")
            if (response['status'] == 'success'):
                print(f"Country: {response['country']}", f"Region: {response['regionName']}", f"City: {response['city']}", sep=' | ')
            else:
                print(response['message'])

        if addr[0] == ip:
            logging.info('Done!')
            return

        hop += 1
        
        
if __name__ == '__main__':
    if len(sys.argv) < 2:
        logging.debug(f"Usage: {sys.argv[0]} HOST [HOPS]")
        sys.exit(0)
    
    port = random.randint(33434, 33534)
    domain = sys.argv[1]
    
    hops = 30
    if len(sys.argv) > 2:
        hops = sys.argv[2]
    
    try:
        addr = socket.gethostbyname(domain)
        logging.debug(f"The domain {domain} was resolve to address {addr}")
    except:
        logging.error(f"Failed to resolve {domain}.")
        exit()

    if len(sys.argv) == 3:
        hops = int(sys.argv[2])

    if hops <= 0:
        logging.error("The hops parameter must be a positive number!")
        exit()

    traceroute(addr, port, hops)
