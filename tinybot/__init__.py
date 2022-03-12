from .user import User
from .func import Func

address = User.address
private_key = User.private_key
tiny_client = User.tiny_client

wallet_balance =  Func.wallet_balance
chain_quote = Func.chain_quote
remove_duplicates = Func.remove_duplicates
load_pickle = Func.load_pickle
save_pickle = Func.save_pickle
transact =  Func.transact