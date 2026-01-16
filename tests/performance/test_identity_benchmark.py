import timeit
from src.core.base.core.IdentityCore import IdentityCore


def benchmark_identity():
    core = IdentityCore()
    pub_key = "public_key_abcdef123456"
    meta = {"type": "worker", "birth_cycle": 42}
    payload = "payload_content_for_signing_simulation"

    # Measure generate_agent_id
    def run_gen_id():
        core.generate_agent_id(pub_key, meta)

    t_id = timeit.timeit(run_gen_id, number=100000)
    print(f"generate_agent_id: {t_id / 100000 * 1_000_000:.4f} μs per call")

    # Measure sign_payload
    def run_sign():
        core.sign_payload(payload, pub_key)

    t_sign = timeit.timeit(run_sign, number=100000)

    print(f"sign_payload: {t_sign / 100000 * 1_000_000:.4f} μs per call")

    # Measure verify_signature
    sig = core.sign_payload(payload, pub_key)

    def run_verify():
        core.verify_signature(payload, sig, pub_key)

    t_verify = timeit.timeit(run_verify, number=100000)
    print(f"verify_signature: {t_verify / 100000 * 1_000_000:.4f} μs per call")


if __name__ == "__main__":
    benchmark_identity()
