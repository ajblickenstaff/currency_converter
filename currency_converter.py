import tkinter as tk
from tkinter import ttk
from forex_python.converter import CurrencyRates, CurrencyCodes, RatesNotAvailableError

class CurrencyConverter:
    def __init__(self):
        self.currency_rate = CurrencyRates()
        self.currency_code = CurrencyCodes()
        
    def convert_currency(self, amount: float, from_currency: str, to_currency: str) -> float:
        rate = self.currency_rate.get_rate(from_currency, to_currency)
        converted_amount = amount * rate
        return converted_amount
        
    def get_symbol(self, currency: str) -> str:
        return self.currency_code.get_symbol(currency)

class CurrencyConverterGUI:
    def __init__(self, converter: CurrencyConverter):
        self.converter = converter
        self.root = tk.Tk()
        self.root.title("Currency Converter")
        self.create_widgets()
        self.root.mainloop()

    def create_widgets(self):
        input_frame = ttk.Frame(self.root, padding=10)
        input_frame.grid(row=0, column=0, sticky=tk.W)

        self.amount_var = tk.DoubleVar()
        amount_label = ttk.Label(input_frame, text="Amount:")
        amount_label.grid(row=0, column=0, sticky=tk.W)
        amount_entry = ttk.Entry(input_frame, textvariable=self.amount_var)
        amount_entry.grid(row=0, column=1, sticky=tk.W)

        self.from_currency_var = tk.StringVar()
        from_currency_label = ttk.Label(input_frame, text="From Currency:")
        from_currency_label.grid(row=1, column=0, sticky=tk.W)
        currency_list = sorted(list(self.converter.currency_rate.get_rates('USD').keys()))
        currency_list.append('USD')
        currency_list.sort()
        from_currency_dropdown = ttk.Combobox(input_frame, textvariable=self.from_currency_var, values=currency_list, state="readonly")
        from_currency_dropdown.grid(row=1, column=1, sticky=tk.W)

        self.to_currency_var = tk.StringVar()
        to_currency_label = ttk.Label(input_frame, text="To Currency:")
        to_currency_label.grid(row=2, column=0, sticky=tk.W)
        to_currency_dropdown = ttk.Combobox(input_frame, textvariable=self.to_currency_var, values=currency_list, state="readonly")
        to_currency_dropdown.grid(row=2, column=1, sticky=tk.W)

        convert_button = ttk.Button(input_frame, text="Convert", command=self.convert)
        convert_button.grid(row=3, column=0, columnspan=2, pady=10)

        self.output_frame = ttk.Frame(self.root, padding=10)
        
        self.result_var = tk.StringVar()
        result_label = ttk.Label(self.output_frame, text="Result:")
        result_label.grid(row=0, column=0, sticky=tk.W)
        result_value = ttk.Label(self.output_frame, textvariable=self.result_var)
        result_value.grid(row=0, column=1, sticky=tk.W)

    def convert(self):
        amount = self.amount_var.get()
        from_currency = self.from_currency_var.get().upper()
        to_currency = self.to_currency_var.get().upper()

        if not from_currency or not to_currency or amount == 0:
            self.result_var.set("Please provide valid input values.")
            return

        try:
            result = self.converter.convert_currency(amount, from_currency, to_currency)
            symbol = self.converter.get_symbol(to_currency)
            self.result_var.set(f"{symbol}{result:.2f}")

            self.output_frame.grid(row=4, column=0, sticky=tk.W)
            self.root.geometry("")

        except (ValueError, RatesNotAvailableError) as e:
            self.result_var.set("An unexpected error occurred.")


if __name__ == '__main__':
    currency_converter = CurrencyConverter()
    CurrencyConverterGUI(currency_converter)
