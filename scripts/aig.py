class Aig(object):
    def __init__(self, M, I, L, O, A):
        self._M = M
        self._I = I
        self._L = L
        self._O = O
        self._A = A
        self._Init = None

    @property
    def maxVar(self): return self._M
    @property
    def inSz(self): return self._I
    @property
    def regSz(self): return self._L
    @property
    def outSz(self): return self._O
    @property
    def gateSz(self): return self._A
    @property
    def init(self): return self._Init
    @init.setter
    def init(self, v): self._Init = v

    def __str__(self):
        return 'aag {M} {I} {L} {O} {A}'.format(M=self.maxVar,
                                                I=self.inSz,
                                                L=self.regSz,
                                                O=self.outSz,
                                                A=self.gateSz)


class ParseException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


def parse(input):
    header = next(input).split()
    header = [chunk.decode('utf-8') for chunk in header]

    if len(header) < 6:
        raise ParseException("Incorrect header" + str(header))
    if header[0] != 'aig':
        raise ParseException('Not a binary aig file: ' + str(header))

    ntk = Aig(int(header[1]),
              int(header[2]),
              int(header[3]),
              int(header[4]),
              int(header[5]))

    init = list()
    for i in range(ntk.regSz):
        reg = next(input).split()
        reg = [chunk.decode('utf-8') for chunk in reg]
        if len(reg) == 1:
            init.append(0)
        elif reg[1] == '0' or reg[1] == '1':
            init.append(int(reg[1]))
        else:
            init.append(2)
    ntk.init = init

    return ntk


def adjust_cex(in_cex, cex_aig, orig_aig, out_cex):
    out_cex.write(next(in_cex))  # result line
    out_cex.write(next(in_cex))  # property line
    out_cex.flush()

    latch_inits = next(in_cex).strip()
    assert len(latch_inits) == cex_aig.regSz

    adjust = (orig_aig.inSz < cex_aig.inSz)
    first_inputs = next(in_cex).strip()           # usual AIGER CEX layout
    has_inputs0  = (len(first_inputs) == cex_aig.inSz)

    # Extra-input bits (only if adjusting)
    extra_bits = first_inputs[orig_aig.inSz:] if (adjust and has_inputs0) else ""
    dc_iter = iter(extra_bits)

    # Rebuild initial latch vector for original design
    buf = []
    for i in range(orig_aig.regSz):
        v = orig_aig.init[i]
        if v == 2:
            # prefer extra bits if available; else pick a deterministic default
            v = int(next(dc_iter, "0"))
        buf.append(str(v))
    out_cex.write("".join(buf) + "\n")

    # Forward first inputs line (trimmed) if present
    if has_inputs0:
        out_cex.write(first_inputs[:orig_aig.inSz] + "\n")

    # Forward the rest, trimming extra inputs when needed
    for line in in_cex:
        s = line.strip()
        if s == '.':
            out_cex.write('.\n')
            break
        if adjust and len(s) == cex_aig.inSz:
            out_cex.write(s[:orig_aig.inSz] + "\n")
        else:
            out_cex.write(line)

    out_cex.flush()

if __name__ == '__main__':
    import sys
    adjust_cex(in_cex=open(sys.argv[1]), cex_aig=parse(open(sys.argv[2])),
               orig_aig=parse(open(sys.argv[3])), out_cex=sys.stdout)
