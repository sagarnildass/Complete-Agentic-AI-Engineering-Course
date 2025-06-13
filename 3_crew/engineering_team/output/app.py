import gradio as gr
from accounts import Account, get_share_price

account = Account(account_id="user123")

def deposit_funds(amount):
    try:
        account.deposit(float(amount))
        return f"Deposited: ${amount}. New Balance: ${account.balance:.2f}"
    except ValueError as e:
        return str(e)

def withdraw_funds(amount):
    if account.withdraw(float(amount)):
        return f"Withdrew: ${amount}. New Balance: ${account.balance:.2f}"
    else:
        return "Insufficient funds for withdrawal."

def buy_shares(symbol, quantity):
    if account.buy_shares(symbol, int(quantity), get_share_price):
        return f"Bought {quantity} of {symbol}. Holdings: {account.get_holdings()}"
    else:
        return "Insufficient funds or invalid transaction."

def sell_shares(symbol, quantity):
    if account.sell_shares(symbol, int(quantity), get_share_price):
        return f"Sold {quantity} of {symbol}. Holdings: {account.get_holdings()}"
    else:
        return "Invalid transaction or insufficient shares."

def portfolio_value():
    return f"Portfolio Value: ${account.get_portfolio_value(get_share_price):.2f}"

def profit_loss():
    return f"Profit/Loss: ${account.get_profit_or_loss(get_share_price):.2f}"

def transaction_history():
    return "\n".join([f"{t['date']}: {t['type']} ${t['amount']} {t.get('symbol', '')} x {t.get('quantity', '')}" for t in account.get_transactions()])

with gr.Blocks() as demo:
    gr.Markdown("# Account Management System")
    
    with gr.Row():
        amount_input = gr.Number(label="Amount", precision=2)
        deposit_button = gr.Button("Deposit")
        withdraw_button = gr.Button("Withdraw")
    
    deposit_output = gr.Textbox(label="Deposit Result", interactive=False)
    withdraw_output = gr.Textbox(label="Withdraw Result", interactive=False)

    deposit_button.click(deposit_funds, inputs=amount_input, outputs=deposit_output)
    withdraw_button.click(withdraw_funds, inputs=amount_input, outputs=withdraw_output)
    
    with gr.Row():
        symbol_input = gr.Textbox(label="Share Symbol (AAPL, TSLA, GOOGL)")
        quantity_input = gr.Number(label="Quantity", precision=0)
        buy_button = gr.Button("Buy Shares")
        sell_button = gr.Button("Sell Shares")
    
    buy_output = gr.Textbox(label="Buy Result", interactive=False)
    sell_output = gr.Textbox(label="Sell Result", interactive=False)

    buy_button.click(buy_shares, inputs=[symbol_input, quantity_input], outputs=buy_output)
    sell_button.click(sell_shares, inputs=[symbol_input, quantity_input], outputs=sell_output)

    with gr.Row():
        value_button = gr.Button("Get Portfolio Value")
        pl_button = gr.Button("Get Profit/Loss")
        trans_button = gr.Button("Get Transaction History")

    value_output = gr.Textbox(label="Portfolio Value", interactive=False)
    pl_output = gr.Textbox(label="Profit/Loss", interactive=False)
    trans_output = gr.Textbox(label="Transaction History", interactive=False)

    value_button.click(portfolio_value, outputs=value_output)
    pl_button.click(profit_loss, outputs=pl_output)
    trans_button.click(transaction_history, outputs=trans_output)

demo.launch()