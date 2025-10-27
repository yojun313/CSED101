class BankAccount:
    def __init__(self, name="none", balance=0):
        self.balance = balance
        self.name = name
    
    def deposit(self, amount):
        self.balance += amount
    
    def withdraw(self, amount):
        if self.balance - amount >= 0:
            self.balance -= amount
            return True
        else:
            print("잔액 부족!")
            return False

    def get_info(self):
        print("이름: %s, 잔고: %d" % (self.name, self.balance))
           
    def transfer(self, other, amount):
        if self.withdraw(amount) == True:
            other.deposit(amount)

    def __str__(self):
        return "이름: %s, 잔고: %d" % (self.name, self.balance)
    
    def __add__(self, amount):
        self.deposit(amount)
    
    def __iadd__(self, amount):
        self.deposit(amount)
        return self
        
    def __sub__(self, amount):
        self.withdraw(amount)
        
    def __isub__(self, amount):
        self.withdraw(amount)
        return self
    
    
class MinimumBalanceAccount(BankAccount):
    def __init__(self, name="none", balance=0, min_bal = 0):
        super().__init__(name, balance)
        self.min_bal = min_bal
    
    def withdraw(self, amount):
        if self.balance-amount < self.min_bal:
            print("최소 잔액을 유지해야 합니다")
            return False
        else:
            self.balance -= amount
            return True

bank = BankAccount("ansdy", 1000)

bank -= 500
print(bank)