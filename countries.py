class Countries():
    def __init__(self,code_AI,name):
        self.code_AI=code_AI
        self.name=name
    def __str__(self):
        return f'Country: { self.code_AI}  user_id = {self.name}'