import tkinter as tk
import _thread
from rwmmem import *
global pid, base_address

pid, base_address, process = Get_Process("Terraria.exe")
running = True

def gui(adw,adaw):
    global window
    window = tk.Tk()
    window.title("Terraria Hax")
    global OPTIONS, varlist, pid, base_address
    OPTIONS = []
    varlist = []
    def rehook():
        global pid, base_address
        pid, base_address, process = Get_Process("Terraria.exe")
    b = tk.Button(text="Rehook Onto Terraria", command = rehook)
    b.grid()

    global new_hack
    class new_hack():
        def new_hack(self, name, hack, offsets=None):
            self.__toggle = False
            def switch():
                if not self.__toggle:
                    self.__toggle = True
                    for i in hack:
                        self.__pointer = i[0]
                        if type(i[2]) == bytes:
                            Write_Bytes(self.__pointer, i[2], len(i[2]))
                else:
                    self.__toggle = False
                    for i in hack:
                        self.__pointer = i[0]
                        if type(i[2]) == bytes:
                            Write_Bytes(self.__pointer, i[1], len(i[1]))
                    
            self.c = tk.Checkbutton(window, command=switch, text=name)
            self.c.grid()
        
        def new_var(self, name, address, offsets, datatype):
            global OPTIONS, varlist
            OPTIONS += [name]
            varlist += [[name, address, offsets, datatype]]

    set_hacks()

    def close_window():
        global running
        running = False 
    def writeval():
        a = itxt.get(1.0, "end-1c")
        for i in varlist:
            if i[0] == variable.get():
                if i[-1] == "Float":
                    pointer = Find_Pointer(base_address, i[1], i[2])
                    Write_Float(pointer, float(a))
                if i[-1] == "Byte":
                    pointer = Find_Pointer(base_address, i[1], i[2])
                    a = hex(a)
                    Write_Bytes(pointer, f'\{a}', len(a))
                if i[-1] == "Int":
                    pointer = Find_Pointer(base_address, i[1], i[2])
                    Write_Int(pointer, int(a))
    window.protocol("WM_DELETE_WINDOW", close_window)

    global variable
    variable = tk.StringVar(window)
    variable.set(OPTIONS[0]) # default value

    w = tk.OptionMenu(window, variable, *OPTIONS)
    w.grid()
    b2 = tk.Button(window, text="Set New Value", command = writeval)
    b2.grid()
    global thingyvar
    thingyvar = variable.get()
    val = 1
    global label
    label = tk.Label(window, text=f"Current {thingyvar}: {val}")
    label.grid()
    itxt = tk.Text(window, height=1, width=25)
    itxt.grid()

    window.mainloop()
    224120040
    24

def magic_mirror():
    ptr = Find_Pointer(base_address, 0x00411C54, [0x0, 0x14, 0x38, 0x24, 0x10C, 0x64, 0x6ba])
    Write_Int(ptr, 1)

HurtSym = ScanForFunction(pid,"55 8B EC 57 56 53 81 EC 6C 02 00 00 8B F1 8D BD B0 FD FF FF")
IntoMouse = ScanForFunction(pid,"55 8B EC 57 56 53 83 EC 08 89 4D F0 8B F2 8B 7D 0C 8B 0D BC")
IntoAir = ScanForFunction(pid,"33 D2 89 91 9C 00 00 00 89 91 B0 00 00 00 88 91 78 01 00 00")
FullBrightHook = ScanForFunction(pid, "55 8B EC 57 56 53 83 EC 14 33 C0 89 45 EC 89 45 F0 89 4D E8")
ResetEffect = ScanForFunction(pid, "55 8B EC 57 56 53 8B F1 80 BE 35 06 00 00 00 74 1F FF 15 14")
resethbox = ScanForFunction(pid, "56 50 8B F1 8D 46 2C DB 46 1C D9 1C 24 D9 04 24 D8 00 D9 18")
wingmove = ScanForFunction(pid, "55 8B EC 83 EC 08 8B 91 B8 02 00 00 83 FA 04 0F 85 11 01 00")
inf = ScanForFunction(pid, "55 8B EC 57 56 53 83 EC 4C 8B F1 8D 7D AC B9 11 00 00 00 33 C0 F3 AB 8B CE 89 55 A8 8B D9")
creativ = ScanForFunction(pid, "55 8B EC 57 56 83 EC 10 33 C0 89 45 F0 89 45 F4 8B F1 8B FA 80 7E 21 00")

def set_hacks():
    global window, ghost, creative, eblockplat, instresp
    #new hack layout          name            addr    off             toggled
    #new_hack().new_hack("Toggle NoClip", [[0xF04A0, b'\x55\x8B\xEC', b'\xC2\x04\x00']])
    new_hack().new_hack("Toggle Dupe When Ctrl+Click", [[IntoAir, b'\x33\xd2', b'\xc3\x90']])
    new_hack().new_hack("Toggle Dupe When Right Click", [[IntoMouse+0xd4, b'\xFF\x8A', b'\xFF\x82']])
    new_hack().new_hack("Toggle Invincibility", [[HurtSym+0x1199, b')\x82\xe4\x03\x00\x00', b'\x01\x82\xe4\x03\x00\x00']])
    new_hack().new_hack("Toggle No Knockback", [[ResetEffect+0x140, b"\x88\x96\x03\x07\x00\x00\x88\x96\xFF\x07\x00\x00", b"\xC7\x86\x03\x07\x00\x00\x01\x00\x00\x00\x90\x90"]])
    new_hack().new_hack("Toggle Infinite Minions", [[ResetEffect+0x322, b"\xC7\x86\x98\x02\x00\x00\x01\x00\x00", b"\xC7\x86\x98\x02\x00\x00\x99\x99\x09"]])
    new_hack().new_hack("Toggle Walk Through Walls", [[resethbox+0x1c, b"\x83\xC0\x2A", b"\x83\xC0\x00"]])
    new_hack().new_hack("Toggle Infinite Wings", [[wingmove+0x6c1, b"\xD9\x99\xB0\x02\x00\x00", b"\x90\x90\x90\x90\x90\x90"]])
    
    #new_hack().new_hook("Toggle Full Bright (wip)", FullBrightHook+0xFC, 
    #b"\x56\x8B\x75\x08\xC7\x06\x00\x00\x80\x3F\xC7\x46\x04\x00\x00\x80\x3F\xC7\x46\x08\x00\x00\x80\x3F\x5E\x8B\x4D\xE4\x39\x09\xE9\xEE\xBE\xB4\x1C",
    #b"\x8B\x4D\xE4\x39\x09")

    ghost = tk.IntVar()
    b = tk.Checkbutton(window, text="Enable Ghost", variable=ghost, onvalue=1, offvalue=0)
    b.grid()

    new_hack().new_hack("Toggle Creative", [[creativ+0x26, b"\x80\xb8\xbb\x06\x00\x00\03", b"\x80\xb8\xbb\x06\x00\x00\00"]])
    new_hack().new_hack("Unlock All Creative Items", [[inf+0x26, b'\x8b\x50\x08', b'\x8b\x51\x04']])
    
    instresp = tk.IntVar()
    b = tk.Checkbutton(window, text="Instant Respawn", variable=instresp, onvalue=1, offvalue=0)
    b.grid()

    b = tk.Button(window, text="Magic Mirror", command = magic_mirror)
    b.grid()

    
    # new varlayout         name      address         offsets                            datatype
    new_hack().new_var("Health", 0x00411C54, [0x0, 0x3e4], "Int")
    new_hack().new_var("Max Health", 0x00411C54, [0x0, 0x3DC], "Int")
    new_hack().new_var("Mana", 0x00411C54, [0x0, 0x3e8], "Int")
    new_hack().new_var("Max Mana", 0x00411C54, [0x0, 0x3eC], "Int")

'''
player 6ba magic mirrior command (make button style hack)
698 toggle ghost
Terraria.Main::DamageVar make ret 0008 for damage hack terraria + 2A6CC210

todo: make button style hack nvm its easy without online hack making
'''
_thread.start_new_thread(gui, (0,0))

while running: 
    global variable, varlist, label, ghost, creative, eblockplat, instresp
    try:
        for i in varlist:
            if i[0] == variable.get():
                if i[-1] == "Float":
                    pointer = Find_Pointer(base_address, i[1], i[2])
                    val = Read_Float(pointer)
                if i[-1] == "Byte":
                    pointer = Find_Pointer(base_address, i[1], i[2])
                    val = Read_Bytes(pointer)
                if i[-1] == "Int":
                    pointer = Find_Pointer(base_address, i[1], i[2])
                    val = Read_Int(pointer)
        thingyvar = variable.get()
        label.config(text=f"Current {thingyvar}: {val}", font=("calibri", 7))

        if ghost.get() == 1:
            pointer = Find_Pointer(base_address, 0x00411C54, [0x0, 0x698])
            Write_Int(pointer, 1)
        else:
            pointer = Find_Pointer(base_address, 0x00411C54, [0x0, 0x698])
            Write_Int(pointer, 0)

        if instresp.get() == 1:
            pointer = Find_Pointer(base_address, 0x00411C54, [0x0, 0x380])
            Write_Int(pointer, 0)

        '''
        script example
        if a.get() == 1:
            pointer = Find_Pointer(base_address, 0x0016C1C4, [0x144, 0x2a4, 0x4a8])
            Write_Float(pointer, 1e38)
        '''
    except:()
