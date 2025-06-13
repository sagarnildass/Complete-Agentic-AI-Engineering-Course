import unittest
from accounts import Account, get_share_price

class TestAccount(unittest.TestCase):
    def setUp(self):
        self.account = Account("user123")

    def test_initial_balance(self):
        self.assertEqual(self.account.balance, 0.0)

    def test_deposit(self):
        self.account.deposit(1000.0)
        self.assertEqual(self.account.balance, 1000.0)

    def test_deposit_negative(self):
        with self.assertRaises(ValueError):
            self.account.deposit(-500.0)

    def test_withdraw(self):
        self.account.deposit(1000.0)
        result = self.account.withdraw(500.0)
        self.assertTrue(result)
        self.assertEqual(self.account.balance, 500.0)

    def test_withdraw_exceed_balance(self):
        self.account.deposit(200.0)
        result = self.account.withdraw(300.0)
        self.assertFalse(result)

    def test_buy_shares(self):
        self.account.deposit(1000.0)
        result = self.account.buy_shares("AAPL", 5, get_share_price)
        self.assertTrue(result)
        self.assertEqual(self.account.holdings["AAPL"], 5)
        self.assertEqual(self.account.balance, 1000.0 - 5 * 150.0)

    def test_buy_shares_insufficient_funds(self):
        self.account.deposit(100.0)
        result = self.account.buy_shares("AAPL", 5, get_share_price)
        self.assertFalse(result)

    def test_sell_shares(self):
        self.account.deposit(1000.0)
        self.account.buy_shares("AAPL", 5, get_share_price)
        result = self.account.sell_shares("AAPL", 3, get_share_price)
        self.assertTrue(result)
        self.assertEqual(self.account.holdings["AAPL"], 2)

    def test_sell_shares_not_owned(self):
        result = self.account.sell_shares("AAPL", 1, get_share_price)
        self.assertFalse(result)

    def test_get_portfolio_value(self):
        self.account.deposit(1000.0)
        self.account.buy_shares("AAPL", 5, get_share_price)
        value = self.account.get_portfolio_value(get_share_price)
        self.assertEqual(value, 1000.0 + 5 * 150.0)

    def test_get_profit_or_loss(self):
        self.account.deposit(1000.0)
        self.account.buy_shares("AAPL", 5, get_share_price)
        profit_or_loss = self.account.get_profit_or_loss(get_share_price)
        self.assertEqual(profit_or_loss, (5 * 150.0 + 1000.0) - 1000.0)

    def test_get_holdings(self):
        self.account.deposit(1000.0)
        self.account.buy_shares("AAPL", 5, get_share_price)
        holdings = self.account.get_holdings()
        self.assertEqual(holdings, {"AAPL": 5})

    def test_get_transactions(self):
        self.account.deposit(1000.0)
        transactions = self.account.get_transactions()
        self.assertEqual(len(transactions), 1)

if __name__ == "__main__":
    unittest.main()