"""Small command-line demo for the final project."""
from APP.pipeline import BadmintonCoach
import json


def main():
    coach = BadmintonCoach(top_k=3)
    print('Badminton AI Coach. Type a problem, or q to quit.')
    while True:
        q = input('\nProblem: ').strip()
        if q.lower() in {'q', 'quit', 'exit'}:
            break
        out = coach.run(q)
        print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
