import discord
from discord.ext import commands

class Admin(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    #functions
    def is_guild_owner(): #i know its in a class but dont add "self" do it
        #seriously don't
        #this function is used for if you are the server owner and ONLY the server owner
        def predicate(ctx):
            return ctx.guild is not None and ctx.guild.owner_id == ctx.author.id
        return commands.check(predicate)
    
    #events
    @commands.Cog.listener()
    async def on_ready(self):
        print('Admin Cog Online')
        
    #commands
        #all admin commands need the 2 lines from below
        #if you dont have both, it either wont run at all
        #or ANYONE can run them!!!
        # \/\/\/\/\/\/\/\/\/\/\/
    @commands.command(aliases = ["k"])
    @commands.has_permissions(administrator = True)
    async def shutdown(self,ctx):
        await ctx.send("shutting down")
        await self.bot.change_presence(status = discord.Status.offline)
        await self.bot.close() #this command TURNS OFF the bot. Completely    

    @commands.command()
    @commands.has_permissions(administrator = True)
    async def am_i_admin(self,ctx):
         await ctx.send("You are an admin!")

    @commands.command()
    @commands.has_permissions(administrator = True)
    async def load(self, ctx, extension):
        #this command allows Admins to turn on extensions that aren't turned on
        self.bot.load_extension(f'cogs.{extension}')

    @commands.command() 
    @commands.has_permissions(administrator = True)
    async def unload(self, ctx, extension):
        #this command allows Admins to turn OFF extensions
        if extension != "Admin": #dont let ANYONE unload admin commands
            self.bot.unload_extension(f'cogs.{extension}')
        else:
            await ctx.send("you can't unload admin permissions!")

def setup(bot):
    bot.add_cog(Admin(bot))
