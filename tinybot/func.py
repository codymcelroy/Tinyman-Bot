from .user import User
import itertools
import pickle

class Func:
  #Asset Balance in Wallet
  def wallet_balance(client, asset, fetch=True):
    global WALLET
    if (fetch):
      WALLET = client.algod.account_info(client.user_address)
    try:
      return asset((next(
        item for item in WALLET['assets'] if item['asset-id'] == asset.id and asset.id != 0
      ) if asset.id else WALLET)['amount'])
    except:
      return asset(0)


  #Quote for a list of swaps
  def chain_quote(client, chain,index,lst_trade):
      seq_pool = client.fetch_pool(chain[index],chain[index+1])
      seq_quote = seq_pool.fetch_fixed_input_swap_quote(lst_trade, slippage=0.01)
      outamt = seq_quote.amount_out
      return outamt ,seq_pool, seq_quote


  def remove_duplicates(lst): 
      out = []
      for tup in lst:
          if [tup] not in lst:
              out.append(tup)
      clean_list = list(k for k,_ in itertools.groupby(out))
      return clean_list


  #loading pickle data to a list
  def load_pickle(workbook):
    with open(workbook, 'rb') as filehandle:
        pickle_list = pickle.load(filehandle)
        return pickle_list


  #Saving a list Pickle
  def save_pickle(outlist,outswaps,workbook):
          data_tuples = tuple(zip(outlist,outswaps))
          sorted_data = sorted(data_tuples, reverse=True,key=lambda tup:(tup[0]))
          cleaned_tup = Func.remove_duplicates(sorted_data)
          with open(workbook, 'wb') as filehandle:
              # store the data as binary data stream
              pickle.dump(cleaned_tup, filehandle)

  #Transaction
  def transact(client, tchain,algo_amt):
    t_len = len(tchain)
    tzero = 0
    ttrade = [algo_amt]
    amount = 0
    print(tchain)
    
    while tzero < t_len-1:
      tlt = ttrade.pop()  
      tpool = client.fetch_pool(tchain[tzero],tchain[tzero+1])
      tquote = tpool.fetch_fixed_input_swap_quote(tlt, slippage=0.005)
      ttransaction_group = tpool.prepare_swap_transactions_from_quote(tquote)
      ttransaction_group.sign_with_private_key(client.user_address, User.private_key)
      result = client.submit(ttransaction_group, wait=True)
      trans_pool = client.fetch_pool(tchain[tzero],tchain[tzero+1])
      print(tquote)
      excess = trans_pool.fetch_excess_amounts()
      if len(excess) >0:
        for key,value in excess.items():
          asset  = key
          amount = value
          print(f'Excess: {amount}')
          if amount > 0:
            transaction_group = trans_pool.prepare_redeem_transactions(amount)
            transaction_group.sign_with_private_key(client.user_address, User.private_key)
            result = client.submit(transaction_group, wait=True)
          else:
            pass
          try:    
            toutamt = tquote.amount_out_with_slippage + amount 
          except:
            print('Wallet Error')
            toutamt = tquote.amount_out_with_slippage
      ttrade.append(toutamt)
      tzero += 1


def main():
  print('Functions being used')

if __name__ == "__main__":
    main()
