# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\ai_eng.py\feathr_project.py\feathr.py\secrets.py\akv_client_2682282be421.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\ai-eng\feathr_project\feathr\secrets\akv_client.py

from azure.core.exceptions import ResourceNotFoundError

from azure.identity import DefaultAzureCredential

from azure.keyvault.secrets import SecretClient

from loguru import logger

class AzureKeyVaultClient:

    def __init__(self, akv_name: str):

        self.akv_name = akv_name

        self.secret_client = None

    def get_feathr_akv_secret(self, secret_name: str):

        """Get Feathr Secrets from Azure Key Vault. Note that this function will replace '_' in `secret_name` with '-' since Azure Key Vault doesn't support it

        Returns:

            _type_: _description_

        """

        if self.secret_client is None:

            self.secret_client = SecretClient(

                vault_url=f"https://{self.akv_name}.vault.azure.net",

                credential=DefaultAzureCredential(),

            )

        try:

            # replace '_' with '-' since Azure Key Vault doesn't support it

            variable_replaced = secret_name.replace("_", "-")  # .upper()

            logger.info(

                "Fetching the secret {} from Key Vault {}.",

                variable_replaced,

                self.akv_name,

            )

            secret = self.secret_client.get_secret(variable_replaced)

            logger.info(

                "Secret {} fetched from Key Vault {}.", variable_replaced, self.akv_name

            )

            return secret.value

        except ResourceNotFoundError as e:

            logger.error(

                f"Secret {secret_name} cannot be found in Key Vault {self.akv_name}."

            )

            raise

