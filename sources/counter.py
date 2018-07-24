class Counter:
    def __init__(self):
        self.a=0

    def __iter__(self):
        return self


    def __next__(self):
        self.a=self.a+1
        if self.a > 10:
            raise StopIteration
        return self.a
    def __getitem__(self,n):
        for item in range(n):
            self.a=self.a+1
        return self.a
    def __call__(self):
        print('hello,my name is Counter')


x=Counter()
x()