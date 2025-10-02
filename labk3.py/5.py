class Account:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance
    
    def deposit(self, amount):
        self.balance += amount
    
    def withdraw(self, amount):
        if amount <= self.balance:
            self.balance -= amount
            return True
        else:
            return False

# Example
acc = Account("John", 100)
acc.deposit(50)
acc.withdraw(30)
print(acc.balance) 
acc.withdraw(200)   
print(acc.balance)  