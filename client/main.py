from StateMachine import StateMachine

if __name__ == '__main__':
    sm = StateMachine('http://127.0.0.1:8000/server')
    sm.run()
