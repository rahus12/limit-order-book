import random
import time
class book:
    def __init__(self): 
        #mock ask and bid values
        #mocking a json format        

        self.order = {
            'ask':{
                1:{'price':10.0,'quantity':200},
                3:{'price':10.3,'quantity':100},
                5:{'price':10.4,'quantity':300},
                2:{'price':10.2,'quantity':500},
                7:{'price':10.7,'quantity':400},
            },

            'bid':{
                1:{'price':12.0,'quantity':200},
                3:{'price':12.3,'quantity':100},
                5:{'price':12.4,'quantity':300},
                2:{'price':12.2,'quantity':500},
                7:{'price':12.7,'quantity':400},
            }
        }

        self.limit_buy_queue = []
        self.limit_sell_queue = []

    #To generate a 5 digit unique id
    def generate_id(self):
        t = int(time.time()/20000)        
        x = random.randint(10000,t)
        return x
        
    def show_book(self):
        print("\nAsking Rates\nRate\tQuantity")        

        for j in sorted(self.order['ask'].items(), key = lambda x:x[1]['price']):
            print("{}\t{}".format(j[1]['price'],j[1]['quantity']))

        print("\nBid Rates\nRate\tQuantity")

        #print rate and quantity               
        for j in sorted(self.order['bid'].items(), key = lambda x:x[1]['price'],reverse=True):
            print("{}\t{}".format(j[1]['price'],j[1]['quantity']))

    def buy_order(self,id,price,quantity):
        self.order['ask'][id]['quantity'] -= quantity
        print("buy order of {} quantity at {} per share success".format(quantity,price))
    
    
    def sell_order(self,id,price,quantity):
        self.order['bid'][id]['quantity'] -= quantity
        print("buy order of {} quantity at {} per share success".format(quantity,price))
    
    def market_order_buy(self,quantity):
        for lst in sorted(self.order['ask'].items(), key = lambda x:x[1]['price']):
            price = lst[1]['price']            
            _quantity = lst[1]['quantity']
            id = lst[0]
            if( quantity <= _quantity ):
                self.buy_order(id,price,quantity)
                quantity -= _quantity
                break
            else:
                self.buy_order(id,price,_quantity)
                quantity -= _quantity           
        if quantity > 0:
            print("{} quantity of share remaining in queue".format(quantity))

    def market_order_sell(self,quantity):
        for lst in sorted(self.order['bid'].items(), key = lambda x:x[1]['price'],reverse=True):
            price = lst[1]['price']            
            _quantity = lst[1]['quantity']
            id = lst[0]
            if( quantity <= _quantity ):
                self.sell_order(id,price,quantity)
                quantity -= _quantity
                break
            else:
                self.sell_order(id,price,_quantity)
                quantity -= _quantity           
        if quantity > 0:
            print("{} quantity of share remaining in queue".format(quantity))
            

    def limit_order_buy(self,l_price,quantity):
        for lst in sorted(self.order['ask'].items(), key = lambda x:x[1]['price']):
            price = lst[1]['price'] 
            if price <= l_price :           
                _quantity = lst[1]['quantity']
                id = lst[0]
                if( quantity <= _quantity ):
                    self.buy_order(id,price,quantity)
                    quantity -= _quantity
                    break
                else:
                    self.buy_order(id,price,_quantity)
                    quantity -= _quantity           
        if quantity > 0:
            orderId = self.generate_id()
            self.limit_buy_queue.append("orderId: "+str(orderId)+" price: "+str(price)+" quantity: "+str(quantity))
            self.order['bid'][orderId] = {'price':price,'quantity':quantity}
            print("{} quantity of share remaining in queue \norder id: {}\n".format(quantity,orderId))
            # uncomment this to see your order added to the orders
            # self.show_book()

    def limit_order_sell(self,l_price,quantity):
        for lst in sorted(self.order['ask'].items(), key = lambda x:x[1]['price'],reverse=True):
            price = lst[1]['price'] 
            if price <= l_price :           
                _quantity = lst[1]['quantity']
                id = lst[0]
                if( quantity <= _quantity ):
                    self.sell_order(id,price,quantity)
                    quantity -= _quantity
                    break
                else:
                    self.sell_order(id,price,_quantity)
                    quantity -= _quantity           
        if quantity > 0:
            orderId = self.generate_id()
            self.limit_sell_queue.append("orderId: "+str(orderId)+" price: "+str(price)+" quantity: "+str(quantity))
            self.order['ask'][orderId] = {'price':price,'quantity':quantity}
            print("{} quantity of share remaining in queue \norder id: {}\n".format(quantity,orderId))        
            # uncomment this to see your order added to the orders
            # self.show_book()

    def cancel_buy_order(self,orderId):
        if orderId in self.order['bid'].keys():
            del self.order['bid'][orderId]
            print("order id: {} canceled")
        else:
            print("order id :{} does not exist".format(orderId))
    
    def cancel_sell_order(self,orderId):
        if orderId in self.order['bid'].keys():
            del self.order['ask'][orderId]
            print("order id: {} canceled")
        else:
            print("order id :{} does not exist".format(orderId))

    def show_pending_queue(self):
        print("\nBuy queue")
        if(len(self.limit_buy_queue)>0):
            for _order in self.limit_buy_queue:
                print(_order)
        else:
            print("Buy queue is empty")
        
        print("\nSell queue")
        if(len(self.limit_sell_queue)>0):
            for _order in self.limit_sell_queue:
                print(_order)
        else:
            print("sell queue is empty")

limitbook = book()

#show the ask and bid rates of selected company
limitbook.show_book()

while(True):
    print("\nEnter the command")
    command = input("Buy[b]\tSell[s]\tcancel order[c]\tshow order queue[q]\texit[e]:  ")

    

    if(command.lower()=='b'):
        order_type = input("Type of order: Market or Limit [m/l]: ")    
        if(order_type.lower()=='m'):       
            quantity = int(input("Enter quantity: "))        
            limitbook.market_order_buy(quantity)
        
        else:
            l_price = float(input("Enter limit price: "))
            quantity = int(input("Enter quantity: "))
            limitbook.limit_order_buy(l_price,quantity)

    elif(command.lower()=='s'):
        order_type = input("Type of order: Market or Limit [m/l]: ")
        if(order_type.lower()=='m'):       
            quantity = int(input("Enter quantity: "))        
            limitbook.market_order_sell(quantity)
        
        else:
            l_price = float(input("Enter limit price: "))
            quantity = int(input("Enter quantity: "))
            limitbook.limit_order_sell(l_price,quantity)
    
    elif(command.lower()=='c'):
        command = input("Cancel buy order[b]: \nCancel sell order[s]: ")
        if(command.lower()=='b'):
            orderId = int(input("Enter orderId: "))
            limitbook.cancel_buy_order(orderId)
        if(command.lower()=='s'):
            orderId = int(input("Enter orderId: "))
            limitbook.cancel_sell_order(orderId)
    
    elif(command.lower()=='q'):
        limitbook.show_pending_queue()
    
    elif(command.lower()=='e'):
        exit(0)
    
    else:
        print("Invalid command input")
