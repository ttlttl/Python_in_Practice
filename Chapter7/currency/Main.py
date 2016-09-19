import os
import sys
import urllib
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as messagebox
Spinbox = ttk.Spinbox if hasattr(ttk, "Spinbox") else tk.Spinbox
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),
        "..")))
import Rates
import Utils


class Window(ttk.Frame):

    def __init__(self, master=None):
        super().__init__(master, padding=2)
        self.create_variables()
        self.create_widgets()
        self.create_layout()
        self.create_bindings()
        self.currencyFromCombobox.focus()
        self.after(5, self.get_rates)


    #输入变量
    def create_variables(self):
        self.currencyFrom = tk.StringVar()
        self.currencyTo = tk.StringVar()
        self.amount = tk.StringVar()
        self.rates = {}

    def create_widgets(self):
        self.currencyFromCombobox = ttk.Combobox(self, textvariable=self.currencyFrom)
        self.currencyToCombobox = ttk.Combobox(self, textvariable=self.currencyTo)
        self.amountSpinbox = Spinbox(self, textvariable=self.amount, from_=1.0,
                                     to=1e6, validate="all", format="%0.2f", width=8)
        self.amountSpinbox.config(validatecommand=(self.amountSpinbox.register(self.validate), "%P"))
        self.resultLabel = ttk.Label(self)

    def validate(self, number):
        return Utils.validate_spinbox_float(self.amountSpinbox, number)

    def create_layout(self):
        padWE = dict(sticky=(tk.W, tk.E), padx="0.5m", pady="0.5m")
        self.currencyFromCombobox.grid(row=0, column=0, **padWE)
        self.amountSpinbox.grid(row=0, column=1, **padWE)
        self.currencyToCombobox.grid(row=1, column=0, **padWE)
        self.resultLabel.grid(row=1, column=1, **padWE)
        self.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        self.columnconfigure(0, weight=2)
        self.columnconfigure(1, weight=1)
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.master.minsize(150, 40)

    #双括号绑定虚拟事件，单括号绑定真实事件
    def create_bindings(self):
        self.currencyFromCombobox.bind("<<ComboboxSelected>>", self.calculate)
        self.currencyToCombobox.bind("<<ComboboxSelected>>", self.calculate)
        self.amountSpinbox.bind("<Return>", self.calculate)
        self.master.bind("<Escape>", lambda event:self.quit())

    def calculate(self, event=None):
        fromCurrency = self.currencyFrom.get()
        toCurrency = self.currencyTo.get()
        amount = self.amount.get()
        if fromCurrency and toCurrency and amount:
            amount = ((self.rates[fromCurrency] / self.rates[toCurrency]) * float(amount))
            self.resultLabel.config(text="{:,.2f}".format(amount))

    def get_rates(self):
        try:
            self.rates = Rates.get()
            self.populate_comboboxes()
        except urllib.error.URLError as err:
            messagebox.showerror("Currency \u2014 Error", str(err), parent=self)
            self.quit()

    #用下载的数据填充combobox
    def populate_comboboxes(self):
        currencies = sorted(self.rates.keys())
        for combobox in (self.currencyFromCombobox, self.currencyToCombobox):
            combobox.state(("readonly",))
            combobox.config(values=currencies)
        Utils.set_combobox_item(self.currencyFromCombobox, "USD", True)
        Utils.set_combobox_item(self.currencyToCombobox, "CNY", True)
        self.calculate()


if __name__ == "__main__":
    if sys.stdout.isatty():
        application = tk.Tk()
        application.title("Window")
        Window(application)
        application.mainloop()
    else:
        print("Loaded OK")

