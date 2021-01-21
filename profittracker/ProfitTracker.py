import datetime
import json
import PySimpleGUI as gui
import calc
import os

addB = gui.Button('Add Order', key='addorder')
price = gui.InputText(key='price')
amount = gui.InputText(key='amount')
wallet = gui.InputText(key='wallet')
buy = gui.Radio('Buy','buysell',default=True,key='buy')
sell = gui.Radio('Sell','buysell',key='sell')
enterP = gui.InputText(key='enterP')
exitP = gui.InputText(key='exitP')
calculate = gui.Button('Calculate Profit:', key='calculate')
orders = gui.Multiline(key='orders', disabled=True, size=(55,20))
clearorders = gui.Button('DELETE ALL ORDERS',key='delete')

layout=[
[clearorders],
[gui.Text('Price(USDT):'),price,buy,sell],
[gui.Text('Amount(BTC):'),amount,gui.Text('Wallet Balance(USDT):'),wallet,addB],
[],
[gui.Text('Profit Calculator(%)')],
[gui.Text('Enter Price(USDT):'),enterP,calculate],
[gui.Text('Exit Price(USDT):'),exitP],
[gui.Text('Wallet Value Graph(USDT)'), gui.Text('Orders:', )],
[gui.Graph(canvas_size=(550,300),graph_bottom_left=(0,0),graph_top_right=(50,100),key='graph'), orders]
]

gui.theme('LightGreen5')
w = gui.Window(title=f"{datetime.date.today()} Profit Tracker",layout=layout).Finalize()
graph = w['graph']
graph.DrawLine((1,0),(1,100))
graph.DrawText( 'Date', (2.3,3))
graph.DrawLine((0,5),(50,5))
graph.DrawText( 'V\na\nl\nu\ne', (0.5,18))

global points 
points = []
global n
n=0
def drawGraphPoints(wallet,i):
    global n
    global points
    g = w['graph']
    p = (float(i)+1,float(wallet))
    g.DrawPoint(p,0.3)
    points.append(p)
    if n == 1:
        print(i)
        #drawGraphLines(points[int(i-1)],points[int(i)-2])
        n=0
        #draws lines, but is struggling to figure out when to run drawLines(), gives list index out of range, breaks after second startup
    else:
        n+=1

def drawGraphLines(p1,p2):
    g = w['graph']
    g.DrawLine(p1,p2)

def delete(i):
    try:
        os.remove(f"orders\order{i}.json")
        a = {'amount':'0'}
        with open(f'orders\orders.json', 'w') as f:
            json.dump(a, f)
    except:
        w['orders'].print('all orders deleted already!')

def printOrders(i):
    with open(f'orders\order{i}.json', 'r') as f:
        d = json.load(f)
    price = d['price']
    amount = d['amount']
    wallet = d['wallet']
    if d['buy'] is True:
        buy = 'Buy'
        sell = ''
    else:
        sell = 'Sell'
        buy = ''
    idnum = d['id']
    w['orders'].print(f'{buy}{sell} Price:{price} Amount:{amount} Wallet Balance:{wallet}$ Id:{idnum} \n')
    drawGraphPoints(wallet,idnum)
with open(f'orders\orders.json', 'r') as f:
        am = json.load(f)
for i in reversed(range(1,int(am['amount'])+1)):
    printOrders(i)
    #runs printOrders amount of old orders times
while True:
    event, values = w.read()
    if event == 'addorder':
        with open(f'orders\orders.json', 'r') as f:
            i = json.load(f)
        newid = int(i['amount'])+1
        #makes new id, reads old amount of orders, adds 1 ^^^
        data = {'price':values['price'],'buy':values['buy'],'amount':values['amount'],'wallet':values['wallet'],'id':newid}
        with open(f'orders\order{newid}.json', 'w+') as f:
            json.dump(data, f)   
        a = {'amount':f'{newid}'}
        #new amount of orders ^^^
        with open(f'orders\orders.json', 'w') as f:
            json.dump(a, f)
        #file that stores the amount of orders made ^^^
        printOrders(newid)
        drawGraphPoints(values['wallet'],newid)
    if event == 'calculate':
        try:
            p = calc.calc(int(values['enterP']),int(values['exitP']))
            w.Element('calculate').Update(text=f'Profit:{p}%')
        except:
            w.Element('calculate').Update(text='Type in price values!')
    if event == 'delete':
        with open(f'orders\orders.json', 'r') as f:
            am = json.load(f)
        for i in range(1,int(am['amount'])+1):
            delete(i)
    if event==gui.WIN_CLOSED or event=='Exit':
        break
