# Home Assistant Component for Deako Lighting

This component implements support for [Deako](https://deako.com) smart lighting in [Home Assistant](https://home-assistant.io). It is a work in progress, see [issues](issues/) for details on remaining work.

## Installation
Until the component has been submitted to Home Assistant you will need to install the component manually by:

1. Downloading the `components/deako` folder.
2. Copying the `deako` folder to `[installation_root]/config/custom_components/`.
3. Adding the following to `configuration.yaml`:
   ```yaml
   light:
     - platform: deako
   ```
