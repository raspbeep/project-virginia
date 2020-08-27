import requests
import json


class P1:
    @staticmethod
    def pay(amount: str, currency: str, merchant=None) -> int:
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json',
        }

        data = {"amount": amount, "currency": currency}

        response = requests.post('https://pythonweekend-ke.herokuapp.com/v1/charge', headers=headers, data=json.dumps(data))

        return response.status_code


class P2:
    @staticmethod
    def pay(amount: str, currency: str, merchant: str) -> int:

        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json',
        }
        try:
            amount = eval(amount)*100
            data = {"merchant": merchant, "amount_of_money": {"amount": amount, "currency": currency}}
            response = requests.post('https://pythonweekend-ke.herokuapp.com/v2/authorize', headers=headers, data=json.dumps(data))
            data = {"payment_reference": response.json()['payment_reference']}
            response = requests.post('https://pythonweekend-ke.herokuapp.com/v2/capture', headers=headers, data=json.dumps(data))

            return response.status_code

        except NameError:
            return 69


class P3:
    @staticmethod
    def pay(amount: str, currency: str, mechant=None) -> int:

        # implements currency code as defined in ISO-4217
        try:
            int(currency)
            with open("country_codes.csv", "r") as f:
                country_codes = {}
                for i in f.readlines():
                    i = i.strip().split(",")
                    country_codes[i[1]] = i[0]

                currency = country_codes[currency]

        except ValueError:
            pass

        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json',
        }
        data = {"amount": amount, "currency": currency}
        response = requests.post('https://pythonweekend-ke.herokuapp.com/v3/authorize', headers=headers, data=json.dumps(data))

        if 'payment_id' in response.json():
            payment_id = response.json()['payment_id']
            headers = {
                'accept': 'application/json',
            }

            response = requests.post(f'https://pythonweekend-ke.herokuapp.com/v3/capture/{payment_id}', headers=headers)

            return response.json()['status']

        else:
            print(400)
