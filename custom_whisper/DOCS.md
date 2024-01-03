# Home Assistant Add-on: Whisper

## Installation

Follow these steps to get the add-on installed on your system:

1. Navigate in your Home Assistant frontend to **Settings** -> **Add-ons** -> **Add-on store**.
2. Find the "Whisper" add-on and click it.
3. Click on the "INSTALL" button.

## How to use

After this add-on is installed and running, it will be automatically discovered
by the Wyoming integration in Home Assistant. To finish the setup,
click the following my button:

[![Open your Home Assistant instance and start setting up a new integration.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=wyoming)

Alternatively, you can install the Wyoming integration manually, see the
[Wyoming integration documentation](https://www.home-assistant.io/integrations/wyoming/)
for more information.

## Configuration

### Option: `language`

Default language for the add-on. In Home Assist 2023.8+, multiple languages can be used simultaneously by different [Assist pipelines](https://www.home-assistant.io/voice_control/voice_remote_local_assistant/).

If you select "auto", the model will run **much** slower but will auto-detect the spoken language.

[Performance of supported languages](https://github.com/openai/whisper#available-models-and-languages)

[List of two-letter language codes](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes)

### Option: `model`

Whisper model that will be used for transcription.

The default model is `tiny-int8`, a compressed version of the smallest Whisper model which is able to run on a Raspberry Pi 4.
Compressed models (`int8`) are slightly less accurate than their counterparts, but smaller and faster.

Available models are sorted from least to most accurate.

- `tiny-int8` (43 MB)
- `tiny` (152 MB)
- `base-int8` (80 MB)
- `base` (291 MB)
- `small-int8` (255 MB)
- `small` (968 MB)
- `medium-int8` (786 MB)
- `custom`

### Option: `beam_size`

Number of candidates to consider simultaneously during transcription (see [beam search](https://en.wikipedia.org/wiki/Beam_search)).

Increasing the beam size will increase accuracy at the cost of performance.

## Custom model

There is a possibility to add a custom model from a remote folder (from a repository or from a webpage). The folder should contain the `model.bin`, `vocabulary.txt`, `config.json` and `hash.json`. The `hash.json` file should contain the md5sum type hash of the first 3 files in JSON format.

Eg:
```
{
    "config.json": "e5a2f85afc17f73960204cad2b002633",
    "model.bin": "c21f8eccfdc11978e9496dcb731c54e2",
    "vocabulary.txt": "c1120a13c94a8cbb132489655cdd1854",
}
```

In this case, the `model` field should be `custom`, and add the parent folder url of the model to the `Custom model url` field.

## Backups

Whisper model files can be quite large, so they are automatically excluded from backups. The models will be re-downloaded when the backup is restored.

## Support

Got questions?

You have several options to get them answered:

- The [Home Assistant Discord Chat Server][discord].
- The Home Assistant [Community Forum][forum].
- Join the [Reddit subreddit][reddit] in [/r/homeassistant][reddit]

In case you've found an bug, please [open an issue on our GitHub][issue].

[discord]: https://discord.gg/c5DvZ4e
[forum]: https://community.home-assistant.io
[issue]: https://github.com/home-assistant/addons/issues
[reddit]: https://reddit.com/r/homeassistant
[repository]: https://github.com/hassio-addons/repository
