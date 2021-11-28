from crypto.configuration.network import set_network
from crypto.identity.address import address_from_passphrase
from crypto.networks.devnet import Devnet
from crypto.transactions.builder.transfer import Transfer

class Crypto:
    # TODO: init crypto class with network type

    def createTransfer(self, recipient, amount, nonce, passphrase, second_passphrase):
        """ Create a transfer transaction (devnet only) """
        set_network(Devnet)

        transaction = Transfer(
            recipientId=recipient,
            amount=amount * 100000000,
            vendorField=f"Faucet - enjoy your {amount} DARK"
        )
        transaction.set_type_group(1)
        transaction.set_nonce(nonce)
        transaction.schnorr_sign(passphrase)
        if (second_passphrase):
            transaction.second_sign(second_passphrase)

        return transaction

    def addressFromPassphrase(self, passphrase):
        """ Generate the address belonging to a given passphrase """
        return address_from_passphrase(passphrase)
