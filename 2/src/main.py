import hashlib
import timeit

import plotly.express as px


class Assignment1:
    INPUT = 'Lorem ipsum dolor sit amet'.encode('utf-8')

    def calculate_hash(self, algorithm: str) -> str:
        h = hashlib.new(algorithm)
        h.update(self.INPUT)
        return h.hexdigest()

    def assignment(self):
        for algorithm in hashlib.algorithms_available:
            if algorithm.startswith('shake_'):
                continue

            elapsed_time = timeit.timeit(lambda: self.calculate_hash(algorithm), number=1)
            print(f'{elapsed_time:.9f} {algorithm}')


class Assignment3:
    BLOCK_SIZE = 2 ** 27  # 128 M

    def assignment(self, filename):
        with open(filename, 'rb') as f:
            hasher = hashlib.sha256()
            while buffer := f.read(self.BLOCK_SIZE):
                hasher.update(buffer)
            return hasher.hexdigest()


class Assignment4:
    INPUTS = [('\0' * (2 ** n)).encode('utf-8') for n in range(16)]

    def get_hash(self, data):
        hasher = hashlib.sha256()
        hasher.update(data)
        return hasher.hexdigest()

    def calculate(self):
        results = []

        for data in self.INPUTS:
            elapsed_time = timeit.timeit(lambda: self.get_hash(data), number=1)
            results.append({'x': elapsed_time})

        return results

    def assignment(self):
        results = self.calculate()

        fig = px.line(results, labels={
            'index': '2 ** n length',
            'value': 'time',
        })
        fig.show()


def main():
    Assignment1().assignment()

    # https://cdimage.kali.org/kali-2021.1/kali-linux-2021.1-live-amd64.iso
    filename = 'kali-linux-2021.1-live-amd64.iso'
    # sha256sum kali-linux-2021.1-live-amd64.iso
    sha256sum = '8e5af78e93424336f787d4dd0fdd89b429675d5ae67b1c1634ea1b53c5650677'

    assert Assignment3().assignment(filename) == sha256sum

    Assignment4().assignment()


if __name__ == '__main__':
    main()
