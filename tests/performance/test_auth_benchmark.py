import timeit
from src.core.base.core.AuthCore import AuthCore




def benchmark_auth():
    core = AuthCore()
    agent_id = "agent_007"
    secret = "super_secret_key_value_12345"

    # Measure generate_challenge
    def run_gen_challenge():
        core.generate_challenge(agent_id)






    t_challenge = timeit.timeit(run_gen_challenge, number=100000)
    print(f"generate_challenge: {t_challenge/100000 * 1_000_000:.4f} μs per call")

    # Measure generate_proof




    challenge = core.generate_challenge(agent_id)
    def run_gen_proof():
        core.generate_proof(challenge, secret)

    t_proof = timeit.timeit(run_gen_proof, number=100000)


    print(f"generate_proof: {t_proof/100000 * 1_000_000:.4f} μs per call")

    # Measure verify_proof
    proof = core.generate_proof(challenge, secret)
    def run_verify():



        core.verify_proof(challenge, proof, secret)

    t_verify = timeit.timeit(run_verify, number=100000)
    print(f"verify_proof: {t_verify/100000 * 1_000_000:.4f} μs per call")





if __name__ == "__main__":
    benchmark_auth()
