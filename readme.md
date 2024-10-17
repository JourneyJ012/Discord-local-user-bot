# A simple Discord User bot you can run for yourself, that can access a few APIs and AIs.

## Setup
Clone this repo and cd in.
run `pip install - r requirements.txt`
Load .env with your OpenAI API key and your Discord API key.
On line 110 of main.py, configure the user IDs for OpenAI access. This is to stop random users from abusing your API key by adding your bot to their account.
On 151-160 and line 231, configure which LLMs you wish to use for the commands. It is recommended to use the ones provided, as they provide a great VRAM to quality ratio.