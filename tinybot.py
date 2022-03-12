from tinybot import address
from tinybot import private_key
from tinybot import tiny_client
from tinybot import wallet_balance
from tinybot import chain_quote
from tinybot import remove_duplicates
from tinybot import load_pickle
from tinybot import save_pickle
from tinybot import transact
import time
from datetime import datetime


client = tiny_client('bot_key')
ALGO = client.fetch_asset(0)

p = './data/'
zero_data = p + 'zero.data'
primary_data = p + 'primary.data'
secondary_data = p + 'secondary.data'
master_data = p + 'master.data'
temp_data = p + 'temp.data'

start_time = time.time()
seconds =  1
round_num = 0
excess_pool_list = []
amount = 1_000_000
fee_per = 1.0105
loop_count = 0

while True:
    current_time = time.time()
    elapsed_time = current_time - start_time
    
    if elapsed_time > seconds:
        print("Finished iterating in: " + str(int(elapsed_time))  + " seconds")
        break
     
    else:
        round_num += 1
        range = 0
        started_algo = wallet_balance(client,ALGO)
        l0_amt = []
        l0 = []
        l1 = []
        l1_amt = []
        l2 = []
        l2_amt = []
        sl = []
        sl_amt = []
        update_nset_amt = []
        update_nset_chain = []
        outlist =[]
        outswaps = []
        primary_list =[]
        secondary_list =[]
#Loading
        try:
            zero_list = load_pickle(zero_data)
            primary_list = load_pickle(primary_data)
            secondary_list = load_pickle(secondary_data)
        except:
            pass

#Roughly 35 mins to loop over 434 items in master 
        if round_num == 2:
            list_identifier = 4
            swaplist = load_pickle(master_data)
            round_num = 0
            amount = 1_000_000 
            print(f'UPDATING {len(swaplist)} ITEMS ON MASTER')

#Which list is being iterated
        else:
            if len(zero_list) > 4:
                list_identifier = 0
                swaplist = zero_list
                print(f' ( 101% )   || 101% : {len(zero_list)} || 100% : {len(primary_list)} || 99% : {len(secondary_list)} ')
    
            elif len(primary_list) > 9 :
                list_identifier = 1
                swaplist = primary_list
                print(f' ( 100% )   || 101% : {len(zero_list)} || 100% : {len(primary_list)} || 99% : {len(secondary_list)} ')


            elif len(secondary_list) > 20 :
                list_identifier = 2
                swaplist = secondary_list
                print(f' ( 99% )   || 101% : {len(zero_list)} || 100% : {len(primary_list)} || 99% : {len(secondary_list)}')

            else:
                list_identifier = 3
                sample_size = 50
                swaplist = load_pickle(master_data)
                swaplist = sorted(swaplist, reverse = True,key = lambda last_price: last_price[0])
                swaplist = swaplist[:100]

#Adding values that we are most interested in            
        if list_identifier > 0 and len(zero_list) > 0:
            for i in zero_list:
                swaplist.append(i)
        
        elif list_identifier > 1 and len(primary_list) > 0:
            for i in primary_list:
                swaplist.append(i)

        elif list_identifier == 3 and len(secondary_list) > 0:
            for i in secondary_list:
                swaplist.append(i)
        else:
            pass
        swaplist = sorted(swaplist, reverse = True,key = lambda last_price: last_price[0])
#Assiging Variables
        while range < len(swaplist):
            ALGO = client.fetch_asset(0)
            chain =swaplist[range][1]
            chain_len = len(chain)
            zero = chain_len-chain_len
            pamt =swaplist[range][0]
            last_trade = []
            trans_pool_list= []
            trans_list = []
            tran_chain = []
            loop_count = 0
            for i in chain:
                last_trade = [ALGO(amount)]
                fee_amt = 0
#Chain loop     
                while zero < chain_len-1:
                    # try:
                    lst_trade = last_trade.pop()  
                    seq_pool = client.fetch_pool(chain[zero],chain[zero+1])
                    seq_quote = seq_pool.fetch_fixed_input_swap_quote(lst_trade, slippage=0.005)
                    wallet_amount = wallet_balance(client,chain[zero+1])
                    swap_fees = seq_quote.swap_fees
                    outamt = seq_quote.amount_out
                    trans_pool_list.append(seq_pool)
                    trans_list.append(seq_quote)
                    outamt = outamt
                    last_trade.append(outamt)
                    excess_pool_list.append(seq_pool)
    
#fee amount                      
                    if chain[zero+1] == ALGO:
                        transaction_fee =  ALGO(round(amount*fee_per,2)+(chain_len-1)*2000)
                        outlist.append(outamt)
                        outswaps.append(chain)
         

                        
                        print( outamt,pamt, transaction_fee ,chain )
                        if transaction_fee < outamt:
                        # if ALGO(1_000_000) < outamt:
                            
                            print('---------------------------------TRANSACTING---------------------------------')
                            print(range, outamt,pamt,  transaction_fee ,chain)

                            myalgo = wallet_balance(client,ALGO)
                            # bf.transactChain(chain,ALGO(amount))
                            transact(client,chain,ALGO(amount))
                            ending_algo = wallet_balance(client,ALGO)

                            print('\n','#######################' ,myalgo , ending_algo,'#######################','\n')

                            if myalgo > ending_algo:
                                fee_per = fee_per+.0005
                                print(fee_per)
                            else:
                                pass
                    zero += 1
            
            if outamt > ALGO(amount*1.014) and loop_count <30:
                loop_count += 1
                continue
            else:
                loop_count = 0
                range +=1

        new_range = 0
        save_pickle(outlist,outswaps,temp_data)
        new_list = load_pickle(temp_data)
        ending_algo = wallet_balance(client,ALGO)


        if list_identifier == 0:
            new_list =new_list + primary_list + secondary_list

        if list_identifier == 1:
            new_list =new_list  + secondary_list

#updating the main list every x rounds
        if list_identifier == 4:
            save_pickle(outlist,outswaps,master_data)

 
 
#Sorting & Apending New List
        while new_range < len(new_list):
            prev_amt = new_list[new_range][0]
            chain = new_list[new_range][1]

            # if prev_amt > ALGO(amount*.98):
            #     sl_amt.append(prev_amt)
            #     sl.append(chain)

            if prev_amt > ALGO(amount*1.01):
                l0_amt.append(prev_amt)
                l0.append(chain)

            elif prev_amt > ALGO(amount):
                l1_amt.append(prev_amt)
                l1.append(chain)

            elif prev_amt > ALGO(amount*.99) :
                l2_amt.append(prev_amt)
                l2.append(chain)


            else:
                pass
            new_range += 1
            save_pickle(l0_amt,l0,zero_data)
            save_pickle(l1_amt,l1,primary_data)
            save_pickle(l2_amt,l2,secondary_data)


            
        print(datetime.now() ,'---Round---', round_num, '++++++++++++++++++++++++++++++++++',  started_algo, ending_algo,'++++++++++++++++++++++++++++++++++','\n')
