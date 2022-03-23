class Users():
    def __init__(self,id_AI,full_name,password,real_id):
        self.id_AI=id_AI
        self.full_name=full_name
        self.password=password
        self.real_id=real_id
    def __str__(self):
        return f'User: { self.full_name} real id = {self.real_id} '