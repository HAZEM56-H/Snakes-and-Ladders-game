from project import check_num_chaing
from project import check_name_chaing
from project import check_color_chaing

import tkinter as tk
root = tk.Tk()
root.withdraw()

block = {}

for i in range(1, 101):
    block[i] = tk.Label(root,text='hh',bg="#ffffff")

def test_number():
#(p, x, block)
    assert check_num_chaing(25, 5, block) == 30
    assert check_num_chaing(98, 5, block) == 98
    assert check_num_chaing(3, -5, block) == 1


def test_name():
#(p1,p2,x,name,block)
    assert check_name_chaing(25,0,5,'p1', block) == 'p1'
    assert check_name_chaing(25, 5, 1,'p2', block) == 'p2'
    assert check_name_chaing(26, 32, 6, 'p1', block) == 'p1/p2'


def test_color():
#(x,block)
    assert check_color_chaing('25,+6', block) == "#2e5dc3"
    assert check_color_chaing('98,-9', block) == "#c32e2e"
    assert check_color_chaing('66', block) == "#adadad"
