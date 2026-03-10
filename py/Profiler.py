from collections import defaultdict


class Profiler:
    calls = {}
    instances = {}

    @classmethod
    def inc_call(cls, name):
        cls.calls[name] = cls.calls.get(name, 0) + 1

    @classmethod
    def inc_instance(cls, name):
        cls.instances[name] = cls.instances.get(name, 0) + 1

    @classmethod
    def report(cls):
        print("=== INSTANCES ===")
        for k, v in cls.instances.items():
            print(f"{k}: {v}")

        print("\n=== CALLS ===")
        for k, v in cls.calls.items():
            print(f"{k}: {v}")
