import tkinter as tk
import tkinter.font as tf
from tkinter import messagebox
from pathlib import Path


class calcGui:
    def __init__(self):

        self.windowSetup()
        self.initTKvariable()
        self.createPhotoLabel()
        self.createLabel()
        self.createShowText()
        self.createShowButton()
        self.createCalcCostButton()
        self.createShowIncomeButton()
        self.createCalcIncomeButton()
        self.createQuitButton()
        self.createUndateButton()
        self.runUI()


    def windowSetup(self):
        self.window = tk.Tk()

        self.window.title('Cost Calculator')
        self.window.geometry('1200x900')
        self.window.config(bg='grey')
        self.window.resizable(1, 1)


    def initTKvariable(self):

        self.textFT = tf.Font(family='Arial', size=12, weight=tf.BOLD)
        self.labelFT = tf.Font(family='Arial', size=16, weight=tf.BOLD)
        self.buttonFT = tf.Font(family='Times', size=14, weight=tf.BOLD)

        self.stateLabelVar = tk.StringVar()
        self.stateLabelVar.set('请点击左侧的功能按钮！')

        self.isShowTextOn = tk.BooleanVar()
        self.isShowTextOn = False

        self.updateFileName = ''


    def createPhotoLabel(self):
        self.p = Path.cwd()
        self.finalPath = ''
        self.isFound = False

        while self.finalPath == '':

            self.ret = Path(self.p).glob('2.gif')
            for item in self.ret:
                if item != '':
                    self.finalPath = item
                    self.isFound = True

            if self.isFound:
                break
            else:
                self.p = self.p.parent

        self.bgPhoto = tk.PhotoImage(file=self.finalPath)

        photoLabel = tk.Label(self.window, image=self.bgPhoto, compound=tk.CENTER)
        photoLabel.pack()


    def createLabel(self):
        self.stateLabel = tk.Label(self.window, textvariable=self.stateLabelVar, height=2, font=self.labelFT,
                                   bg='white')
        self.stateLabel.place(x=760, y=60, anchor='nw')


    def createShowText(self):
        self.showText = tk.Text(self.window, width=60, height=36, font=self.textFT)
        self.showText.place(x=580, y=180, anchor='nw')


    def createShowButton(self):
        self.showButton = tk.Button(self.window, text='花费表', command=self.ReadAll, width=15, height=3,
                                    font=self.buttonFT,
                                    relief=tk.GROOVE, cursor='hand2', activebackground='grey', activeforeground='white')
        self.showButton.place(x=70, y=200, anchor='nw')


    def createCalcCostButton(self):
        self.calcCostButton = tk.Button(self.window, text='计算总花费', command=self.StartCal, width=15, height=3,
                                        font=self.buttonFT,
                                        relief=tk.GROOVE, cursor='hand2', activebackground='grey',
                                        activeforeground='white')
        self.calcCostButton.place(x=340, y=200, anchor='nw')


    def createCalcIncomeButton(self):
        self.calcIncomeButton = tk.Button(self.window, text='计算总收益', command=self.Income, width=15, height=3,
                                          font=self.buttonFT,
                                          relief=tk.GROOVE, cursor='hand2', activebackground='grey',
                                          activeforeground='white')
        self.calcIncomeButton.place(x=340, y=350, anchor='nw')


    def createShowIncomeButton(self):
        self.showIncomeButton = tk.Button(self.window,text='收益表', font=self.buttonFT,width=15,height=3,
                                          command=self.showIncome,relief=tk.GROOVE, cursor='hand2', activebackground='grey',
                                          activeforeground='white')
        self.showIncomeButton.place(x=70, y=350, anchor='nw')


    def createQuitButton(self):
        self.quitButton = tk.Button(self.window, text='Quit', command=self.window.destroy, width=15, height=3,
                                    font=self.buttonFT,
                                    relief=tk.GROOVE, cursor='hand2', activebackground='grey', activeforeground='white')
        self.quitButton.place(x=70, y=500, anchor='nw')


    def createUndateButton(self):
        self.updateButton = tk.Button(self.window, text='Update', command=self.UpdateText, width=15, height=3,
                                      font=self.buttonFT,
                                      relief=tk.GROOVE, cursor='hand2', activebackground='grey',
                                      activeforeground='white')
        self.updateButton.place(x=70, y=650, anchor='nw')


    def ReadAll(self):
        with open(Path.joinpath(self.p, 'COST.txt'), 'r', encoding='UTF-8') as fh:
            self.isShowTextOn = True
            self.updateFileName = 'Cost'
            self.showText.delete(0.0, tk.END)
            self.showText.insert('end', fh.read())


    def UpdateText(self):
        if self.isShowTextOn:
            if self.updateFileName == 'Cost':
                with open(Path.joinpath(self.p, 'COST.txt'), 'w', encoding='UTF-8') as fh:
                    fh.write(self.showText.get(0.0, tk.END))
                    tk.messagebox.showinfo(title='Update Completed', message='更新完毕！')
            elif self.updateFileName == 'Income':
                with open(Path.joinpath(self.p, 'Income.txt'), 'w', encoding='UTF-8') as fh:
                    fh.write(self.showText.get(0.0, tk.END))
                    tk.messagebox.showinfo(title='Update Completed', message='更新完毕！')
        else:
            tk.messagebox.showerror(title='Error!!!!', message='你的内容框是空白的！')


    def StartCal(self):
        numCollections = []
        with open(Path.joinpath(self.p, 'COST.txt'), 'r', encoding='UTF-8') as fh:
            for line in fh.readlines():
                for i in line:
                    if i == '￥':
                        numCollections.append(float(line[line.index(i) + 1:].strip()))

        self.stateLabelVar.set('总成本为{:.2f}'.format(sum(numCollections)))
        self.stateLabel.config(fg='black', bg='white')

    def Income(self):
        infoList = []

        with open(Path.joinpath(self.p, 'Income.txt'), 'r', encoding='UTF-8') as fh:
            for index, line in enumerate(fh.readlines()):
                if index == 0 or line == '\n':
                    continue

                oneInfo = line.split()

                if len(oneInfo) > 1:
                    infoList.append({'Date': oneInfo[0], 'Income': float(oneInfo[1])})

            totalIncome = sum([i['Income'] for i in infoList])
            self.stateLabelVar.set("总收益：{:.2f}".format(totalIncome))
            self.stateLabel.config(fg='red', bg='white')

    def showIncome(self):
        with open(Path.joinpath(self.p, 'Income.txt'), 'r', encoding='UTF-8') as fh:
            self.isShowTextOn = True
            self.updateFileName = 'Income'
            self.showText.delete(0.0, tk.END)
            self.showText.insert('end', fh.read())

    def runUI(self):
        self.window.mainloop()


"""def StartCal():
    numCollections = []
    with open('COST.txt', 'r', encoding='UTF-8') as fh:
        for line in fh.readlines():
            for i in line:
                if i == '￥':
                    numCollections.append(float(line[line.index(i) + 1:].strip()))

    print('\n\n\n\n\n')

    print('\n\n\n                   总成本为{:.2f}\n\n\n\n'.format(sum(numCollections)))


def ReadAll():
    with open('COST.txt', 'r', encoding='UTF-8') as fh:
        for line in fh.readlines():
            print(line)


def Income():
    infoList = []

    with open('Income.txt', 'r', encoding='UTF-8') as fh:
        for index, line in enumerate(fh.readlines()):
            if index == 0 or line == '\n':
                continue

            print(line,end='')

            oneInfo = line.split()
            infoList.append({'Date': oneInfo[0], 'Income': float(oneInfo[1])})

        totalIncome = sum([i['Income'] for i in infoList])
        print("\n\n总收益：{:.2f}".format(totalIncome))
"""

if __name__ == '__main__':
    runCalculator = calcGui()

    """print('-' * 55)
    userInput = input("\n\n请输入以下数字\n1. 花费列表\n2. 价格总和\n3. 退出程序\n4. 总收益\n\n>>")
    print('-' * 55)

    if userInput == '1':
        ReadAll()
    elif userInput == '2':
        StartCal()
    elif userInput == '3':
        break
    elif userInput == '4':
        Income()
    else:
        print("Wrong Input. Try again!")"""


