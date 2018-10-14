import argparse
from StateMachine.StateMachine import StateMachine


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--api_url", help="base apu url", default="http://127.0.0.1:8000/server")
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    sm = StateMachine(args.api_url)
    sm.run()
