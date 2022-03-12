from algosdk import mnemonic
from tinyman.v1.client import TinymanMainnetClient
import os
from dotenv import load_dotenv



#Creating Tinyman client object 
class User:
    def __init__(self) -> None:
        pass

    def load_env_key(environment_key):
        load_dotenv()
        env_key = os.getenv(environment_key)
        return env_key
    
    def private_key(mnemonic_phrase):
        try:
            key = User.load_env_key(mnemonic_phrase)
            private_key = mnemonic.to_private_key(key)
        except:
            private_key = mnemonic.to_private_key(mnemonic_phrase)
        return private_key

    def address(mnemonic_phrase):
        try:
            key = User.load_env_key(mnemonic_phrase)
            public_address = mnemonic.to_public_key(key)
        except:
            public_address = mnemonic.to_public_key(mnemonic_phrase)
        return public_address

    def tiny_client(mnemonic_phrase):
        public_address = User.address(mnemonic_phrase)
        client = TinymanMainnetClient(user_address=public_address)
        return client

    def main():
        key = input("Enter Environment Key or Mnemonic Phrase: ")
        client = User.tiny_client(key)
        print(f'Tinyman client object created for {client.user_address}')

if __name__ == "__main__":
    User.main()

    
