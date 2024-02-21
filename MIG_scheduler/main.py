
from algorithm import create_allotments_family
from inputs import generate_tasks
from pprint import pprint
import random


def main():
    n, times, instance_sizes = generate_tasks()
    random.shuffle(times)
    create_allotments_family(times, instance_sizes)
    # print("Times GPC superlinear:")
    # pprint(times_GPC_superlinear)
    # print()
    # print("Times GPC linear:")
    # pprint(times_GPC_linear)
    # print()
    # print("Times GPC sublinear:")
    # pprint(times_GPC_sublinear)
    # times = times_GPC_superlinear + times_GPC_linear + times_GPC_sublinear
    # random.shuffle(times)
    # pprint(times_GPC_superlinear)
    # create_allotments_family(times_GPC_superlinear)


if __name__ == "__main__":
    main()