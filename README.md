# Home Assistant Component for Deako Lighting

This component implements support for [Deako](https://deako.com) smart lighting in [Home Assistant](https://home-assistant.io). It is a work in progress, see [issues](https://github.com/iamwillbar/home-assistant-deako/issues) for details on remaining work.

Only Deako Smart Suite switches can be controlled (if you have the first generation Smart switches you will also need a Deako Connect).

## Installation
Until the component has been submitted to Home Assistant you will need to install the component manually by:

1. Downloading the `components/deako` folder.
2. Copying the `deako` folder to `[installation_root]/config/custom_components/`.
3. Adding the following to `configuration.yaml`:
   ```yaml
   light:
     - platform: deako
   ```
