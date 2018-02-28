# -*-coding: utf-8-*-
from tkinter import *
from tkinter.messagebox import showinfo, showwarning

class BalancedTernary:
    str2dig = {'1': 1, 'T': -1, '0': 0}
    dig2str = {1: '1', -1: 'T', 0: '0'}
    table = ((0, -1), (1, -1), (-1, 0), (0, 0), (1, 0), (-1, 1), (0, 1))
    
    def __init__(self, inp):
        if isinstance(inp, str):
            self.digits = [BalancedTernary.str2dig[c] for c in reversed(inp)]
        elif isinstance(inp, list):
            self.digits = list(inp)

    def to_string(self):
        return "".join(BalancedTernary.dig2str[d] for d in reversed(self.digits))

    def to_int(self):
        return reduce(lambda y,x: x + 3 * y, reversed(self.digits), 0)

    @staticmethod
    def _neg(digs):
        return [-d for d in digs]
    
    def __neg__(self):
        return BalancedTernary(BalancedTernary._neg(self.digits))

    @staticmethod
    def _add(a, b, c=0):
        """Check empty"""
        if not (a and b):
            if c == 0:
                return a or b
            else:
                return BalancedTernary._add([c], a or b)
        else:
            (d, c) = BalancedTernary.table[3 + (a[0] if a else 0) + (b[0] if b else 0) + c]
            res = BalancedTernary._add(a[1:], b[1:], c)
            """Trim leading zeros"""
            return [d]+res
    
    def __add__(self, b):
        return BalancedTernary(BalancedTernary._add(self.digits, b.digits))
    
    def __sub__(self, b):
        return self + (-b)
        
class CalcBalancedTernary:
    def entry_text(self, text):
        self.text_field.configure(state='normal')
        self.my_text = self.text_field.get()
        if text in '+-':
            try:
                if self.my_text[len(self.my_text) - 1] in '+-':
                    self.my_text = self.my_text[:-1]
            except:
                pass
            self.my_text += text
        else:
            if text == '0' and self.my_text == '0':
                self.text_field.configure(state='disabled')
                return
            self.my_text += text
        self.text_field.delete(0, END)
        self.text_field.insert(END, self.my_text)
        self.text_field.configure(state='disabled')


    """v1"""
    @staticmethod
    def rule(x, y):
        if x=='0' and y=='0': return '0'
        if (x=='1' and y=='0') or (x=='0' and y=='1'): return '1'
        if (x=='T' and y=='0') or (x=='0' and y=='T'): return 'T'
        if (x=='1' and y=='T') or (x=='T' and y=='1'): return '0'
        if (x=='1' and y=='1'): return '1T'
        if (x=='T' and y=='T'): return 'T1'        
    @staticmethod
    def add(a, b):
        dot_a = a.index('.')
        dot_b = b.index('.')
        a = '0' * (20 - dot_a) + a
        a = a + '0' * (40 - len(a))
        b = '0' * (20 - dot_b) + b
        b = b + '0' * (40 - len(b))
        aa = [x for x in a]
        aa.reverse()
        bb = [x for x in b]
        bb.reverse()
        cc = []
        temp = '0'
        for i in range(len(aa)):
            if aa[i] == '.':
                cc.append('.')
            else:
                temp1 = rule(aa[i], bb[i])
                if temp1 == '0':
                    cc.append(temp)
                    temp = '0'
                elif temp1 == '1':
                    if temp == '0': 
                        cc.append('1')
                        temp = '0'
                    elif temp == '1': 
                        cc.append('T')
                        temp = '1'
                    elif temp == 'T':
                        cc.append('0')
                        temp = '0'
                elif temp1 == 'T':
                    if temp == '0': 
                        cc.append('T')
                        temp = '0'
                    elif temp == '1': 
                        cc.append('0')
                        temp = '0'
                    elif temp == 'T':
                        cc.append('1')
                        temp = 'T'
                elif temp1 == '1T':
                    if temp == '0': 
                        cc.append('T')
                        temp = '1'
                    elif temp == '1': 
                        cc.append('0')
                        temp = '1'
                    elif temp == 'T':
                        cc.append('1')
                        temp = '0'
                elif temp1 == 'T1':
                    if temp == '0': 
                        cc.append('1')
                        temp = 'T'
                    elif temp == '1': 
                        cc.append('T')
                        temp = '0'
                    elif temp == 'T':
                        cc.append('0')
                        temp = 'T'

        cc.reverse()
        c = ''.join(cc)
        c = c.lstrip('0')
        c = c.rstrip('0')
        return c

    """v2"""
    @staticmethod
    def operator(a, b, sign):
        """Standardize"""
        fixed_position = 20
        fixed_length = 40
        dot_a = a.index('.')
        dot_b = b.index('.')
        a = '0' * (fixed_position - dot_a) + a
        a = a + '0' * (fixed_length - len(a))
        a = a[:fixed_position] + a[fixed_position + 1:]
        b = '0' * (fixed_position - dot_b) + b
        b = b + '0' * (fixed_length - len(b))
        b = b[:fixed_position] + b[fixed_position + 1:]
        
        """Operate"""
        aa = BalancedTernary(a)
        bb = BalancedTernary(b)
        if sign == '+':
            cc = aa + bb
        else:
            cc = aa - bb
        c = cc.to_string()
        return c[:fixed_position] + '.' + c[fixed_position:]

    def equal(self):
        self.text_field.configure(state='normal')
        try:
            self.my_text = self.text_field.get() + '+'
            temp = ''
            sign = '+'
            res = '0.'
            for x in self.my_text:
                if x not in '+-':
                    temp += x
                else:
                    if temp.count('.') == 0: 
                        temp += '.'
                    res = self.operator(res, temp, sign)
                    temp = ''
                    sign = x

            res = res.lstrip('0')
            res = res.rstrip('0')
            if res[len(res)-1] == '.':
                res = res[:-1]
            if res == '':
                res = '0'
            self.text_field.delete(0, END)
            self.text_field.insert(END, res)
            self.text_field.configure(state='disabled')
        except:
            showwarning(title='Error', message='Invalid Input')
        self.text_field.configure(state='disabled')

    def back(self):
        self.text_field.configure(state='normal')
        self.my_text = self.text_field.get()
        try:
            self.my_text = self.my_text[:-1]
        except:
            pass
        self.text_field.delete(0, END)
        self.text_field.insert(0, self.my_text)
        self.text_field.configure(state='disabled')

    def clear(self):
        self.text_field.configure(state='normal')
        self.text_field.delete(0, END)
        self.text_field.configure(state='disabled')

    def __init__(self, master):
        for row_index in range(3):
            Grid.rowconfigure(master, row_index, weight=1)
        for column_index in range(4):
            Grid.columnconfigure(master, column_index, weight=1)
        """Setup text field"""
        self.text_field = Entry(master, justify='right')
        self.text_field.configure(state='disabled')
        self.text_field.grid(row=0, column=0, columnspan=4, sticky=N + S + E + W)

        """Setup variables"""
        self.my_text = ''

        """Setup menu"""
        menu = Menu(master)
        master.config(menu=menu)
	
        signMenu = Menu(menu)
        menu.add_cascade(label='Operators', menu=signMenu)
        signMenu.add_command(label='+', command=lambda: self.entry_text('+'))
        signMenu.add_command(label='-', command=lambda: self.entry_text('-'))

        editMenu = Menu(menu)
        menu.add_cascade(label='Edit', menu=editMenu)
        editMenu.add_command(label='←', command=lambda: self.back())
        editMenu.add_command(label='C', command=lambda: self.clear())

        helpMenu = Menu(menu)
        menu.add_cascade(label='Help', menu=helpMenu)
        helpMenu.add_command(label='About', command=lambda: showinfo(title='Info', message='Made by Nguyen Ngoc Hai'))

        """Setup buttons"""
        Button(master, text='-1', width=10, command=lambda: self.entry_text('T')).grid(row=1, column=0, sticky=N + S + E + W)
        Button(master, text='0', width=10, command=lambda: self.entry_text('0')).grid(row=1, column=1, sticky=N + S + E + W)
        Button(master, text='1', width=10, command=lambda: self.entry_text('1')).grid(row=2, column=0, sticky=N + S + E + W)
        Button(master, text='+', width=10, command=lambda: self.entry_text('+')).grid(row=1, column=2, sticky=N + S + E + W)
        Button(master, text='-', width=10, command=lambda: self.entry_text('-')).grid(row=2, column=2, sticky=N + S + E + W)
        Button(master, text='=', width=10, command=lambda: self.equal()).grid(row=2, column=3, sticky=N + S + E + W)
        Button(master, text='.', width=10, command=lambda: self.entry_text('.')).grid(row=2, column=1, sticky=N + S + E + W)
        Button(master, text='←', width=10, command=lambda: self.back()).grid(row=1, column=3, sticky=N + S + E + W)


if __name__ == '__main__':
    """Create and Configure root"""
    root = Tk()
    root.title('Calculator')

    """Create and Configure frame"""
    Grid.rowconfigure(root, 0, weight=1)
    Grid.columnconfigure(root, 0, weight=1)
    my_calc = CalcBalancedTernary(root)
    root.mainloop()
