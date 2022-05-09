FROM gorialis/discord.py:minimal

WORKDIR /

RUN pip install discord.py requests --no-cache-dir

COPY . .

CMD ["python", "bot.py"]
