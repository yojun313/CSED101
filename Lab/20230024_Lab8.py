class BankAccount:

    def __init__(self, name = None, balance = 0):
        self.name = name
        self.balance = balance
    
    def deposit(self, amount):
        self.balance += amount
    
    def withdraw(self, amount):
        self.balance -= amount
        
    def transfer(self, other, amount):
        if self.balance >= amount:
            other.deposit(amount)
            self.withdraw(amount)
        else:
            print("잔액 부족!")
    
    def get_info(self):
        print("이름: %s, 잔고: %s" % (self.name, self.balance))
        
    def __str__(self):
        return "이름: %s, 잔고: %d" %(self.name, self.balance)

bank = BankAccount("문요준", 1000)
print(bank)