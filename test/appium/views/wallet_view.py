import logging

from views.base_view import BaseView
from views.base_element import BaseButton, BaseText


class SendButton(BaseButton):

    def __init__(self, driver):
        super(SendButton, self).__init__(driver)
        self.locator = self.Locator.xpath_selector("//*[@text='SEND']")

    def navigate(self):
        from views.send_transaction_view import SendTransactionView
        return SendTransactionView(self.driver)


class RequestButton(BaseButton):

    def __init__(self, driver):
        super(RequestButton, self).__init__(driver)
        self.locator = self.Locator.xpath_selector("//*[@text='REQUEST']")

    def navigate(self):
        from views.send_transaction_view import SendTransactionView
        return SendTransactionView(self.driver)


class SendRequestButton(BaseButton):

    def __init__(self, driver):
        super(SendRequestButton, self).__init__(driver)
        self.locator = self.Locator.xpath_selector("//*[@text='SEND REQUEST']")


class ChooseRecipientButton(BaseButton):

    def __init__(self, driver):
        super(ChooseRecipientButton, self).__init__(driver)
        self.locator = self.Locator.xpath_selector("//*[@text='Choose recipient...']")


class TransactionsButton(BaseButton):

    def __init__(self, driver):
        super(TransactionsButton, self).__init__(driver)
        self.locator = self.Locator.xpath_selector('(//android.view.ViewGroup[@content-desc="icon"])[3]')

    def navigate(self):
        from views.transactions_view import TransactionsView
        return TransactionsView(self.driver)


class ChooseFromContactsButton(BaseButton):
    def __init__(self, driver):
        super(ChooseFromContactsButton, self).__init__(driver)
        self.locator = self.Locator.xpath_selector("//*[@text='Choose From Contacts']")


class EthAssetText(BaseText):
    def __init__(self, driver):
        super(EthAssetText, self).__init__(driver)
        self.locator = self.Locator.xpath_selector("//*[@text='ETH']/../android.widget.TextView[1]")


class UsdTotalValueText(BaseText):
    def __init__(self, driver):
        super(UsdTotalValueText, self).__init__(driver)
        self.locator = self.Locator.xpath_selector("//*[@text='USD']/../android.widget.TextView[1]")


class WalletView(BaseView):
    def __init__(self, driver):
        super(WalletView, self).__init__(driver)
        self.driver = driver

        self.send_button = SendButton(self.driver)
        self.transactions_button = TransactionsButton(self.driver)
        self.eth_asset = EthAssetText(self.driver)
        self.usd_total_value = UsdTotalValueText(self.driver)
        self.request_button = RequestButton(self.driver)

        self.send_request_button = SendRequestButton(self.driver)

    def get_usd_total_value(self):
        return float(self.usd_total_value.text)

    def get_eth_value(self):
        return float(self.eth_asset.text)

    def verify_currency_balance(self, expected_rate: int, errors: list):
        usd = self.get_usd_total_value()
        eth = self.get_eth_value()
        expected_usd = round(eth * expected_rate, 2)
        percentage_diff = abs((usd - expected_usd) / ((usd + expected_usd) / 2)) * 100
        if percentage_diff > 2:
            errors.append('Difference between current (%s) and expected (%s) USD balance > 2%%!!' % (usd, expected_usd))
        else:
            logging.info('Current USD balance %s is ok' % usd)
