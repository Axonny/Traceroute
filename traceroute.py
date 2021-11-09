import time
from scapy.all import *


class Traceroute:
    def __init__(self, hostname: str, sequence=0, queries=3, sendwait=0, wait=1000, max_hops=30, size=40,
                 ipv6=False, isTCP=False, port=0):
        self.hostname = hostname
        self.sequence = sequence
        self.queries = queries
        self.sendwait = sendwait
        self.wait = wait
        self.max_hops = max_hops
        self.size = size
        self.ipv6 = ipv6
        self.isTCP = isTCP
        self.port = port

    def traceroute(self) -> None:
        for i in range(1, self.max_hops + 1):
            pkt = self._create_packet(i)
            replies = self._send_packet(pkt)
            if len(replies) == 0:
                self._formatted_output(i, "**.***.***.***", "*")
                continue

            reply = replies[0]
            if (TCP in reply and reply['TCP'].flags.A) or reply.type == 0:
                self._formatted_output(i, self._join_src(replies), self._get_times(replies))
                print("Done!")
                break
            else:
                self._formatted_output(i, self._join_src(replies), self._get_times(replies))

    def _send_packet(self, pkt: packet) -> list[packet]:
        answers = []
        for _ in range(self.queries):
            reply = sr1(pkt, verbose=0, timeout=self.wait / 1000, inter=self.sendwait / 1000)
            if reply is not None:
                reply.reply_time = self._get_time(reply)
                answers.append(reply)
        return answers

    def _create_packet(self, cur_ttl: int) -> packet:
        ip = IPv6(dst=self.hostname, hlim=cur_ttl) if self.ipv6 else IP(dst=self.hostname, ttl=cur_ttl)
        if self.isTCP:
            protocol = TCP(dport=self.port, flags='S')
        else:
            protocol = ICMPv6EchoRequest(seq=self.sequence) if self.ipv6 else ICMP(seq=self.sequence)
        pkt = ip / protocol
        return pkt / Raw(RandString(self.size - len(pkt)))

    @staticmethod
    def _get_time(reply: packet) -> int:
        seconds = time.time() - reply.time
        ms = seconds * 1000
        return ms

    @staticmethod
    def _formatted_output(n: int, ip: str, ms: int) -> None:
        print(f'{n:<3}', f'{ip:<15}', ms)

    @staticmethod
    def _join_src(replies=list[packet]) -> str:
        return ' '.join(set([reply.src for reply in replies]))

    @staticmethod
    def _get_times(replies=list[packet]) -> float:
        times = [reply.reply_time for reply in replies]
        return '  '.join([f'{round(t, 3):<5} ms' for t in times])
