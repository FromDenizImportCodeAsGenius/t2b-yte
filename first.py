from typing import Any
import os
import dill
import types
import decimal
import fractions
class bit_convert:

    def code_explain(self):
        """
        The result will have form

        1(a byte of 11111111) - data bits(3999200 bytes) - type bits(800 bytes)

        data bytes for

        int:
        stored directly

        float:
        stored left shift 64

        bool/none/ellipis/notimp:
        bools are their value
        none is 0
        ellipsis is 0
        not imp is 0

        bytes/bytearray:
        stored directly

        str:
        stored with utf-32 encoding

        memoryview:
        stored with .tobytes()

        list/tuple/filter/map/iter/generator:
        stored as len and then index - len_data_and_type - data - type for each element

        set/frozenset:
        stored as len and then len_data_and_type - data - type for each element

        range:
        three stored elements(40 bytes each)
        start - stop - step

        zip: 
        len_of_zipped - zipped

        dict:
        len and then tuple_of_keys - tuple_of_values

        enumerate: 
        starting_index - len - data

        complex:
        lenreal - real - lenimag - imag

        file:
        mode - lenfilepath - file_path

        code/function/class:
        store with bytearray by dill.dumps

        module:
        store with bytearray by dill.dump_module

        decimal.Decimal:
        store by storing the simple continued fraction by len - data for each number


        """
    def convert(self,data : Any ,call=False):
        data = data
        name = type(data).__qualname__
        array = bytearray
        bitname = array(bytes(name.ljust(400).encode("utf-32")))
        bitdata = array()
        dataclass = type(data)
        temp = bin(0)
        match dataclass:

            case "int":
                temp = data.to_bytes()

            case "float":
                temp = (data << 64).to_bytes()

            case "str":
                temp = data.encode("utf-16")

            case str(types.NoneType)|str(types.EllipsisType)|str(types.NotImplementedType):
                temp = bytes()

            case "bool":
                temp = int(data).to_bytes()

            case "bytearray"|"bytes":
                temp = data

            case "memoryview":
                temp = data.tobytes()

            case "list"|"tuple":
                asd = ""
                asd += bin(str(len(data)))[2:].ljust(80) # Binary, Padding for length of container

                for ind,elem in enumerate(data):
                    asd += bin(ind)[2:].ljust(80) # Binary, Padding for index

                    lend = "".join(f"{b:08b}" for b in self.convert(elem,True)) # type: ignore # Encoded Element
                    asd += bin(str(len(lend)))[2:].ljust(80) # Binary, Padding for length of element
                    asd += lend # Encoded Element
                asdd = int(asd,2)
                temp = asdd.to_bytes((len(asd)+7)//2)

            case "filter"|"map"|"iter"|str(types.GeneratorType):
                data = list(data)
                asd = ""
                asd += bin(str(len(data)))[2:].ljust(80) # Binary, Padding for length of container

                for ind,elem in enumerate(data):
                    asd += bin(str(ind))[2:].ljust(80) # Binary, Padding for index

                    lend = "".join(f"{b:08b}" for b in self.convert(elem,True)) # Encoded Element
                    asd += bin(str(len(lend)))[2:].ljust(80) # Binary, Padding for length of element
                    asd += lend # Encoded Element

                asdd = int(asd,2)
                temp = asdd.to_bytes((len(asd)+7)//2)


            case "set"|"frozenset":
                asd = ""
                asd += bin(len(data))[2:].ljust(80) # Binary, Padding for length of container

                for elem in data:

                    lend = "".join(f"{b:08b}" for b in self.convert(elem,True)) # type: ignore # Encoded Element
                    asd += bin(len(lend))[2:].ljust(80) # Binary, Padding for length of element
                    asd += lend # Encoded Element
                asdd = int(asd,2)
                temp = asdd.to_bytes((len(asd)+7)//2)
            case "range":
                asd = ""
                asd += bin(str(len(data)))[2:].ljust(80) # Binary, Padding for length of container

                for elem in [data.start, data.stop, data.step]:
                    asd += bin(len(data))[2:].ljust(320) # Encoded Element
                
                asdd = int(asd,2)
                temp = asdd.to_bytes((len(asd)+7)//2)
            
            case "dict":
                lnn = bin(str(len(data)))[2:].ljust(80)
                key = tuple(data.keys())
                val = tuple(data.values())

                asd = ""

                for ind,elem in enumerate(key):
                    asd += bin(str(ind))[2:].ljust(80) # Binary, Padding for index

                    lend = "".join(f"{b:08b}" for b in self.convert(elem,True)) # Encoded Element
                    asd += bin(str(len(lend)))[2:].ljust(80) # Binary, Padding for length of element
                    asd += lend # Encoded Element

                asdd = ""

                for ind,elem in enumerate(val):
                    asdd += bin(str(ind))[2:].ljust(80) # Binary, Padding for index

                    lend = "".join(f"{b:08b}" for b in self.convert(elem,True)) # Encoded Element
                    asdd += bin(str(len(lend)))[2:].ljust(80) # Binary, Padding for length of element
                    asdd += lend # Encoded Element

                qwe = lnn + asd + asdd
                asdd = int(qwe,2)
                temp = asdd.to_bytes((len(qwe)+7)//2)

            case "complex":
                r = (data.real << 64).to_bytes()
                i = (data.imag << 64).to_bytes()
                rl = bytes([len(r)])
                il = bytes([len(i)])
                temp = rl + r + il + i

            case str(types.CodeType)|str(types.FunctionType)|str(types.BuiltinFunctionType)|str(types.MethodType)|str(types.BuiltinMethodType)|"type":
                temp = dill.dumps(data)

            case str(types.ModuleType):
                temp = dill.dump_module(data)

            case "zip":
                data = zip(data)
                lll = bin(len(list(data)[0]))[2:].ljust(40)
                asd = lll
                for z in data:
                    for elem in z:
                        lend = "".join(f"{b:08b}" for b in self.convert(elem,True)) # type: ignore # Encoded Element
                        asd += bin(len(lend))[2:].ljust(80) # Binary, Padding for length of element
                        asd += lend # Encoded Element
                asdd = int(asd,2)
                temp = asdd.to_bytes((len(asd)+7)//2)
            case "enumerate":
                _, (it, st) = data.__reduce__()
                asd = bin(st)[2:].ljust(40)
                asd += bin(len(data))[2:].ljust(80) # Binary, Padding for length of container

                for elem in data:
                    lend = "".join(f"{b:08b}" for b in self.convert(elem,True)) # type: ignore # Encoded Element
                    asd += bin(len(lend))[2:].ljust(80) # Binary, Padding for length of element
                    asd += lend # Encoded Element
                asdd = int(asd,2)
                temp = asdd.to_bytes((len(asd)+7)//2)
            case "file":
                path = os.path.abspath(data.name) 
                temp = path.encode("utf-32")
            case str(decimal.Decimal):
                asd = ""
                left = data
                while left != 0:
                    n, d = left.as_integer_ratio()
                    whole = n // d
                    m = bin(whole)[2:]
                    p = bin(len(m))[2:].ljust(80)
                    asd += p + m
                    left = decimal.Decimal(d) / decimal.Decimal(n - (n // d) * d)
                asdd = int(asd,2)
                temp = asdd.to_bytes((len(asd)+7)//2)

            case _:
                try:
                    data = decimal.Decimal(data)
                    return self.convert(data,True)
                except:
                    try:
                        data = list(data)
                        return self.convert(data,True)
                    except:
                        temp = dill.dumps(data)


        bitdata = array(temp) #type:ignore
        start = array([255])
        fill = bytes(3999200 - len(bitdata))
        stuffing = start + fill
        bits = bitdata + bitname
        if not bool(call):
            bits = stuffing + bits
        return bits

BC = bit_convert()
