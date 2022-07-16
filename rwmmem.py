from struct import unpack, pack
from tarfile import LENGTH_NAME
from win32con import PROCESS_VM_READ, PROCESS_QUERY_INFORMATION
from win32api import OpenProcess, CloseHandle
from win32process import EnumProcesses, GetModuleFileNameEx, EnumProcessModules
from ctypes import byref, sizeof, c_uint, windll
from ReadWriteMemory import ReadWriteMemory
from pymem import Pymem
import pymem
import keystone
x86 = keystone.Ks(keystone.KS_ARCH_X86, keystone.KS_MODE_32)

def asm_to_bytes(asm):
    final = b''
    for i in x86.asm(asm)[0]:
        final += i.to_bytes(1, 'little')
    return final

def Get_Process(process_name):
    global processt
    global mem
    mem = Pymem(process_name)
    rwm = ReadWriteMemory()
    processt = rwm.get_process_by_name(process_name)
    processt.open()
    p_id, base_address = get_process_by_name(process_name)
    return mem.process_handle, base_address, mem


def Find_Pointer(base_address, address, offsets):
    pointer = processt.get_pointer(base_address + address, offsets)
    return pointer

def Read_Int(address) -> int:
    val = processt.read(address)
    return val

def Read_Float(address) -> float:
    val = mem.read_float(address)
    return val

def Read_String(address) -> str:
    val = mem.read_string(address)
    return val

def Read_Bool(address) -> bool:
    val = mem.read_bool(address)
    return val
    
def Read_Double(address):
    val = mem.read_double(address)
    return val

def Read_Bytes(address, length):
    val = mem.read_bytes(address, length)
    return val

def Write_Bytes(address, val, length):
    mem.write_bytes(address, val, length)
    



def read_process_memory(p_id, address, offsets=[]):
    h_process = windll.kernel32.OpenProcess(PROCESS_VM_READ, False, p_id)
    data = c_uint(0)
    bytesRead = c_uint(0)
    current_address = address

    if offsets:
        offsets.append(None)
        for offset in offsets:
            windll.kernel32.ReadProcessMemory(h_process, current_address, byref(data), sizeof(data), byref(bytesRead))
            if not offset:
                return data.value
            else:
                current_address = data.value + offset
    else:
        windll.kernel32.ReadProcessMemory(h_process, current_address, byref(data), sizeof(data), byref(bytesRead))

    windll.kernel32.CloseHandle(h_process)
    return data.value

# 0 - int, 1 - float
def Write_Int(address, New_Value) -> None:
    processt.write(address, New_Value)
def Write_Float(address, New_Value) -> None:
    processt.write(address, To_Int(New_Value))

def To_Float(x) -> float:
    y = unpack("@f", pack("@I", x))[0]
    return y

def To_Int(x) -> int:
    y = unpack("@I", pack("@f", x))[0]
    return y


def get_process_by_name(process_name):
    process_name = process_name.lower()
    processes = EnumProcesses()
    for process_id in processes:
        if process_id == -1:
            continue
        try:
            h_process = OpenProcess(PROCESS_QUERY_INFORMATION | PROCESS_VM_READ, True, process_id)
            try:
                modules = EnumProcessModules(h_process)
                for base_address in modules:
                    name = str(GetModuleFileNameEx(h_process, base_address))
                    if name.lower().find(process_name) != -1:
                        return process_id, base_address
            finally:
                CloseHandle(h_process)
        except:
            pass

def PLAT(aob:str):
    trueB = bytearray(b'')
    aob = aob.replace(' ','')
    PLATlist = []
    for i in range(0,len(aob), 2):
        PLATlist.append(aob[i:i+2])
    for i in PLATlist:
        if i.find("?") != -1 or i.lower() == "5b" or i.lower() == "24":
           trueB.extend(b'.')
        if i.find("?") == -1 and i.lower() != "5b" and i.lower() != "24":
           trueB.extend(bytes.fromhex(i))
    return bytes(trueB)

def ScanForFunction(handle,pattern:str,isString = False,return_multiple=False):
    if isString:
        pattern = hex(pattern,True)
    pattern = PLAT(pattern)
    
    next_region = 0
    found = []
    while next_region < 0x7FFFFFFF0000:
        next_region, page_found = pymem.pattern.scan_pattern_page(handle,next_region,pattern)
        if not return_multiple and page_found:
           return page_found
        if page_found:
            found.append(page_found)
    if not return_multiple:
        return None
    return found