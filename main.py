import tkinter as tk
from tkinter import colorchooser
import sqlite3
import random
zzz=0
winp1=0;winp2=0;roundd=0;p1=0;p2=0
x=[]
moving = False

def new_map():#انشاء مصوفة فيهة الترتيب والبونصات
    x.clear()
    for i in range(100):
        x.append(f"{i+1:02}")
    for i in range(10,90,10):
        n = random.randint(0, 9)
        m = random.randint(0, 9)
        x[i+n]=f'{i+n+1},{random.randint(-7,7)}'
        x[i+m]=f'{i+m+1},{random.randint(-15,7)}'

    for i in range(100):
        if ',' in x[i]:
            n,m=x[i].split(',')
            n=int(n);m=int(m)

            if(m==0):
                x[i]=f'{n+1},+6'
            if(';' in x[n+m]):
                x[i]=f' {n+1},+{m+1}'
            if m>0:
                x[i]=f' {n+1},+{m}'
new_map()


def pons(old_p, new_p, name1, color1, p2, name2, color2, callback=None):
    """تحريك اللاعب خانة بخانة، ثم استدعاء callback بعد انتهاء الحركة."""

    def restore_block(position):
        if position < 1 or position > 100:
            return

        # إذا كانت الخانة تحتوي اللاعب الآخر، لا نمسحه
        if position == p2 and p2 > 0:
            block[position]['text'] = name2
            block[position]['bg'] = color2
            return

        # إرجاع الخانة إلى شكلها الطبيعي
        block[position]['text'] = x[position - 1]
        if ',' in x[position - 1]:
            effect = int(x[position - 1].split(',')[1])
            if effect > 0:
                block[position]['bg'] = "#2e5dc3"
            elif effect < 0:
                block[position]['bg'] = "#c32e2e"
            else:
                block[position]['bg'] = "#2e5dc3"
        else:
            block[position]['bg'] = "#adadad"

    def put_player(position):
        if position < 1 or position > 100:
            return

        # اللاعبان في نفس الخانة
        if position == p2 and p2 > 0:
            block[position]['text'] = '(p1/p2)'
            block[position]['bg'] = "#fff49d"
        else:
            block[position]['text'] = name1
            block[position]['bg'] = color1

    # لا توجد حركة
    if old_p == new_p:
        put_player(new_p)
        if callback:
            xx.after(300, lambda: callback(new_p))
        return

    if new_p > old_p:
        now = old_p
        def move_forward():
            nonlocal now
            # إزالة اللاعب من الخانة الحالية أولاً
            if now >= 1:
                restore_block(now)
            now += 1
            put_player(now)

            if now < new_p:
                xx.after(500, move_forward)
            elif callback:
                xx.after(500, lambda: callback(new_p))

        move_forward()

    else:
        now = old_p
        def move_backward():
            nonlocal now
            if now >= 1:
                restore_block(now)
            now -= 1
            put_player(now)

            if now > new_p:
                xx.after(500, move_backward)
            elif callback:
                xx.after(500, lambda: callback(new_p))

        move_backward()


def chaing(p1, name1, color1, p2=0, name2='(p2)', color2='green', bot_level=1, callback=None):

    if bot_level == 1:
        num = random.randint(1, 6)

    elif bot_level == 2:
        possible = []

        for step in range(1, 7):
            position = p1 + step
            if position > 100:
                continue

            if ',' in x[position - 1]:
                effect = int(x[position - 1].split(',')[1])
                if effect > 0:
                    possible.append(step)

        if possible:
            num = random.choice(possible)
        else:
            num = random.randint(1, 6)

    elif bot_level == 3:
        positive = []
        safe = []

        for step in range(1, 7):
            position = p1 + step
            if position > 100:
                continue

            if ',' in x[position - 1]:
                effect = int(x[position - 1].split(',')[1])
                if effect > 0:
                    positive.append(step)
                elif effect < 0:
                    continue
            else:
                safe.append(step)

        if positive:
            num = random.choice(positive)
        elif safe:
            num = random.choice(safe)
        else:
            num = random.randint(1, 6)
    else:
        num = random.randint(1, 6)

    lb3['text'] = num

    new_p = p1 + num

    # إذا تجاوز اللاعب الخانة 100، لا يتحرك
    if new_p > 100:
        lb4['text'] = 'over'
        if callback:
            xx.after(300, lambda: callback(p1))
        return

    effect = 0

    if ',' in x[new_p - 1]:
        effect = int(x[new_p - 1].split(',')[1])

        if effect > 0:
            lb4['text'] = f"you up, {effect}"
        elif effect < 0:
            lb4['text'] = f"you down, {effect}"
        else:
            lb4['text'] = ''
    else:
        lb4['text'] = ''

    final_p = new_p + effect

    if final_p < 1:
        final_p = 1

    if final_p > 100:
        lb4['text'] = 'over'
        if callback:
            xx.after(300, lambda: callback(p1))
        return

    # لا يوجد تأثير: حركة واحدة فقط
    if effect == 0:
        pons(p1, new_p, name1, color1,p2, name2, color2,
             callback=lambda pos: callback(pos) if callback else None)
        return

    # يوجد تأثير: ننتظر انتهاء حركة
    def apply_effect(_):
        # lambda يعني من يخلص الوكت فعل الدالة
        xx.after(300, lambda: pons(new_p, final_p, name1, color1,p2, name2, color2,
                                    callback=lambda pos: callback(pos) if callback else None))

    pons(p1, new_p, name1, color1,p2, name2, color2,callback=apply_effect)


def click():
    global p1, p2, roundd, zzz, moving

    # منع الضغط أثناء حركة اللاعب
    if moving:
        return

    moving = True
    butn.config(state='disabled')
    zzz += 1

    # دور اللاعب 1
    if zzz % 2 == 1:

        def player1_done(final_position):
            global p1, roundd, moving

            p1 = final_position
            lb5['text'] = f'playr(1) : {p1:02}'

            if p1 == 100:
                moving = False
                winer(1)
                return

            roundd += 1
            lb0['text'] = f'the round is: {roundd}'
            butn['bg'] = settings['color_2']

            # دور الكمبيوتر
            if settings["players"] == 1:
                xx.after(500, computer_turn)
            else:
                moving = False
                butn.config(state='normal')
        chaing(p1, '(p1)', settings['color_1'],p2, '(p2)', settings['color_2'],callback=player1_done)

    elif settings["players"] == 2:

        def player2_done(final_position):
            global p2, roundd, moving
            p2 = final_position
            lb6['text'] = f'playr(2) : {p2:02}'

            if p2 == 100:
                moving = False
                winer(2)
                return

            roundd += 1
            lb0['text'] = f'the round is: {roundd}'
            butn['bg'] = settings['color_1']

            moving = False
            butn.config(state='normal')
        chaing(p2, '(P2)', settings['color_2'],p1, '(p1)', settings['color_1'],callback=player2_done)

# دور الكمبيوتر
def computer_turn():
    global p2, roundd, zzz, moving

    # يبقى الزر معطلاً أثناء حركة الكمبيوتر
    moving = True
    butn.config(state='disabled')
    zzz += 1

    def computer_done(final_position):
        global p2, roundd, moving

        p2 = final_position
        lb6['text'] = f'Computer : {p2:02}'

        if p2 == 100:
            moving = False
            winer(2)
            return

        roundd += 1
        lb0['text'] = f'the round is: {roundd}'
        butn['bg'] = settings['color_1']

        moving = False
        butn.config(state='normal')
    chaing(p2, '(P2)', settings['color_2'],p1, '(p1)', settings['color_1'],settings['bot_level'],callback=computer_done)

def re_zero():
    global p1, p2, roundd

    if p1>0:
        block[p1]['text']=x[p1-1]
        block[p1]['bg']="#adadad"
    if p2>0:
        block[p2]['text']=x[p2-1]
        block[p2]['bg']="#adadad"

    p1 = 0
    p2 = 0
    roundd = 0
    lb5['text']=0
    lb6['text']=0
    lb0['text']=0

    new_map()
    update_map()

def winer(player):
     global winp1, winp2, moving, zzz
     moving = False
     zzz=1   
     if player==1:
          winp1+=1
          lb1['text']=f'playr(1) is win : {winp1}'
          lb4['text'] = "Player 1 WIN!"
          w_block[5,4]['text']='plyer 1'

     if player==2:
          winp2+=1
          lb2['text']=f'playr(2) is win : {winp2}'
          lb4['text'] = "Player 2 WIN!"
          w_block[5,4]['text']='plyer 2'
     re_zero()
     winer_window.deiconify()
     xx.withdraw()


     
    

#======================================================================================
#======================================================================================
#======================================================================================
xx = tk.Tk()
xx.withdraw()

db = sqlite3.connect("game_settings.db")#dbيمثل الاتصال بقاعدة البيانات
cursor = db.cursor()#عرفت متغير علمود من خلاله ارسل البيانات للقاعدة
#انشاء جدول وتحديد نوع البانات
#IF NOT EXISTS اذا ماكو انشاء جدول 
#من السطر الاول جوة حددت الاسم settings للقاعدة
cursor.execute("""
CREATE TABLE IF NOT EXISTS settings (
    id INTEGER PRIMARY KEY,
    players INTEGER,
    bot_level INTEGER,
    color_1 TEXT,
    color_2 TEXT
)
""")
cursor.execute("""
INSERT OR IGNORE INTO settings
(id, players, bot_level, color_1, color_2)
VALUES (1, 2, 1, 'purple', 'green')
""")
db.commit()#حفظ التغيرات

#كود القراء للSQL
cursor.execute("""
SELECT players, bot_level, color_1, color_2
FROM settings
WHERE id = 1
""")

row = cursor.fetchone()#احضر الصفوف بالترتيب من عملية القرائة في الاعلى
settings = {
    "players": row[0],
    "bot_level": row[1],
    "color_1": row[2],
    "color_2": row[3]
}

def start_game():
    global p1,p2
    settings["players"] = players.get()
    settings["bot_level"] = bot_level.get()
    settings['color_1']=color_1.get()
    settings['color_2']=color_2.get()

    lb5['bg']=settings['color_1']
    lb6['bg']=settings['color_2']

    if p1>0:
            block[p1]['bg']=settings['color_1']
    if p2>0:
            block[p2]['bg']=settings['color_2']

#الخانة الاولة مكان موقت للقيم والثانية ارسال القيم الؤقتة الى مكان الستخدام
    cursor.execute("""
    UPDATE settings
    SET players = ?,
        bot_level = ?,
        color_1 = ?,
        color_2 = ?
    WHERE id = 1
    """, (
        settings["players"],
        settings["bot_level"],
        settings["color_1"],
        settings["color_2"]
    ))
    db.commit()

    settings_window.withdraw()
    xx.deiconify()


def exit_game():
    settings_window.destroy()
    winer_window.destroy()
    xx.destroy()

def setting_buton():
    xx.withdraw()
    settings_window.deiconify()

# نافذة الإعدادات
settings_window = tk.Toplevel(xx)#لإنشاء نافذة جديدة مرتبطة بالرئيسية
settings_window.title("Game Settings")
settings_window.geometry("300x400")
settings_window.resizable(False, False)#امكتنية تغير حجم النافذة

#عنوان
title = tk.Label(settings_window,text="Game Settings",font=("Arial",18,"bold"))
title.pack(pady=20)

#اختيار عدد الاواعيب
fr_players_label=tk.Frame(settings_window)
fr_players_label.pack()

players_label = tk.Label(fr_players_label,text="Number of players:")
players_label.grid(row=0, column=0, padx=10)

players = tk.IntVar(value=settings['players'])
players_menu = tk.OptionMenu(fr_players_label,players,1,2)
players_menu.grid(row=0, column=1, padx=10)


# صعوبة البوت
fr_bot_level_lb=tk.Frame(settings_window,pady=20)
fr_bot_level_lb.pack()

bot_level_lb = tk.Label(fr_bot_level_lb,text="level of bot :")
bot_level_lb.grid(row=0, column=0, padx=10)

bot_level = tk.IntVar(value=settings['bot_level'])
bot_level_menu = tk.OptionMenu(fr_bot_level_lb,bot_level,1,2,3)
bot_level_menu.grid(row=0, column=1, padx=10)


# اختيار الاون الاول
def choose_color_1():#كاعد افتح نافذة مخصصة بالاون
    color = colorchooser.askcolor(title="Choose Player 1 Color",initialcolor=color_1.get())
    #initialcolor يجعل الاون الحالي هوة الافتراضي
    if color[1]:#من فوك اخذت الاون على شكل الاول ارجيبي والثاني هيكس فاخذ الثاني
        color_1.set(color[1])
        color_1_button.config(bg=color[1])#تغير لون زر اختيار الاون

fr_color_1 = tk.Frame(settings_window, pady=10)
fr_color_1.pack()

color_1_label = tk.Label(fr_color_1,text="Color of Player 1 :")
color_1_label.grid(row=0, column=0, padx=10)

color_1 = tk.StringVar(value=settings['color_1'])
color_1_button = tk.Button(fr_color_1,text="Choose Color",width=10,
                           bg=color_1.get(),command=choose_color_1)
color_1_button.grid(row=0, column=1, padx=10)


# اختيار الاون الثاني
def choose_color_2():
    color = colorchooser.askcolor(title="Choose Player 2 Color",initialcolor=color_2.get())
    if color[1]:
        color_2.set(color[1])
        color_2_button.config(bg=color[1])

fr_color_2 = tk.Frame(settings_window, pady=10)
fr_color_2.pack()

color_2_label = tk.Label(fr_color_2,text="Color of Player 2 :")
color_2_label.grid(row=0, column=0, padx=10)

color_2 = tk.StringVar(value=settings['color_2'])
color_2_button = tk.Button(fr_color_2,text="Choose Color",width=10,
                           bg=color_2.get(),command=choose_color_2)
color_2_button.grid(row=0, column=1, padx=10)




start_button = tk.Button(settings_window,text="START GAME",width=15,command=start_game,relief="flat"
                         ,bd=0,cursor="hand2",bg="#a5e6fc")
start_button.pack(pady=20)

exit_button = tk.Button(settings_window,text="EXIT",width=15,command=exit_game,relief="flat"
                        ,bd=0,cursor="hand2",bg="#a5e6fc")
exit_button.pack()

#=================================================
#=================================================
#=================================================

m=tk.PanedWindow()
m.pack()

m1=tk.PanedWindow(m)
m1.pack()
frame1 = tk.Frame(m1)
frame2 = tk.Frame(m1)
frame3 = tk.Frame(m1)
m1.add(frame1)
m1.add(frame2)
m1.add(frame3)
lb1=tk.Label(frame1,height=2,width=14,fg='white',bg="#3d6e74",text=f'playr(1) is win : {winp1}')
lb0=tk.Label(frame2,height=2,width=11,fg='white',bg="#3d6e74",text=f'the round is: {roundd}')
lb2=tk.Label(frame3,height=2,width=14,fg='white',bg="#3d6e74",text=f'playr(2) is win : {winp2}')
lb1.pack(padx=(10,0), pady=(10, 10))
lb0.pack(padx=(10,0), pady=(10, 10))
lb2.pack(padx=(10,0), pady=(10, 10))


b1=tk.Button(m,command=re_zero,text=('Re Start'),bg="#eae486")
b1.place(relx=1.0, x=0, y=10, anchor='e')

b2=tk.Button(m,command=setting_buton,text=('setting'),bg="#eae486")
b2.place(relx=1.0, x=-510, y=0)


m2 = {}
block = {}
block[0]=0
m2[1] = tk.PanedWindow(m)
m2[1].pack()

def new_map_block():
    j=1

    for i in range(90, -10, -10):
        for ii in range(10):

            if (i + ii) % 10 == 0 and i != 100:
                j += 1
                m2[j] = tk.PanedWindow(m)
                m2[j].pack()

            block[i + ii + 1] = tk.Label(m2[j],text=f"{x[i + ii]:02}",height=2,
                                        width=6,bg="#adadad")

            m2[j].add(block[i + ii + 1])
new_map_block()

def update_map():
    for i in range(100):
        number = i + 1

        block[number]['text'] = x[i]
        block[number]['bg'] = "#adadad"

        if ',' in x[i]:
            effect = int(x[i].split(',')[1])

            if effect >= 0:
                block[number]['bg'] = "#2e5dc3"

            elif effect < 0:
                block[number]['bg'] = "#c32e2e"
update_map()

m3=tk.PanedWindow(m)
m3.pack()
frame10 = tk.Frame(m3)
frame20 = tk.Frame(m3)
m3.add(frame10)
m3.add(frame20)
lb3 = tk.Label(frame10,height=2,width=6,fg='white',bg="#3d6e74",text='0')
lb4 = tk.Label(frame20,height=2,width=22,fg='white',bg="#3d6e74",text='if you get affect is see in her')
lb3.pack(pady=(20, 0))
lb4.pack(anchor='w', padx=(50,0), pady=(20, 0))


m4=tk.PanedWindow(m)
m4.pack()
frame100 = tk.Frame(m4)
frame200 = tk.Frame(m4)
m4.add(frame100)
m4.add(frame200)
lb5 = tk.Label(frame100,height=2,width=10,fg='white',bg=settings['color_1'],text=f'playr(1) : {p1:02}')
lb6 = tk.Label(frame200,height=2,width=10,fg='white',bg=settings['color_2'],text=f'playr(2) : {p2:02}')
lb5.pack(pady=(20, 0))
lb6.pack(anchor='w', padx=(20,0), pady=(20, 0))

m5=tk.PanedWindow(m)
m5.pack()
butn=tk.Button(
    m5,text="CLICK",font=("Arial", 12, "bold"),fg="white",bg="#0e274c",activeforeground="white",activebackground="#2f5559",width=10,
    height=2,relief="flat",bd=0,cursor="hand2",command=click)
m5.add(butn)


#==========================================


winer_window = tk.Toplevel(xx)
winer_window.title("Game Settings")
winer_window.geometry("300x450")
winer_window.resizable(False, False)
winer_window.withdraw()

w = {}
w_block = {}
for i in range(0, 6):
    w[i] = tk.PanedWindow(winer_window)
    w[i].pack()
    for ii in range(0, i + 1):
        w_block[i, ii] = tk.Label(w[i],text='*',height=2,width=4,bg="#8fff66")
        w_block[i, ii].pack(side='left')#خليه على يسار العنصر السابق

w_block[5,1]['text']='the'
w_block[5,2]['text']='winer'
w_block[5,3]['text']='is'

w2 = {}
w_block2 = {}
for i in range(4, 0,-1):
    w2[i] = tk.PanedWindow(winer_window)
    w2[i].pack()
    for ii in range(0, i):
        w_block2[i, ii] = tk.Label(w2[i],text='*',height=2,width=4,bg="#8fff66")
        w_block2[i, ii].pack(side='left')

f_winer=tk.Frame(winer_window,pady=10)
f_winer.pack()

w_boutn_exit=tk.Button(f_winer,text='exit game',command=exit_game,fg="white",bg="#3d6e74",
    activeforeground="white",activebackground="#2f5559",width=12,height=2,relief="flat",cursor="hand2")
w_boutn_exit.pack(side='left',padx=5)

def cont():
    xx.deiconify()
    winer_window.withdraw()

w_boutn_cont=tk.Button(f_winer,text='continoe game',command=cont,fg="white",bg="#3d6e74",
    activeforeground="white",activebackground="#2f5559",width=12,height=2,relief="flat",cursor="hand2")
w_boutn_cont.pack(side='left')





xx.mainloop()

