
import timeit
from src.logic.agents.security.core.PrivacyCore import PrivacyCore




def benchmark_privacy():
    # Setup data










    clean_text = "This is a clean sentence with no PI." * 10

    email_text = "Email me at test@example.com or support@company.org." * 5






    mixed_text = """
    User: john.doe
    Email: john@doe.com
    IP: 192.168.0.1
    Key: secret_key="ABCDEFGHIJKLMNOPQRSTUVWXYZ123456"


    """ * 20

    t_clean = timeit.timeit(lambda: PrivacyCore.redact_text(clean_text), number=1000)
    t_email = timeit.timeit(lambda: PrivacyCore.redact_text(email_text), number=1000)
    t_mixed = timeit.timeit(lambda: PrivacyCore.redact_text(mixed_text), number=1000)





    print(f"Redact Clean (1000 calls): {t_clean/1000 * 1e6:.2f} us")
    print(f"Redact Email (1000 calls): {t_email/1000 * 1e6:.2f} us")
    print(f"Redact Mixed (1000 calls): {t_mixed/1000 * 1e6:.2f} us")





if __name__ == "__main__":
    benchmark_privacy()
