# spelling
A small tool to practice spelling

The code has been shamelessly copied from https://gist.github.com/jeffgrover/8761544be4e8025f2a67b629d7f481dc and then adapted to my needs.

The lists of words `short_words`, `medium_words` and `long_words` have been extracted from https://en.wiktionary.org/wiki/Wiktionary:Frequency_lists/English/Wikipedia_(2016).

The list of words `bee_list_words` is from the list of 2025 words from an Irish schools.

## Making it work

On Linux, the script uses [gtss](https://gtts.readthedocs.io/en/latest/cli.html) for a nice text to speech (unfortunately this requires an internet connexion and there can be some delay) and [mpg123](https://www.mpg123.de/) to play the result. 

On Debian, this is easily installed with:

```
apt-get install python3-gtss mpg123
```

Alternatively, you can switch to another text-to-speech tool by modifying `say.sh` or the method `say` in `spelling.py`. Typically `spd-say` is a good alternative which doesn't require a connexion. If you know of a high quality TTS solution which runs locally, please tell me (open an issue).
