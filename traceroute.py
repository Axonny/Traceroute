import time
from scapy.all import IP, ICMP, Raw, RandString, sr1, packet


class Traceroute:
    def __init__(self, hostname: str, sequence=0, queries=3, sendwait=0, wait=1000, max_hops=30, size=40):
        self.hostname = hostname
        self.sequence = sequence
        self.queries = queries
        self.sendwait = sendwait
        self.wait = wait
        self.max_hops = max_hops
        self.size = size

    def traceroute(self) -> None:
        for i in range(1, self.max_hops + 1):
            pkt = self._create_packet(i)
            reply = sr1(pkt, verbose=0, timeout=self.wait / 1000, retry=self.queries, inter=self.sendwait / 1000)
            if reply is None:
                self._formatted_output(i, "**.***.***.***", "*")
            elif reply.type == 0:
                self._formatted_output(i, reply.src, self._get_time(reply))
                print("Done!")
                break
            else:
                self._formatted_output(i, reply.src, self._get_time(reply))

    def _create_packet(self, cur_ttl: int) -> packet:
        pkt = IP(dst=self.hostname, ttl=cur_ttl) / ICMP(seq=self.sequence)
        return pkt / Raw(RandString(self.size - len(pkt)))

    @staticmethod
    def _get_time(reply: packet) -> int:
        seconds = time.time() - reply.time
        ms = round(seconds * 1000)
        return ms

    @staticmethod
    def _formatted_output(n: int, ip: str, ms: int) -> None:
        print(f'{n:<3}', f'{ip:<15}', f'{ms} ms')
