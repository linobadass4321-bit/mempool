#!/usr/bin/env python3
"""
Leiva-L1: Educational Layer-1 Blockchain Architecture
Lead Architect: Jose Catalino Leiva Jr
Consensus Engine: Proof-of-Work (PoW)
Cryptographic Primitive: SHA-256
"""

import hashlib
import json
import time
from datetime import datetime
from typing import List, Dict, Any


class Transaction:
    """Represents a single transaction in the blockchain"""
    
    def __init__(self, sender: str, receiver: str, amount: float):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.timestamp = datetime.now().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "sender": self.sender,
            "receiver": self.receiver,
            "amount": self.amount,
            "timestamp": self.timestamp
        }


class Block:
    """Represents a single block in the blockchain"""
    
    def __init__(self, index: int, transactions: List[Transaction], previous_hash: str, difficulty: int = 4):
        self.index = index
        self.timestamp = datetime.now().isoformat()
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.difficulty = difficulty
        self.nonce = 0
        self.hash = self.mine_block()
    
    def calculate_hash(self) -> str:
        """Calculate SHA-256 hash of the block"""
        block_data = {
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": [tx.to_dict() for tx in self.transactions],
            "previous_hash": self.previous_hash,
            "nonce": self.nonce
        }
        block_string = json.dumps(block_data, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def mine_block(self) -> str:
        """Mine the block using Proof-of-Work"""
        target = "0" * self.difficulty
        attempt = 0
        
        print(f"\n[Mining] Block #{self.index} mining started by Jose Catalino Leiva Jr...")
        print(f"[Target] Finding hash with {self.difficulty} leading zeros...\n")
        
        start_time = time.time()
        
        while True:
            self.hash = self.calculate_hash()
            attempt += 1
            
            # Display progress every 100,000 attempts
            if attempt % 100000 == 0:
                elapsed = time.time() - start_time
                rate = attempt / elapsed if elapsed > 0 else 0
                print(f"[Mining Block #{self.index}] Attempt: {attempt:,} | Hash Rate: {rate:,.0f} h/s | Current Hash: {self.hash[:16]}...")
            
            if self.hash.startswith(target):
                elapsed = time.time() - start_time
                print(f"\n[Success] Block #{self.index} successfully mined!")
                print(f"[Stats] Attempts: {attempt:,} | Time: {elapsed:.2f}s | Nonce: {self.nonce}\n")
                return self.hash
            
            self.nonce += 1
    
    def display_block(self):
        """Display block information in tree format"""
        hash_short = self.hash[:16] + "..."
        prev_hash_short = self.previous_hash[:16] + "..." if self.previous_hash != "0" else "GENESIS"
        
        print(f"Block #{self.index}")
        print(f"├─ Index: {self.index}")
        print(f"├─ Timestamp: {self.timestamp}")
        print(f"├─ Transactions: {len(self.transactions)}")
        print(f"├─ Previous Hash: {prev_hash_short}")
        print(f"├─ Hash: {hash_short}")
        print(f"└─ Nonce: {self.nonce}")
        print()


class Blockchain:
    """Main blockchain class for Leiva-L1"""
    
    def __init__(self, founder: str = "Jose Catalino Leiva Jr", difficulty: int = 4):
        self.chain: List[Block] = []
        self.pending_transactions: List[Transaction] = []
        self.founder = founder
        self.difficulty = difficulty
        self.mining_reward = 10
        
        print("\n" + "="*60)
        print("  LEIVA-L1: EDUCATIONAL LAYER-1 BLOCKCHAIN")
        print("="*60)
        print(f"Founder Signature: {self.founder}")
        print(f"Genesis Hash: 0000abc123... [Mining] Block #0 mining started...")
        print("="*60 + "\n")
        
        # Create genesis block
        self.create_genesis_block()
    
    def create_genesis_block(self):
        """Create the first block in the blockchain"""
        genesis_block = Block(0, [], "0", self.difficulty)
        self.chain.append(genesis_block)
    
    def get_latest_block(self) -> Block:
        """Get the most recent block in the chain"""
        return self.chain[-1]
    
    def add_transaction(self, transaction: Transaction) -> bool:
        """Add a transaction to pending transactions"""
        self.pending_transactions.append(transaction)
        return True
    
    def mine_pending_transactions(self, miner_address: str) -> Block:
        """Mine pending transactions and add reward"""
        # Add mining reward transaction
        reward_tx = Transaction("SYSTEM", miner_address, self.mining_reward)
        self.pending_transactions.append(reward_tx)
        
        # Create and add new block
        new_block = Block(
            len(self.chain),
            self.pending_transactions,
            self.get_latest_block().hash,
            self.difficulty
        )
        
        self.chain.append(new_block)
        self.pending_transactions = []
        
        return new_block
    
    def is_chain_valid(self) -> bool:
        """Validate the entire blockchain"""
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            
            # Verify current block's hash
            if current_block.hash != current_block.calculate_hash():
                return False
            
            # Verify link to previous block
            if current_block.previous_hash != previous_block.hash:
                return False
            
            # Verify proof-of-work
            if not current_block.hash.startswith("0" * self.difficulty):
                return False
        
        return True
    
    def display_chain(self):
        """Display the entire blockchain in visual format"""
        print("\n" + "="*60)
        print("  BLOCKCHAIN CHAIN VISUALIZATION")
        print("="*60 + "\n")
        
        # Display blocks in tree format
        for block in self.chain:
            block.display_block()
        
        # Display chain link visualization
        print("\n" + "-"*60)
        print("CHAIN LINK VISUALIZATION:")
        print("-"*60 + "\n")
        
        chain_viz = ""
        for i, block in enumerate(self.chain):
            hash_short = block.hash[:8]
            chain_viz += f"[Block #{block.index}]\nHash: {hash_short}"
            
            if i < len(self.chain) - 1:
                chain_viz += "\n    ↓\n    ↓\n"
        
        print(chain_viz)
        print("\n")
    
    def get_balance(self, address: str) -> float:
        """Calculate balance for a given address"""
        balance = 0
        
        for block in self.chain:
            for tx in block.transactions:
                if tx.sender == address:
                    balance -= tx.amount
                if tx.receiver == address:
                    balance += tx.amount
        
        return balance
    
    def validate_and_report(self):
        """Validate blockchain and display report"""
        is_valid = self.is_chain_valid()
        
        print("\n" + "="*60)
        print("  BLOCKCHAIN VALIDATION REPORT")
        print("="*60)
        print(f"Is the ledger secure and valid? {is_valid}")
        print(f"Total Blocks: {len(self.chain)}")
        print(f"Total Transactions: {sum(len(block.transactions) for block in self.chain)}")
        print(f"Difficulty Level: {self.difficulty} leading zeros")
        print("="*60 + "\n")
        
        return is_valid


# ============================================================================
# MAIN EXECUTION - Educational Demonstration
# ============================================================================

if __name__ == "__main__":
    # Initialize blockchain
    blockchain = Blockchain(founder="Jose Catalino Leiva Jr", difficulty=4)
    
    # Create sample transactions
    tx1 = Transaction("Alice", "Bob", 50)
    tx2 = Transaction("Bob", "Charlie", 25)
    tx3 = Transaction("Charlie", "Alice", 10)
    tx4 = Transaction("Alice", "David", 15)
    tx5 = Transaction("David", "Bob", 20)
    
    # Mine Block #1
    print("\n--- Processing Transaction Block 1 ---")
    blockchain.add_transaction(tx1)
    blockchain.add_transaction(tx2)
    blockchain.add_transaction(tx3)
    block1 = blockchain.mine_pending_transactions("Miner1")
    
    # Mine Block #2
    print("\n--- Processing Transaction Block 2 ---")
    blockchain.add_transaction(tx4)
    blockchain.add_transaction(tx5)
    block2 = blockchain.mine_pending_transactions("Miner2")
    
    # Display blockchain
    blockchain.display_chain()
    
    # Validate and report
    blockchain.validate_and_report()
    
    # Display account balances
    print("ACCOUNT BALANCES:")
    print("-"*60)
    for address in ["Alice", "Bob", "Charlie", "David", "Miner1", "Miner2"]:
        balance = blockchain.get_balance(address)
        print(f"{address}: {balance} LEI")
    print("-"*60 + "\n")
