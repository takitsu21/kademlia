import argparse
import logging
import asyncio
from kademlia.network import Server

handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
log = logging.getLogger('kademlia')
log.addHandler(handler)
log.setLevel(logging.DEBUG)

server = Server()
loop = asyncio.get_event_loop()


def parse_arguments():
    parser = argparse.ArgumentParser()

    # Optional arguments
    parser.add_argument("-i", "--ip", help="IP address of existing node", type=str, default=None)
    parser.add_argument("-p", "--port", help="port number of existing node", type=int, default=None)
    parser.add_argument("-hp", "--host-port", help="port number of existing node", type=int, default=8468)
    return parser.parse_args()


def connect_to_bootstrap_node(args):
    loop.run_until_complete(server.listen(args.port))
    bootstrap_node = (args.ip, args.host_port)
    loop.run_until_complete(server.bootstrap([bootstrap_node]))
    while True:
        inp = input("set/get a key: ")
        formatted_input = inp.split(" ")
        if formatted_input[0] == "set":
            loop.run_until_complete(server.set(f"{formatted_input[1]}", f"{formatted_input[2]}"))
        elif formatted_input[0] == "get":
            res = loop.run_until_complete(server.get(f"{formatted_input[1]}"))
            print(f"Get result: {formatted_input[1]} = {res}")

def create_bootstrap_node(args):
    loop.set_debug(True)

    loop.run_until_complete(server.listen(args.host_port))

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.stop()
        loop.close()


def main():
    args = parse_arguments()
    if args.ip and args.port and args.host_port:
        connect_to_bootstrap_node(args)
    else:
        create_bootstrap_node(args)


if __name__ == "__main__":
    main()
