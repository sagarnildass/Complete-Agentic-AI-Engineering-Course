class Account:
    def __init__(self, account_id: str):
        self.account_id = account_id
        self.balance = 0.0
        self.initial_deposit = 0.0
        self.holdings = {}
        self.transactions = []

    def deposit(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError('Deposit amount must be positive.')
        self.balance += amount
        if self.initial_deposit == 0:
            self.initial_deposit = amount
        self.record_transaction('deposit', amount)

    def withdraw(self, amount: float) -> bool:
        if amount <= 0:
            raise ValueError('Withdrawal amount must be positive.')
        if self.balance - amount < 0:
            return False
        self.balance -= amount
        self.record_transaction('withdrawal', amount)
        return True

    def buy_shares(self, symbol: str, quantity: int, get_share_price: callable) -> bool:
        if quantity <= 0:
            raise ValueError('Quantity must be positive.')
        price_per_share = get_share_price(symbol)
        total_cost = price_per_share * quantity
        if total_cost > self.balance:
            return False
        self.balance -= total_cost
        self.holdings[symbol] = self.holdings.get(symbol, 0) + quantity
        self.record_transaction('buy', total_cost, symbol, quantity)
        return True

    def sell_shares(self, symbol: str, quantity: int, get_share_price: callable) -> bool:
        if quantity <= 0:
            raise ValueError('Quantity must be positive.')
        if symbol not in self.holdings or self.holdings[symbol] < quantity:
            return False
        price_per_share = get_share_price(symbol)
        total_revenue = price_per_share * quantity
        self.balance += total_revenue
        self.holdings[symbol] -= quantity
        if self.holdings[symbol] == 0:
            del self.holdings[symbol]
        self.record_transaction('sell', total_revenue, symbol, quantity)
        return True

    def get_portfolio_value(self, get_share_price: callable) -> float:
        total_value = self.balance
        for symbol, quantity in self.holdings.items():
            total_value += get_share_price(symbol) * quantity
        return total_value

    def get_profit_or_loss(self, get_share_price: callable) -> float:
        current_value = self.get_portfolio_value(get_share_price)
        return current_value - self.initial_deposit

    def get_holdings(self) -> dict:
        return self.holdings

    def get_transactions(self) -> list:
        return self.transactions

    def record_transaction(self, type: str, amount: float, symbol: str = None, quantity: int = None) -> None:
        from datetime import datetime
        transaction = {
            'type': type,
            'amount': amount,
            'symbol': symbol,
            'quantity': quantity,
            'date': datetime.now() 
        }
        self.transactions.append(transaction)

def get_share_price(symbol):
    fixed_prices = {'AAPL': 150.0, 'TSLA': 750.0, 'GOOGL': 2800.0}
    return fixed_prices.get(symbol, 0.0)

# Example usage:
if __name__ == '__main__':
    account = Account(account_id="user123")
    account.deposit(1000.0)
    account.buy_shares('AAPL', 5, get_share_price)
    account.sell_shares('AAPL', 2, get_share_price)
    account.withdraw(100.0)
    portfolio_value = account.get_portfolio_value(get_share_price)
    profit_or_loss = account.get_profit_or_loss(get_share_price)
    holdings = account.get_holdings()
    transactions = account.get_transactions()
    print(f'Portfolio Value: {portfolio_value}')
    print(f'Profit/Loss: {profit_or_loss}')
    print(f'Holdings: {holdings}')
    print(f'Transactions: {transactions}')