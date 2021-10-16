import random, math, threading

class qubits:
    def __init__(self, values, weights):
        self.values = values
        self.weights = weights
    
    def soft_measure(self):
        normalized_weights = []
        _max = sum(self.weights)
        if _max == 0:
            return 0
        for i in self.weights:
            normalized_weights.append(i / _max)
        
        r = random.choices(self.values, self.weights)
        return r[0]
    
    def measure(self):
        val = []
        wei = []
        v = self.soft_measure()
        for i in range(len(self.values)):
            if self.values[i] == v:
                val.append(self.values[i])
                wei.append(self.weights[i])
        self.values = val
        self.weights = wei
        return v

    def __str__(self):
        s = ""
        for i in range(len(self.values)):
            s += str(round(self.weights[i], 2)) + "|" + str(self.values[i]) + "> + "
        return s[:-3]

class processor:
    def __init__(self):
        self.source = None
        self.out = None

    def compile(self, source):
        self.source = source

    def run_threaded(self, values, constants={}):
        varlist = list(values.keys())
        size = len(list(values.values())[0].values)
        self.out = qubits([], [])
        for i in range(size):
            t = threading.Thread(target=self.__run_thread__, args=(varlist, values, constants, i,))
            t.daemon = True
            t.name = "jDev QuantaLib #" + str(i)
            t.start()
        while len(self.out.values) != size:
            print(str(len(self.out.values)) + "/" + str(size))
    
    def run(self, values, constants={}):
        varlist = list(values.keys())
        size = len(list(values.values())[0].values)
        self.out = qubits([], [])
        for i in range(size):
            vals = {}
            for k in varlist:
                vals[k] = values[k].values[i]
                vals['w' + k] = values[k].weights[i]
            v, w = self.__run_pass__(vals, constants)
            self.out.values.append(v)
            self.out.weights.append(w)

    def __run_thread__(self, varlist, values, constants, i):
        vals = {}
        for k in varlist:
            vals[k] = values[k].values[i]
            vals['w' + k] = values[k].weights[i]
        v, w = self.__run_pass__(vals, constants)
        self.out.values.append(v)
        self.out.weights.append(w)

    def __run_pass__(self, values, constants):
        source = self.source

        for x in values:
            source = x + "=" + str(values[x]) + "\n" + source
        for x in constants:
            source = x + "=" + str(constants[x]) + "\n" + source

        _locals = dict()
        exec(source, globals(), _locals)
        return _locals['v'], _locals['w']

    def measure(self):
        return self.out.measure()
    
    def get_qubits(self):
        return self.out