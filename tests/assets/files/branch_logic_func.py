if True:
    def hello():
        print("Hello, world!")
else:
    def hello():
        print("Hi!")

for idx in range(10):
    def goodbye():
        print(f"Goodbye #{idx}!")