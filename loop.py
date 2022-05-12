import eth_obsidian as eth
from nice_print import yellow_print
from threading import Thread


blocks_created = 0
check_count = 0
latest_block_found = ""
while(blocks_created < 250):
    block = eth.get_latest_block()
    check_count += 1

    if(len(eth.transaction_queue)> 0):
        thread = Thread(target = eth.construct_transaction_file(block))
        thread.start()
        thread.join()

    if(block.number != latest_block_found):
        eth.construct_block_file(block)

        blocks_created += 1
        check_count = 0
    else:
        yellow_print(f"{check_count} No New Blocks | Current Count: {block.number} | Transaction Queue: {len(eth.transaction_queue)}")
    latest_block_found = block.number

