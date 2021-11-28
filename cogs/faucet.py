import discord
import os

from discord.ext import commands

from libs.API import API
from libs.crypto import Crypto
from libs.utils import reset_if_not_on_cooldown


class Faucet(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.api = API()
        self.crypto = Crypto()

    @commands.command(cooldown_after_parsing=True, usage="<address>")
    @commands.cooldown(rate=1, per=604800, type=commands.BucketType.user)
    async def faucet(self, ctx, address):
        """ Get some tokens """

        if len(address) != 34:
            ctx.command.reset_cooldown(ctx)
            return await ctx.send("This does not appear to be a valid address")

        if not address.startswith(os.getenv("FAUCET_ADDRESS_PREFIX")):
            ctx.command.reset_cooldown(ctx)
            return await ctx.send("This does not look like a valid address")

        try:
            host = os.getenv("FAUCET_HOST")
            amount = int(os.getenv("FAUCET_AMOUNT"))
            currency_type = os.getenv("FAUCET_CURRENCY")
            faucet_address = self.crypto.addressFromPassphrase(os.getenv("FAUCET_PASSPHRASE"))

            response = await self.api.get(f"{host}/wallets/{faucet_address}")
            response_data = response['data']

            if int(response_data['balance']) < amount:
                return await ctx.send("Insufficient funds in the faucet, please let someone know to get it topped up")

            transaction = self.crypto.createTransfer(address, amount, int(response_data['nonce']) + 1, os.getenv("FAUCET_PASSPHRASE"), os.getenv("FAUCET_SECOND_PASSPHRASE"))
            transaction_response = await self.api.post(f"{host}/transactions", { "transactions": [transaction.to_dict()] }, { 'content-type': 'application/json'})
            transaction_response = await transaction_response.json()

            if 'error' in transaction_response:
                return await ctx.send(f"Failed sending transaction, please try again")

            await ctx.send(f"{amount} {currency_type} is on its way to {address}")
        except Exception as e:
            print(e)
            await ctx.send(f"An error occured, please try again!")


    @faucet.error
    async def prefix_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send("You forgot to provide an address for the faucet")
            reset_if_not_on_cooldown(ctx)
            return
        elif isinstance(error, commands.errors.CommandOnCooldown):
            # Do not reset cooldown in this case
            pass


    @commands.command(name='explorer')
    async def explorer(self, ctx):
        """ Return the explorer url. """
        await ctx.send('https://explorer.ark.io/')


def setup(bot):
    bot.add_cog(Faucet(bot))
