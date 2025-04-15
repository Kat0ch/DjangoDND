def test(**kwargs):
    for arg in kwargs:
        print(kwargs[arg])


test(**{'name': 'Max', 'last_name': 'Efim'})
