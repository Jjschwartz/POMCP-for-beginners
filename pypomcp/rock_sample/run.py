from pypomcp.pomcp import POMCP

from pypomcp.rock_sample.rock_sample_model import RockSampleModel


LINE_BREAK = "-"*60


def run_episode(M, timeout, step_limit):
    s = M.b0.sample()
    d = False
    total_reward = 0

    t = 0
    pomcp = POMCP(model)
    print("Episode Map:")
    print(M.map)
    print("\nInitial Actual state:")
    print(s)
    while not d and t < step_limit:
        a = pomcp.search(timeout)
        # pomcp.display()
        next_s, o, r, d = M.step(s, a)
        pomcp.update(a, o)
        total_reward += r
        s = next_s
        print(LINE_BREAK)
        print(f"Step={t}\na={a}\no={o}\nr={r}")
        print(s)
        t += 1
        # input()

    return total_reward, t, d


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("n", type=int)
    parser.add_argument("k", type=int)
    parser.add_argument("-s", type=float, default=0.9, help="sensor efficiency (default=0.9)")
    parser.add_argument("-t", type=float, default=1, help="search time (s) (default=1)")
    parser.add_argument("-l", type=int, default=100, help="Step limit (default=100)")
    parser.add_argument("-e", type=int, default=100, help="Number of episodes (default=100)")

    args = parser.parse_args()

    model = RockSampleModel(args.n, args.k, args.s)

    print(LINE_BREAK)
    print(f"Running {args.e} episodes")
    print(LINE_BREAK)
    ep_returns = []
    ep_lens = []
    ep_done = []
    for e in range(args.e):
        print(LINE_BREAK)
        print(f"Episode {e} Start")
        print(LINE_BREAK)
        r, t, d = run_episode(model, args.t, args.l)
        ep_returns.append(r)
        ep_lens.append(t)
        ep_done.append(int(d))
        print(LINE_BREAK)
        print(f"Episode {e} done. Reward={r}")

    print(LINE_BREAK)
    print("All done")
    print(f"Average reward = {sum(ep_returns)/args.e:.2f}")
    print(f"Average episode lengths = {sum(ep_lens)/args.e:.2f}")
    print(f"Percent complete = {sum(ep_done)/args.e * 100:.2f}")
    print()
