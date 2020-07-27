
from Classes.Music.YTDLSource import YTDLSource

class Music():
    def get_spotify():
        pass

    def get_youtube():
         @commands.command(pass_context=True)
         async def play(self, ctx, *, url):
            print(url)
            server = ctx.message.guild
            voice_channel = server.voice_client

            async with ctx.typing():
                player = await YTDLSource.from_url(url, loop=self.bot.loop)
                ctx.voice_channel.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
            await ctx.send('Now playing: {}'.format(player.title))